"""The DocuMind Desk's door on rag-api: the hard gate before any handler runs (workshop lesson 10.5).

A question the law hands to a person (shared/desk_rules.py: posh, grievance, privacy_request, exit_dues,
human_requested) must never reach retrieval or a model, on any path into rag-api - the Chat page's direct brain
streams here, and the MCP server and the A2A peer call /v1/query themselves. So the gate sits in front of the three
routes that take a question, POST /v1/query, /v1/stream and /v1/passages, as a pure ASGI middleware: the handlers
stay exactly as they are, and a hit never enters them. The chat service's langchain, langgraph and adk brains reach
rag-api through a tool their own model chose to call: on those paths the person's words have already reached that
model, and this door sees only the search words the model wrote. It stops the search when those words hit the gate,
which they need not, and the brain's model then writes the reply itself. The chat service's own door
(services/chat/desk.py) keeps those turns from every model: it gates POST /v1/chat before any brain runs, with the
same rules and the same desk_gate switch.

    1. The body is buffered, at most 64 KiB (a 413 above that). QueryRequest caps the question at 4,000 characters,
       but pydantic reads it only after this door has read the body, so that cap does not bound the read.
    2. A body that is not JSON, has no string `query`, or a query over QueryRequest's 4,000 characters is replayed
       unchanged: the handler's own 422 answers it. The gate and the masking run off the event loop.
    3. No hit and no identifier: the original bytes go through untouched, and nothing is read or verified.
    4. Otherwise the caller is verified and the roster checked first, with the functions install() was given
       (auth.py's verify_iap and enforce_membership), so this file calls no verifier of its own and reads no
       tenant's settings for a caller who is not on its roster.
         - A hit: their HTTP errors are answered here - an HTTPException raised in a middleware, outside the app's
           exception handling, would be a 500. Then tenant_settings/{tenant}.desk_gate: off replays the body; on
           returns the fixed reply of shared/desk_law.py - a RAGResponse on /v1/query, a token event then done on
           /v1/stream - with model "none", backend "desk_gate", no citations, cost 0 and 0 tokens. Nothing is
           retrieved, generated or cached.
         - Aadhaar or card numbers and no hit (checked by Verhoeff and Luhn, shared/identifiers.py): a refused
           caller's body is replayed unchanged, so the handler gives its own 401 or 403; for a member, when the
           tenant's desk_gate is on, the numbers are masked before the body is replayed, so neither retrieval nor
           the model sees them. PAN and GSTIN pass. No row is logged for a mask.
    5. A hit that is answered logs {"event": "desk_gate", ...} with the class and the rules version, never the
       question. For posh, grievance and privacy_request the row's user is null and its class "sensitive".

Its own replies are rendered the way FastAPI renders JSON (compact, UTF-8), so a refused caller gets the same bytes
whether or not the question hit the gate. main.py installs it before CORSMiddleware, so CORS wraps it and its replies
carry the same CORS headers as the handlers'. It imports nothing from fastapi or starlette, so its test runs in plain
asyncio with a fake app and fake auth.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time

from shared import desk_law, desk_rules

PATHS = {"/v1/query": "query", "/v1/stream": "stream", "/v1/passages": "passages"}
MAX_BODY = 64 * 1024
QUERY_MAX = 4000        # QueryRequest.query's max_length (schemas.py): a route that takes a longer question raises both


def _read(question: str):
    """The gate's class and the masked question, in one call: the door runs it off the event loop."""
    return desk_rules.gate(question), desk_rules.mask(question)

log = logging.getLogger("documind-api")


class _Headers:
    """The request's headers as verify_iap and shared/iap.py read them: .get(name), case-insensitive."""

    def __init__(self, raw):
        self._h: dict[str, str] = {}
        for k, v in raw or ():
            self._h.setdefault(k.decode("latin-1").lower(), v.decode("latin-1"))

    def get(self, name: str, default=None):
        return self._h.get(name.lower(), default)

    def __getitem__(self, name: str) -> str:
        return self._h[name.lower()]

    def __contains__(self, name) -> bool:
        return isinstance(name, str) and name.lower() in self._h


class _Caller:
    """What verify() is handed in place of a framework request: the headers, which is all it reads."""

    def __init__(self, scope):
        self.scope = scope
        self.headers = _Headers(scope.get("headers"))


def flag_on(doc) -> bool:
    """desk_gate is on only when the tenant's settings say so; a missing field or a failed read is off."""
    v = (doc or {}).get("desk_gate")
    return v is True or (isinstance(v, str) and v.strip().lower() == "on")


async def _respond(send, status: int, body: bytes, content_type: bytes, headers=None) -> None:
    hs = [(b"content-type", content_type), (b"content-length", str(len(body)).encode())]
    for k, v in (headers or {}).items():
        hs.append((str(k).lower().encode("latin-1"), str(v).encode("latin-1")))
    await send({"type": "http.response.start", "status": status, "headers": hs})
    await send({"type": "http.response.body", "body": body})


def _dumps(obj) -> bytes:
    """JSON as FastAPI's JSONResponse renders it: no spaces, UTF-8 as it is, no NaN."""
    return json.dumps(obj, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")


async def _json(send, status: int, obj, headers=None) -> None:
    await _respond(send, status, _dumps(obj), b"application/json", headers)


def _replay(body: bytes, receive):
    """A receive() that hands the app the buffered body once, then whatever the server sends next (a disconnect)."""
    sent = False

    async def receive_again():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": body, "more_body": False}
        return await receive()
    return receive_again


def _with_length(scope, n: int):
    hs = [(k, v) for k, v in scope.get("headers") or () if k.lower() != b"content-length"]
    return {**scope, "headers": hs + [(b"content-length", str(n).encode())]}


class DeskDoor:
    def __init__(self, app, settings, verify, member):
        self.app, self.settings, self.verify, self.member = app, settings, verify, member

    async def _on(self, tenant: str) -> bool:
        try:
            return flag_on(await asyncio.to_thread(self.settings, tenant))
        except Exception:  # noqa: BLE001 - a failed read is off, as rag-api's own tenant_settings() treats it
            return False

    async def __call__(self, scope, receive, send):
        surface = PATHS.get(scope.get("path")) if scope.get("type") == "http" and scope.get("method") == "POST" else None
        if surface is None:
            return await self.app(scope, receive, send)
        t0 = time.time()
        too_big = {"detail": f"request body over {MAX_BODY} bytes"}
        declared = _Headers(scope.get("headers")).get("content-length")
        if declared and declared.strip().isdigit() and int(declared) > MAX_BODY:
            return await _json(send, 413, too_big)
        chunks, size = [], 0
        while True:
            msg = await receive()
            if msg["type"] == "http.disconnect":
                return None
            part = msg.get("body", b"")
            size += len(part)
            if size > MAX_BODY:
                return await _json(send, 413, too_big)
            chunks.append(part)
            if not msg.get("more_body"):
                break
        body = b"".join(chunks)
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            payload = None
        question = payload.get("query") if isinstance(payload, dict) else None
        if not isinstance(question, str):
            return await self.app(scope, _replay(body, receive), send)
        if len(question) > QUERY_MAX:              # the handler's own 422 answers it; nothing is read past the cap
            return await self.app(scope, _replay(body, receive), send)
        tenant = payload.get("tenant_id")
        cls, (masked, kinds) = await asyncio.to_thread(_read, question)
        if not isinstance(tenant, str) or not tenant or (cls is None and not kinds):
            return await self.app(scope, _replay(body, receive), send)
        try:
            user = await asyncio.to_thread(self.verify, _Caller(scope))
            await asyncio.to_thread(self.member, user["email"], tenant)
        except Exception as e:  # noqa: BLE001 - an HTTP error is answered here; anything else is the server's 500
            status = getattr(e, "status_code", None)
            if not isinstance(status, int):
                raise
            if cls is None:                         # nothing to mask for a caller the handler refuses: it answers
                return await self.app(scope, _replay(body, receive), send)
            return await _json(send, status, {"detail": getattr(e, "detail", str(e))}, getattr(e, "headers", None))
        if cls is None:
            if await self._on(tenant):
                payload["query"] = masked
                body = json.dumps(payload).encode()
                return await self.app(_with_length(scope, len(body)), _replay(body, receive), send)
            return await self.app(scope, _replay(body, receive), send)
        if not await self._on(tenant):
            return await self.app(scope, _replay(body, receive), send)
        sensitive = cls in desk_rules.SENSITIVE
        log.info(json.dumps({"event": "desk_gate", "surface": surface, "tenant": tenant,
                             "user": None if sensitive else user["email"],
                             "class": "sensitive" if sensitive else cls, "rules_version": desk_rules.RULES_VERSION}))
        text = desk_law.template(cls)
        latency = int((time.time() - t0) * 1000)
        usage = {"tokens_in": 0, "tokens_out": 0, "cached_tokens": 0, "cost_usd": 0.0, "model": "none", "backend": "desk_gate"}
        if surface == "stream":
            done = {**usage, "latency_ms": latency, "stages": {}, "cache_hit": "none"}
            sse = (f"event: token\ndata: {json.dumps({'t': text})}\n\n"
                   f"event: done\ndata: {json.dumps(done)}\n\n").encode()
            return await _respond(send, 200, sse, b"text/event-stream; charset=utf-8")
        if surface == "passages":
            return await _json(send, 200, {"passages": [], "answer": text, "answerable": False, "usage": usage})
        return await _json(send, 200, {"answer": text, "citations": [], "confidence": "low", "answerable": False,
                                       **usage, "latency_ms": latency, "stages": {}, "cache_hit": "none"})


def install(app, settings, verify, member) -> None:
    """Put the door in front of the app. settings(tenant) returns tenant_settings/{tenant}; verify(request) returns
    {"email": ...} or raises 401; member(email, tenant) raises 403. Starlette makes the middleware added last the
    outermost, so a line added after this one - main.py's CORSMiddleware - wraps the door."""
    app.add_middleware(DeskDoor, settings=settings, verify=verify, member=member)
