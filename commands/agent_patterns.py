#!/usr/bin/env python3
"""The agent bench's patterns (workshop lessons 10.1-10.3 and 10.5): one question through one agent pattern, every
model call recorded. commands/agent_turn.py prints one turn (make agent-turn); evals/agent_eval.py scores a task set
over patterns, thinking levels and desks (make agent-eval).

    loop          the Desk agent's own loop (services/chat/desk_agent.py, workshop lesson 10.4): langchain's
                  create_agent over a desk's tools (desk_agent.TOOLSETS: astar, one retrieve over every class the
                  person may read and every calculator; or handbook or statute), the desk's system prompt, the turn's
                  limits (desk_agent.DeskTurnLimits), the recorder, then the guard (desk_agent._guard). The model
                  thinks natively between its calls
    react_text    lesson 10.1: prompted ReAct, for a model with no function calling. No function declaration is sent:
                  the desk's tools are written into the prompt, the model writes "Thought: ..." and "Action:
                  <tool>[<JSON arguments>]" and stops at "Observation:", and code reads the Action and runs it. The
                  Observation is always code's: a result, a refusal or a format error (REACT_TEXT below)
    plan_first    lesson 10.1: the loop, its prompt led by an instruction to write a plan first. Nothing runs the
                  plan: the model reads it back on every later call, and the loop still decides each call
    planned       plan_execute and rewoo (lesson 10.2), verify (10.3): each joins PATTERNS under its own name, on the
                  same tools, the same context and the same recorder, so the bench compares patterns and nothing else.
                  Until then naming one is an error that says so

Nothing in services/chat changes. The bench imports desk_agent's tools, prompt, middleware and model and builds an
agent of its own beside the Desk's (desk_agent.agent() is never called), so a turn here is the Desk's agent mode with a
recorder added and no router in front: the desk is chosen, not routed.

THE CONTEXT. context() is the dict desk_agent.run() hands its agent (desk_agent.py, run()): the tenant, the person's
assertion, the turn's Meter, the desk's classes and tool names, the masked message the argument check reads
(desk_calc.check_args), an empty ledger, no calculations; plus bench_calls, the recorder's list. The tools read it
through their ToolRuntime as in the Desk, so a calculator refuses here what it refuses there. The Meter is the turn's
own, at the chat service's limits (12 model calls, Rs 5, 100 s); in the Desk it is the router's, which has already
counted the router's call. mirror() shapes a turn's messages exactly as run() does, and a test holds the two equal.

THE RECORDER. A wrap_model_call middleware and nothing else: a before_model or after_model hook would add graph nodes
(limits.TurnLimitsMiddleware's rule). It sits inside DeskTurnLimits, so it records every call the turn's limits let
through and none they refuse: the thinking level the call was sent with; input and cached tokens; thinking tokens, from
usage_metadata's output_token_details["reasoning"] (langchain-google-genai 4.4.0 reads Gemini's thoughts_token_count
into it and adds the same count to output_tokens, chat_models.py:2051-2064); visible tokens, the output less the
thinking; the rupees at list price (shared/prices.py, where thinking is billed as output); the tool calls the model
asked for, with their arguments; and its text. The Meter charges the same calls at the same price, so the recorder's
rupees add up to the turn's.

THINKING. None keeps the desk agent's own level (desk_agent.THINKING_LEVEL, low, set on the model). minimal, low,
medium or high is sent with every call as its thinking_level, which langchain-google-genai reads per call, and the
recorder notes the level each call carried. Which levels gemini-3.6-flash takes on location global is a lane's fact:
the bench sends what it is asked to. Every pattern's calls go through the recorder, react_text's too.

REACT_TEXT (_react_text()). A two-node LangGraph StateGraph on the turn's context: think, then act while there is an
Action. think renders the turn as text (transcript(): the question, then each step as code read it and the
Observation code wrote after it) into one user message, under a system prompt that holds the desk's own prompt,
REACT_PROTOCOL and the desk's tools as JSON lines (declarations(): each tool as ChatGoogleGenerativeAI.bind_tools
converts it, convert_to_openai_tool, chat_models.py:4632). The transcript is the user turn because langchain-google-
genai 4.4.0 refuses a request ending on a model turn for gemini-3.6-flash (no prefill, chat_models.py:3829-3838). The
call binds no tools and sends the stop sequence "Observation:" (STOP; stop_sequences, chat_models.py:3631), and it goes
through the loop's own two wrappers, applied by hand: DeskTurnLimits around the recorder. So the turn's Meter is asked
before every call (the call cap, the rupees, the deadline, each call's timeout, each call priced as the agent's model)
and a runaway loop ends at the cap with stopped_by model_calls, as the loop's does; THINKING goes with every call.
read_step() reads the reply. It first cuts it at its first "Observation:", in one line marked as the cut (the Change-it
of lesson 10.1): whatever a model writes past its stop sequence, an observation of its own included, is never read. A
Final Answer then ends the turn; otherwise its one Action becomes a tool call, on an AIMessage code builds and never
sends; anything else is a format error. act is langgraph's ToolNode over the desk's tools with limits.timed_tool_call,
the wrapper LangGraphBrain's ToolNode takes (brains.py), so check_args, the ledger, the tools' timeouts and the error
contract are the Desk's own. A result, a refusal (check_args', or ToolNode's for a name or an argument it cannot take)
or a format error is the next Observation, for the model to read and correct. Each code-built message keeps the step
in additional_kwargs["react"]: what the model wrote, what code read, what the cut dropped, the Action, the Final
Answer or the error; trace() carries it, and commands/agent_turn.py prints it.

OFFLINE (offline(), scripted()). Only the two things that leave the process are replaced. rag-api: the one
documind_tools.retrieve runs its local lane (_retrieve_local: the lexical ranking and the evidence gate) over the chunks
shared/documind_corpus.py mints for the tenant, held in memory in place of the Chroma directory, each search ranked
once a run. The model: ScriptedModel follows the row of evals/agent_tasks.jsonl that asks its question. It searches with
the row's search words, calls the row's calculator with the row's arguments and answers from what the calculator
returned; on a lookup it quotes the clause's sentence; with no row it searches once and works out no figure. Its
tokens are the script's: four characters a token over what it is sent and what it writes (no tool declarations), and
0, 64, 256 or 1,024 thinking tokens a call at minimal, low, medium or high. With slips on (evals/agent_eval.py) it skips the calculator on
about one run in five of a calculator row (a crc32 of the row id and the run) and writes the figure itself, from code,
so the run is right with no calculator behind it; on a trap row it does so on its first run. A single turn
(commands/agent_turn.py) never slips. When its prompt opens with PLAN_FIRST, its first message also writes a plan
(plan_text()). react_text's model is ScriptedTextModel (scripted(pattern="react_text")): it takes no tools (bind_tools
raises, as for a model with no function calling), reads the transcript back into the same history, takes the same
step and writes it as Thought and Action, or Thought and Final Answer; its tokens count all it is sent, the
declarations in its prompt among them, where the loop's script counts none. It honours a stop sequence as Gemini does
(the reply ends before it). invents plays a model whose stop sequence does not hold, for the Change-it: after its
calculator's Action it writes an Observation of its own (agent_turn.py's --invent: "Rs 2,50,000") and a Final Answer
from it. replies, a fixed list of replies, is for tests and page cells: a malformed Action, an invented wage, a loop.
No credential, no network, no cost.
"""
from __future__ import annotations

import json
import math
import re
import sys
import warnings
import zlib
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Callable

KIT = Path(__file__).resolve().parents[1]
for _p in (str(KIT / "services" / "chat"), str(KIT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from shared import desk_calc, prices  # noqa: E402 - the standard library only

TASKS = KIT / "evals" / "agent_tasks.jsonl"
OFFLINE_PROJECT = "documind-ai-YOUR-ID"     # the placeholder the offline corpus's source_uri carries
THINKING_LEVELS = ("minimal", "low", "medium", "high")
SCRIPTED_THINKING = {"minimal": 0, "low": 64, "medium": 256, "high": 1024}
CHARS_PER_TOKEN = 4
# The patterns the lessons add, each in its own pull request, and the lesson it is for.
PLANNED = {"plan_execute": "10.2", "rewoo": "10.2", "verify": "10.3"}
STOP = "Observation:"           # react_text's stop sequence, and where its parser cuts what the model wrote


def _da():
    """services/chat/desk_agent.py, on first use: it needs the chat image's pins."""
    import desk_agent
    return desk_agent


def classes_for(desk: str) -> list[str]:
    """The doc_type classes a desk's retrieve searches: the desk's own (desk_routes.doc_types), or for astar every class
    of the answer desks, as desk_graph gives arm A* for a person who may read both."""
    import desk_routes
    if desk in desk_routes.ANSWER_DESKS:
        return desk_routes.doc_types(desk)
    return desk_routes.fallback_doc_types(desk_routes.ANSWER_DESKS)


# ----------------------------------------------------------------------------- the context and the recorder
def context(desk: str, question: str, tenant: str = "acme", classes=None, meter=None, assertion=None) -> dict:
    """The context desk_agent.run() builds for its agent (desk_agent.py, run()), and the recorder's list."""
    import limits
    da = _da()
    return {"tenant": tenant, "assertion": assertion, "meter": meter or limits.Meter(model=da.AGENT_MODEL),
            "desk_classes": list(classes if classes is not None else classes_for(desk)), "desk_message": question or "",
            "desk_ledger": [], "desk_calcs": [], "desk_answerable": False,
            "desk_tools": tuple(t.name for t in da.TOOLSETS[desk]), "bench_calls": []}


def call_record(n: int, usage: dict | None, level: str, model: str, tool_calls=(), text: str = "",
                message_id: str | None = None) -> dict:
    """One model call as the recorder keeps it. output_tokens counts the thinking (langchain-google-genai adds
    thoughts_token_count to it); the visible tokens are the rest. The rupees are list price, thinking as output."""
    u = usage or {}
    tokens_in, tokens_out = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
    cached = int((u.get("input_token_details") or {}).get("cache_read") or 0)
    thinking = int((u.get("output_token_details") or {}).get("reasoning") or 0)
    return {"n": n, "id": message_id, "model": model, "thinking_level": level, "tokens_in": tokens_in,
            "cached_tokens": cached, "thinking_tokens": thinking, "visible_tokens": max(tokens_out - thinking, 0),
            "tokens_out": tokens_out, "inr": round(prices.inr(prices.usd(model, tokens_in, tokens_out, cached)), 6),
            "tool_calls": [{"name": tc.get("name"), "args": tc.get("args") or {}} for tc in tool_calls or ()],
            "text": text}


def recorder(thinking: str | None = None, model: str | None = None):
    """The wrap-only recorder: each model call into the context's bench_calls, its thinking level sent when given."""
    from langchain.agents.middleware import AgentMiddleware
    from langchain_core.messages import AIMessage
    da = _da()
    priced = model or da.AGENT_MODEL

    class Recorder(AgentMiddleware):
        """Records each model call the turn's limits let through, and sends THINKING with it."""

        def _send(self, request):
            if thinking:
                request = request.override(model_settings={**request.model_settings, "thinking_level": thinking})
            return request

        def _level(self, request) -> str:
            return (request.model_settings.get("thinking_level") or getattr(request.model, "thinking_level", None)
                    or da.THINKING_LEVEL)

        def _log(self, request, response):
            calls = request.runtime.context["bench_calls"]
            inner = getattr(response, "model_response", response)          # an ExtendedModelResponse wraps one
            for m in getattr(inner, "result", None) or [inner]:
                if isinstance(m, AIMessage):
                    calls.append(call_record(len(calls) + 1, m.usage_metadata, self._level(request), priced,
                                             m.tool_calls, da._text(m.content), m.id))
            return response

        def _failed(self, request, exc: BaseException) -> None:
            calls = request.runtime.context["bench_calls"]
            calls.append({**call_record(len(calls) + 1, None, self._level(request), priced), "error": type(exc).__name__})

        def wrap_model_call(self, request, handler):
            request = self._send(request)
            try:
                response = handler(request)
            except Exception as exc:                       # noqa: BLE001 - recorded, then raised as it was
                self._failed(request, exc)
                raise
            return self._log(request, response)

        async def awrap_model_call(self, request, handler):
            request = self._send(request)
            try:
                response = await handler(request)
            except Exception as exc:                       # noqa: BLE001
                self._failed(request, exc)
                raise
            return self._log(request, response)

    return Recorder()


# ----------------------------------------------------------------------------- the patterns
def _loop(question: str, ctx: dict, *, desk: str, llm, recorder, prompt: str | None = None) -> list:
    """The Desk agent's loop, as desk_agent.agent() builds it and run() invokes it, with the recorder inside the turn's
    limits: create_agent over the desk's tools, no checkpointer, the framework's recursion limit as the backstop. prompt
    replaces the desk's system prompt (plan_first's)."""
    import limits
    from langchain.agents import create_agent
    from langchain_core.messages import HumanMessage
    from langgraph.errors import GraphRecursionError
    da = _da()
    agent = create_agent(model=llm, tools=da.TOOLSETS[desk], system_prompt=prompt or da.system_prompt(desk),
                         middleware=[da.DeskTurnLimits(), recorder, da._guard()], checkpointer=False,
                         name=f"bench_{desk}")
    try:
        out = agent.invoke({"messages": [HumanMessage(content=question)]},
                           config={"recursion_limit": limits.recursion_limit()}, context=ctx)
        return out["messages"]
    except GraphRecursionError:              # the backstop tripped before the Meter: the turn stops, whole
        limits.meter_of(ctx).stop("recursion_limit")
        return [limits.stop_message()]


# plan_first (lesson 10.1): the instruction that leads the desk's prompt. Nothing runs the plan it asks for.
PLAN_FIRST = ("Plan first. Before your first tool call, write your plan as numbered steps: each search and each "
              "calculator you will use, in order, and what each needs from the question or a passage. Then work "
              "through it, one call at a time.")


def _plan_first(question: str, ctx: dict, *, desk: str, llm, recorder) -> list:
    """The loop, its system prompt led by PLAN_FIRST. The plan is text in the model's first message, read back on
    every later call; no code executes it, so the loop decides each call as before and the model may leave its plan
    (lesson 10.2's patterns execute theirs)."""
    return _loop(question, ctx, desk=desk, llm=llm, recorder=recorder,
                 prompt=PLAN_FIRST + "\n\n" + _da().system_prompt(desk))


# react_text (lesson 10.1): the text protocol, after the desk's own prompt and before its tools.
REACT_PROTOCOL = (
    "You cannot call functions here: you use a tool by writing it as text, and code runs it. Write one step a "
    "reply, in this form:\n\n"
    "Thought: what you need next, and why\n"
    "Action: <tool>[<its arguments, as one JSON object>]\n\n"
    "and stop there. Code runs the tool and writes what it returned on the next line, as \"Observation: ...\": never "
    "write an Observation yourself. When the observations hold what your answer needs, reply instead with\n\n"
    "Thought: why you can answer now\n"
    "Final Answer: your answer to the person, citing each passage you use as [n]\n\n"
    "The tools, one JSON declaration a line (its name, what it does, its parameters):")
_LABEL = r"^[ \t*_]*{}[ \t*_]*:[ \t*_]*"                  # a label at a line's start, markdown emphasis allowed
_ACTIONS = re.compile(_LABEL.format("Action"), re.M | re.I)
_ACTION = re.compile(_LABEL.format("Action") + r"([A-Za-z_][\w.-]*)[ \t]*\[\s*", re.M | re.I)
_FINAL = re.compile(_LABEL.format("Final[ \t]+Answer"), re.M | re.I)
FORMAT = "format error: "                # the start of every Observation the parser writes
_FORM = "<tool>[<its arguments, as one JSON object>]"


def declarations(desk: str) -> list[dict]:
    """The desk's tools as the loop declares them to Gemini (ChatGoogleGenerativeAI.bind_tools converts each with
    convert_to_openai_tool), each description on one line: what react_text writes into its prompt instead."""
    from langchain_core.utils.function_calling import convert_to_openai_tool
    out = []
    for t in _da().TOOLSETS[desk]:
        d = convert_to_openai_tool(t)["function"]
        out.append({**d, "description": " ".join(d["description"].split())})
    return out


def react_prompt(desk: str) -> str:
    """react_text's system prompt: the desk's own, REACT_PROTOCOL, then each tool's declaration as a JSON line."""
    return (_da().system_prompt(desk) + "\n\n" + REACT_PROTOCOL + "\n"
            + "\n".join(json.dumps(d, ensure_ascii=False) for d in declarations(desk)))


def read_step(text: str) -> dict:
    """One react_text reply, read by code: {read, final} when it holds a Final Answer, which ends the turn; {read,
    action: {name, args}} for its one Action; {read, error} otherwise, the Observation that names the fix. read is the
    text code read: the reply up to its first "Observation:", which only code may write."""
    text = text.split(STOP, 1)[0]       # THE CUT: from the first "Observation:" on, nothing the model wrote is read
    text = text.strip()
    final = _FINAL.search(text)
    if final:
        return {"read": text, "final": text[final.end():].strip()}
    actions = list(_ACTIONS.finditer(text))
    if not actions:
        return {"read": text, "error": FORMAT + f"no Action and no Final Answer. Write one Action, as Action: {_FORM}, "
                                                "or a Final Answer."}
    if len(actions) > 1:
        return {"read": text, "error": FORMAT + f"{len(actions)} Actions in one reply. Write one, then stop: code runs "
                                                "it and writes its Observation."}
    found = _ACTION.match(text, actions[0].start())
    if not found:
        return {"read": text, "error": FORMAT + f"the Action is not written as {_FORM}. Write it so, as in Action: "
                                                "retrieve[{\"query\": \"what to look for\"}]."}
    name = found.group(1)
    try:
        args, end = json.JSONDecoder().raw_decode(text, found.end())
        if not isinstance(args, dict):
            raise ValueError(f"a JSON {type(args).__name__}, not an object")
        if not text[end:].lstrip().startswith("]"):
            raise ValueError("no ] after the object")
    except ValueError as e:                  # json.JSONDecodeError is one
        why = e.msg if isinstance(e, json.JSONDecodeError) else str(e)
        return {"read": text, "error": FORMAT + f"the arguments of {name} are not one JSON object in brackets ({why}). "
                                                f"Write them as JSON, as in Action: {name}[{{\"argument\": value}}]."}
    return {"read": text, "action": {"name": name, "args": args}}


def transcript(messages: list) -> str:
    """react_text's turn as its model reads it: the question, then each step as code read it, each followed by the
    Observation code wrote: the tool's result or error, or the parser's format error."""
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
    da = _da()
    lines = []
    for m in messages:
        if isinstance(m, HumanMessage):
            lines.append(f"Question: {da._text(m.content)}")
        elif isinstance(m, AIMessage):
            step = m.additional_kwargs.get("react") or {}
            lines.append(step.get("read", da._text(m.content)))
            if step.get("error"):
                lines.append(f"{STOP} {step['error']}")
        elif isinstance(m, ToolMessage):
            lines.append(f"{STOP} {da._text(m.content)}")
    return "\n".join(lines)


def _react_text(question: str, ctx: dict, *, desk: str, llm, recorder) -> list:
    """Prompted ReAct (the module's REACT_TEXT): think writes one step as text through the loop's own wrappers, act runs
    its Action through ToolNode with the brains' timed wrapper, until a Final Answer or the turn's limits."""
    import limits
    from langchain.agents.middleware import ModelRequest, ModelResponse
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    from langgraph.errors import GraphRecursionError
    from langgraph.graph import END, START, MessagesState, StateGraph
    from langgraph.prebuilt import ToolNode
    da = _da()
    system, turn_limits = SystemMessage(content=react_prompt(desk)), da.DeskTurnLimits()

    def call(request):                       # the model call itself: no tool bound, the stop sequence sent
        return ModelResponse(result=[request.model.invoke([request.system_message, *request.messages], stop=[STOP],
                                                          **request.model_settings)])

    def think(state, runtime):
        request = ModelRequest(model=llm, system_message=system, state=state, runtime=runtime,
                               messages=[HumanMessage(content=transcript(state["messages"]))])
        out = turn_limits.wrap_model_call(request, lambda r: recorder.wrap_model_call(r, call))
        if isinstance(out, AIMessage):       # the turn's limits refused the call: the stop, as the loop's
            return {"messages": [out]}
        reply = out.result[0]
        wrote = da._text(reply.content)
        step = {**read_step(wrote), "wrote": wrote}
        step["cut"] = wrote.strip()[len(step["read"]):].strip()        # what the cut dropped, if anything
        action = step.get("action")
        calls = ([{"name": action["name"], "args": action["args"], "id": f"action-{len(state['messages'])}",
                   "type": "tool_call"}] if action else [])
        return {"messages": [AIMessage(content=step["final"] if "final" in step else step["read"], tool_calls=calls,
                                       id=reply.id, usage_metadata=reply.usage_metadata,
                                       additional_kwargs={"react": step})]}

    def route(state):
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "act"
        return "think" if (last.additional_kwargs.get("react") or {}).get("error") else END

    g = StateGraph(MessagesState, context_schema=dict)
    g.add_node("think", think)
    g.add_node("act", ToolNode(da.TOOLSETS[desk], wrap_tool_call=limits.timed_tool_call))   # LangGraphBrain's seam
    g.add_edge(START, "think")
    g.add_conditional_edges("think", route, {"act": "act", "think": "think", END: END})
    g.add_edge("act", "think")
    try:
        out = g.compile().invoke({"messages": [HumanMessage(content=question)]},
                                 config={"recursion_limit": limits.recursion_limit()}, context=ctx)
        return out["messages"]
    except GraphRecursionError:              # the backstop tripped before the Meter: the turn stops, whole
        limits.meter_of(ctx).stop("recursion_limit")
        return [limits.stop_message()]


@dataclass(frozen=True)
class Pattern:
    name: str
    lessons: str
    what: str
    turn: Callable          # turn(question, ctx, *, desk, llm, recorder) -> the turn's messages
    text: bool = False      # its model writes its actions as text, no function declared: scripted()'s text model


PATTERNS: dict[str, Pattern] = {
    "loop": Pattern("loop", "10.1-10.3, 10.5", "the Desk agent's own loop: create_agent over a desk's tools, the model "
                    "thinking natively between its calls", _loop),
    "react_text": Pattern("react_text", "10.1", "prompted ReAct: no function declaration sent, the tools written into "
                          "the prompt, the model writing Thought and Action as text and stopping at \"Observation:\", "
                          "code reading the Action, running it through ToolNode and writing each Observation",
                          _react_text, text=True),
    "plan_first": Pattern("plan_first", "10.1", "the loop, its prompt led by an instruction to write a plan first: "
                          "nothing runs the plan, and the loop still decides every call", _plan_first),
}


def pattern(name: str) -> Pattern:
    if name in PATTERNS:
        return PATTERNS[name]
    if name in PLANNED:
        raise ValueError(f"pattern {name!r} is planned for lesson {PLANNED[name]}'s pull request and not built yet; "
                         f"built: {', '.join(PATTERNS)}")
    raise ValueError(f"no pattern {name!r}: built {', '.join(PATTERNS)}; planned {', '.join(PLANNED)}")


def gemini():
    """The Desk agent's model as the chat service builds it (desk_agent.chat_model(): gemini-3.6-flash on location
    global, thinking low, the call timeout and attempts of services/chat/limits.py). It reads GOOGLE_CLOUD_PROJECT, and
    every call it makes is a billed Vertex AI call."""
    return _da().chat_model()


def run(name: str, question: str, *, llm, desk: str = "astar", thinking: str | None = None, tenant: str = "acme",
        classes=None, meter=None, assertion=None) -> dict:
    """One turn of pattern `name` on `question`, as one record: desk_agent.run()'s keys (mirror()), the composed
    section, every model call (calls), the trace of calls and tool results, and the totals. llm is gemini() on a lane,
    scripted() offline."""
    if thinking is not None and thinking not in THINKING_LEVELS:
        raise ValueError(f"thinking is one of {', '.join(THINKING_LEVELS)}, or unset for the desk agent's own")
    p = pattern(name)
    ctx = context(desk, question, tenant=tenant, classes=classes, meter=meter, assertion=assertion)
    messages = p.turn(question, ctx, desk=desk, llm=llm, recorder=recorder(thinking))
    return record(name, desk, thinking, ctx, messages)


# ----------------------------------------------------------------------------- one turn's record
def mirror(ctx: dict, messages: list) -> dict:
    """desk_agent.run()'s result from a turn's context and messages, shaped line for line as run() shapes it."""
    import limits
    from langchain_core.messages import AIMessage, ToolMessage
    da = _da()
    meter = limits.meter_of(ctx)
    last = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
    answer = da._text(last.content) if last is not None else ""
    held = set(ctx["desk_tools"])           # a name the model made up is "unknown": no model text reaches a log

    def named(name) -> str:
        return name if name in held else "unknown"

    calls = [named(tc.get("name")) for m in messages for tc in (getattr(m, "tool_calls", None) or [])]
    results = [m for m in messages if isinstance(m, ToolMessage)]
    stopped = meter.stopped_by is not None or answer == limits.STOP_ANSWER
    seen, calcs = set(), []
    for c in ctx["desk_calcs"]:
        key = (c["calculator"], c["formula"])
        if key not in seen:
            seen.add(key)
            calcs.append(c)
    return {"answer": answer, "passages": list(ctx["desk_ledger"]), "calculations": calcs, "tool_calls": calls,
            "refusals": [named(m.name) for m in results if m.status == "error"],
            "retrieve_calls": sum(m.name == "retrieve" and m.status != "error" for m in results),   # searches sent
            "answerable": bool(ctx["desk_answerable"]) and not stopped and bool(answer.strip()),
            "stopped_by": meter.stopped_by}


def _source(uri) -> str:
    """An object's file name: a lane's source_uri names its project, and a saved run never does."""
    return str(uri or "").rsplit("/", 1)[-1]


def _json(content):
    if isinstance(content, (dict, list)):
        return content
    try:
        return json.loads(content)
    except (TypeError, ValueError):
        return None


def tool_result(name: str, status: str, content) -> dict:
    """What a tool returned, short: a search's passages by n, source and section; a calculator's figure, formula and
    sections; a refusal's or an error's words."""
    body = _json(content)
    if status == "error" or not isinstance(body, dict):
        return {"error" if status == "error" else "text": str(content)[:400]}
    if name == "retrieve":
        out = {"passages": [{k: p.get(k) for k in ("n", "source", "doc_type", "section")}
                            for p in body.get("passages") or ()], "answerable": body.get("answerable")}
        out.update({k: body[k] for k in ("error", "note", "timed_out") if k in body})
        return out
    return {k: body.get(k) for k in ("value", "unit", "formula", "cites", "error", "timed_out") if k in body}


def trace(messages: list, calls: list, held) -> list[dict]:
    """The turn step by step: each model message (its recorded call's n, its text) with the tools it asked for, their
    arguments and what each returned. A tool name the desk does not hold shows as unknown, with no arguments. A
    react_text step also carries what the model wrote and what code read of it (react)."""
    from langchain_core.messages import AIMessage, ToolMessage
    da = _da()
    by_id = {c.get("id"): c["n"] for c in calls if c.get("id")}
    steps, tools = [], {}
    for m in messages:
        if isinstance(m, AIMessage):
            step = {"call": by_id.get(m.id), "text": da._text(m.content), "tools": []}
            if m.additional_kwargs.get("react"):
                step["react"] = dict(m.additional_kwargs["react"])
            for tc in m.tool_calls or ():
                known = tc.get("name") in held
                tool = {"name": tc.get("name") if known else "unknown", "args": tc.get("args") if known else {},
                        "status": None, "result": None}
                step["tools"].append(tool)
                tools[tc.get("id")] = tool
            steps.append(step)
        elif isinstance(m, ToolMessage) and m.tool_call_id in tools:
            tool = tools[m.tool_call_id]
            tool["status"], tool["result"] = m.status, tool_result(tool["name"], m.status, m.content)
    return steps


def record(name: str, desk: str, thinking: str | None, ctx: dict, messages: list) -> dict:
    """One turn, JSON-ready: mirror()'s keys (the passages by file name, never a URI), the section as the Desk composes
    it, every recorded call, the trace and the totals."""
    import limits
    da = _da()
    got = mirror(ctx, messages)
    calls, meter = ctx["bench_calls"], limits.meter_of(ctx)
    passages = [{"n": p.get("n"), "chunk_id": p.get("chunk_id"), "source": _source(p.get("source_uri")),
                 "page": p.get("page"), "doc_type": p.get("doc_type"), "section": p.get("section"),
                 "text": p.get("text")} for p in got["passages"]]
    return {**got, "passages": passages, "pattern": name, "desk": desk, "tenant": ctx["tenant"],
            "question": ctx["desk_message"], "thinking": thinking, "composed": da.compose(got),
            "calls": calls, "trace": trace(messages, calls, set(ctx["desk_tools"])), "model_calls": len(calls),
            **{k: sum(c.get(k) or 0 for c in calls)
               for k in ("tokens_in", "cached_tokens", "thinking_tokens", "visible_tokens", "tokens_out")},
            "inr": round(sum(c.get("inr") or 0 for c in calls), 6), "rag_inr": round(prices.inr(meter.rag_cost_usd), 6)}


# ----------------------------------------------------------------------------- offline: the corpus in memory
_CHUNKS: dict[str, list] = {}


class CorpusStore:
    """The local lane's Chroma directory, in memory: the tenant's chunks as shared/documind_corpus.py mints them (the
    metadata shared/local_corpus.py writes), and the one call documind_tools._retrieve_local makes of a store."""

    @staticmethod
    def chunks(tenant: str) -> list[dict]:
        if tenant not in _CHUNKS:
            from shared import documind_corpus
            with warnings.catch_warnings():            # the loader leaves its files to the garbage collector
                warnings.simplefilter("ignore", ResourceWarning)
                docs = documind_corpus.load_documents(tenant, str(KIT / "evals"), OFFLINE_PROJECT)
            _CHUNKS[tenant] = [c for d in docs for c in documind_corpus.chunk_document(d, tenant)]
        return _CHUNKS[tenant]

    def get(self, where=None, include=None) -> dict:
        clauses = (where or {}).get("$and", [where or {}])
        tenant = next((c["tenant_id"] for c in clauses if "tenant_id" in c), None)
        want = next((c["doc_type"] for c in clauses if "doc_type" in c), None)
        allowed = None if want is None else set(want["$in"]) if isinstance(want, dict) else {want}
        rows = [c for c in self.chunks(tenant) if allowed is None or c["doc_type"] in allowed] if tenant else []
        return {"documents": [c["text"] for c in rows],
                "metadatas": [{"tenant_id": tenant, "doc_type": c["doc_type"], "page": c["page_start"],
                               "source_uri": c["source_uri"], "chunk_id": c["chunk_id"],
                               **({"section": c["section"]} if c.get("section") else {})} for c in rows]}


@contextmanager
def offline():
    """rag-api's place taken by the kit's corpus while the block runs: documind_tools.retrieve on its local lane over a
    CorpusStore, each distinct search ranked once. Put back on the way out."""
    from shared import documind_tools
    from shared import profile as lane_profile
    lane, memo = documind_tools.retrieve, {}

    def retrieve(query, tenant_id, top_k=5, doc_type=None, assertion=None, brain=None, passages=False):
        key = json.dumps([query, tenant_id, top_k, doc_type, passages])
        if key not in memo:
            memo[key] = lane(query, tenant_id, top_k=top_k, doc_type=doc_type, assertion=assertion, brain=brain,
                             passages=passages)
        return deepcopy(memo[key])

    saved = (documind_tools.PROFILE, lane_profile.build_store, documind_tools.retrieve)
    documind_tools.PROFILE, documind_tools.retrieve = "local", retrieve
    lane_profile.build_store = lambda embeddings=None: CorpusStore()
    try:
        yield
    finally:
        documind_tools.PROFILE, lane_profile.build_store, documind_tools.retrieve = saved


# ----------------------------------------------------------------------------- offline: the scripted model
def tasks(path: Path = TASKS) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def task_for(question: str, tenant: str | None = None) -> dict | None:
    """The row of evals/agent_tasks.jsonl that asks this question (of this tenant), or None."""
    return next((r for r in tasks() if r["question"] == question and tenant in (None, r["tenant"])), None)


def slips(task: dict, run: int) -> bool:
    """Whether the scripted model writes this run's figure itself: a trap row on its first run, a calculator row on
    about one run in five."""
    if task["kind"] == "trap":
        return run == 0
    return task["kind"] == "calc" and zlib.crc32(f"{task['id']}:{run}".encode()) % 5 == 0


def scripted_usage(chars_in: int, text: str, calls: list, level: str) -> dict:
    """The script's token counts, in usage_metadata's shape: four characters a token in and out, and a fixed number of
    thinking tokens a call for the level (output_token_details only when there are some, as langchain-google-genai
    reports them)."""
    tokens_in = max(1, math.ceil(chars_in / CHARS_PER_TOKEN))
    written = len(text) + sum(len(c["name"]) + len(json.dumps(c["args"])) for c in calls)
    visible, thinking = max(1, math.ceil(written / CHARS_PER_TOKEN)), SCRIPTED_THINKING.get(level, 0)
    usage = {"input_tokens": tokens_in, "output_tokens": visible + thinking, "total_tokens": tokens_in + visible + thinking,
             "input_token_details": {"cache_read": 0}}
    if thinking:
        usage["output_token_details"] = {"reasoning": thinking}
    return usage


def _stem(name) -> str:
    return _source(name).rsplit(".", 1)[0]


def _holds(task: dict, passage: dict) -> bool:
    """The passage is the row's clause: a handbook clause by its code, a Code's window by its file."""
    if task.get("rule"):
        return _stem(passage.get("source")) == _stem(desk_calc.RULES[task["rule"]]["file"])
    return bool(desk_calc.clause_text(passage, task["clause"]))


def _cite(passages: list, prefer=None) -> str:
    chosen = next((p for p in passages if p.get("n") and prefer and prefer(p)), None)
    chosen = chosen or next((p for p in passages if p.get("n")), None)
    return f" [{chosen['n']}]" if chosen else ""


def figure_text(result: dict) -> str:
    """A calculator's figure as the scripted answer writes it: Rs 2,40,000; 45 days; 4 December 2026; yes or no."""
    unit, value = result.get("unit"), result.get("value")
    if unit == "INR":
        return desk_calc.inr(value) if value is not None else "not payable on what the question states"
    if unit == "days":
        return f"{desk_calc.num(value)} days"
    if unit == "date":
        d = date.fromisoformat(str(value))
        return f"{d.day} {d:%B %Y}"
    if unit == "yes/no":
        return "yes, it must have one" if value else "no, it need not have one"
    return str(value)


def next_step(question: str, history: list[dict], task: dict | None, slip: bool = False) -> tuple[str, list[dict]]:
    """The scripted model's next message, (text, [{name, args}]), from the turn so far: {"role": "ai", "tools": [names]}
    and {"role": "tool", "name", "status", "content"} items, oldest first."""
    da = _da()
    asked = [n for h in history if h["role"] == "ai" for n in h["tools"]]
    results = [h for h in history if h["role"] == "tool"]
    passages = [p for h in results if h["name"] == "retrieve" and h["status"] != "error"
                for p in (_json(h["content"]) or {}).get("passages") or () if isinstance(p, dict)]
    if "retrieve" not in asked:
        return "", [{"name": "retrieve", "args": {"query": task["search"] if task else question}}]
    if task is None:
        return ("A scripted model: no row of the task set asks this question, so it searched once and works out no "
                "figure" + _cite(passages) + "."), []
    held = (lambda p: _holds(task, p))
    if task["kind"] == "lookup":
        want = Decimal(str(task["expected"])).normalize()
        for p in passages:
            if p.get("n") and _holds(task, p):              # its sentences, cut as documind_tools._snippet cuts them
                for piece in re.split(r"(?<=[.;])\s+|\n+(?=[^a-z\s])", str(p.get("text") or "")):
                    sentence = " ".join(piece.split())
                    if want in desk_calc.numbers_in(sentence):
                        return f"{sentence.rstrip('.;')} [{p['n']}].", []
        return "The passages I found do not give that figure" + _cite(passages) + ".", []
    calc = task["calcs"][-1]
    if slip:                                            # the figure written without a calculator call
        result = desk_calc.calculate(calc["calculator"], **calc["args"])
        return f"{da.LABELS[calc['calculator']]}: {figure_text(result)}{_cite(passages, held)}.", []
    for c in task["calcs"]:
        if c["calculator"] not in asked:
            return "", [{"name": c["calculator"], "args": dict(c["args"])}]
    done = [h for h in results if h["name"] == calc["calculator"]]
    if not done or done[-1]["status"] == "error":
        words = da.ARG_WORDS.get(task.get("missing") or "", "a number")
        return (f"I cannot work this figure out yet: the calculator needs {words}, which your question does not state. "
                f"Please tell me {words}" + _cite(passages, held) + "."), []
    body = _json(done[-1]["content"]) or {}
    found = " ".join(str(v) for v in (body.get("found") or {}).values())
    n = re.search(r"\[(\d+)\]", found)
    cite = f" [{n.group(1)}]" if n else _cite(passages, held)
    return f"{da.LABELS[calc['calculator']]}: {figure_text(body)}{cite}.", []


def plan_text(task: dict | None) -> str:
    """The plan the scripted model writes with its first call when its prompt opens with PLAN_FIRST: the steps its row
    needs, numbered."""
    if task is None:
        steps = ["Search for the passages that answer the question", "Answer from them"]
    elif task["kind"] == "lookup":
        steps = ["Search for the clause that states the figure", "Answer with the figure as the clause states it"]
    else:
        steps = (["Search for the passage the figure rests on"]
                 + [f"Call {c['calculator']} with numbers the question and that passage state" for c in task["calcs"]]
                 + ["Answer with the figure it returns, citing the passage"])
    return "Plan: " + " ".join(f"{i}. {s}." for i, s in enumerate(steps, 1))


_MARKS = re.compile(r"^(Question|Thought|Action|Observation|Final Answer):[ \t]?", re.M)


def _blocks(text: str) -> list[tuple[str, str]]:
    """A react_text transcript by its labels: [(label, text)], each text running to the next label."""
    marks = list(_MARKS.finditer(text))
    return [(m.group(1), text[m.end():marks[i + 1].start() if i + 1 < len(marks) else len(text)].strip())
            for i, m in enumerate(marks)]


def text_step(sent: str, task: dict | None, slip: bool = False, invents: str | None = None) -> str:
    """ScriptedTextModel's reply to the transcript it is sent: next_step()'s history, read back from the transcript's
    Action and Observation lines (an Action it cannot read is skipped with its Observation), and next_step()'s step
    written as Thought and Action, or Thought and Final Answer. With invents, the Action of the row's calculator runs
    on into an Observation of the script's own and a Final Answer from it."""
    da = _da()
    blocks = _blocks(sent)
    question = next((body for label, body in blocks if label == "Question"), "")
    history, pending = [], None
    for label, body in blocks:
        if label == "Action":
            m = re.fullmatch(r"([A-Za-z_]\w*)\s*\[\s*(\{.*\})\s*\]", body, re.S)
            pending = m.group(1) if m and isinstance(_json(m.group(2)), dict) else None
            if pending:
                history.append({"role": "ai", "tools": [pending]})
        elif label == "Observation" and pending:
            history.append({"role": "tool", "name": pending, "content": body,
                            "status": "success" if isinstance(_json(body), dict) else "error"})
            pending = None
    text, calls = next_step(question, history, task, slip)
    if not calls:
        last = next((h for h in reversed(history) if h["role"] == "tool"), None)
        thought = ("The calculator could not run on what the question states." if last and last["status"] == "error"
                   else "I have what the answer needs.")
        return f"Thought: {thought}\nFinal Answer: {text}"
    name, args = calls[0]["name"], calls[0]["args"]
    thought = ("I need the passage this rests on, so I search for it." if name == "retrieve" else
               f"{name} works the figure out from numbers the question and the passages state.")
    reply = f"Thought: {thought}\nAction: {name}[{json.dumps(args, ensure_ascii=False)}]"
    if invents and task and task.get("calcs") and name == task["calcs"][-1]["calculator"]:
        passages = [p for h in history if h["role"] == "tool" and h["name"] == "retrieve" and h["status"] != "error"
                    for p in (_json(h["content"]) or {}).get("passages") or () if isinstance(p, dict)]
        reply += (f"\n{STOP} {invents}\nThought: The calculator returned the figure.\n"
                  f"Final Answer: {da.LABELS.get(name, name)}: {invents}{_cite(passages, lambda p: _holds(task, p))}.")
    return reply


_SCRIPTED: list = []


def _scripted_class():
    if _SCRIPTED:
        return _SCRIPTED[0]
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from pydantic import ConfigDict, Field

    class ScriptedModel(BaseChatModel):
        """The offline model: next_step() for its task row, scripted token counts, every call's thinking level kept in
        `seen`. bind_tools binds the call's settings (thinking_level among them), as Gemini's does."""
        model_config = ConfigDict(arbitrary_types_allowed=True)
        model: str = "gemini-3.6-flash"
        thinking_level: str = "low"
        task: dict | None = None
        slip: bool = False
        seen: list = Field(default_factory=list)

        @property
        def _llm_type(self) -> str:
            return "scripted"

        def bind_tools(self, tools, tool_choice=None, **kw):
            return self.bind(**kw)

        def _generate(self, messages, stop=None, run_manager=None, **kw):
            level = kw.get("thinking_level") or self.thinking_level
            self.seen.append(kw.get("thinking_level"))
            question = next((str(m.content) for m in messages if m.type == "human"), "")
            history, chars = [], 0
            for m in messages:
                content = m.content if isinstance(m.content, str) else json.dumps(m.content)
                chars += len(content)
                if m.type == "ai":
                    history.append({"role": "ai", "tools": [tc["name"] for tc in m.tool_calls or ()]})
                    chars += sum(len(tc["name"]) + len(json.dumps(tc["args"])) for tc in m.tool_calls or ())
                elif m.type == "tool":
                    history.append({"role": "tool", "name": m.name, "status": m.status, "content": content})
            text, calls = next_step(question, history, self.task, self.slip)
            if not history and any(m.type == "system" and PLAN_FIRST in str(m.content) for m in messages):
                text = "\n".join(t for t in (plan_text(self.task), text) if t)      # plan_first: the plan comes first
            msg = AIMessage(content=text, usage_metadata=scripted_usage(chars, text, calls, level),
                            tool_calls=[{"name": c["name"], "args": c["args"], "id": f"scripted-{len(history)}-{i}",
                                         "type": "tool_call"} for i, c in enumerate(calls)])
            return ChatResult(generations=[ChatGeneration(message=msg)])

    _SCRIPTED.append(ScriptedModel)
    return ScriptedModel


_SCRIPTED_TEXT: list = []


def _scripted_text_class():
    if _SCRIPTED_TEXT:
        return _SCRIPTED_TEXT[0]
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from pydantic import ConfigDict, Field

    class ScriptedTextModel(BaseChatModel):
        """react_text's offline model, a model with no function calling: it takes no tools (BaseChatModel.bind_tools
        raises), and each reply is text_step() for its task row, or the next of `replies` (the last again once they
        run out). It honours a stop sequence as Gemini does: the reply ends before the first one, which is not
        included. honours_stop=False plays an endpoint that does not. Per call it keeps the thinking level sent
        (`seen`), the stop sequences (`stops`), the names of the other settings sent (`settings`: a function
        declaration would be "tools"), the system prompt (`system`) and the transcript it was sent (`sent`)."""
        model_config = ConfigDict(arbitrary_types_allowed=True)
        model: str = "gemini-3.6-flash"
        thinking_level: str = "low"
        task: dict | None = None
        slip: bool = False
        invents: str | None = None
        honours_stop: bool = True
        replies: list | None = None
        seen: list = Field(default_factory=list)
        stops: list = Field(default_factory=list)
        settings: list = Field(default_factory=list)
        system: list = Field(default_factory=list)
        sent: list = Field(default_factory=list)

        @property
        def _llm_type(self) -> str:
            return "scripted-text"

        def _generate(self, messages, stop=None, run_manager=None, **kw):
            level = kw.get("thinking_level") or self.thinking_level
            self.seen.append(kw.get("thinking_level"))
            self.stops.append(list(stop or ()))
            self.settings.append(sorted(k for k in kw if k != "thinking_level"))
            self.system.append(next((str(m.content) for m in messages if m.type == "system"), ""))
            said = next((str(m.content) for m in reversed(messages) if m.type == "human"), "")
            self.sent.append(said)
            chars = sum(len(m.content if isinstance(m.content, str) else json.dumps(m.content)) for m in messages)
            if self.replies is not None:
                text = self.replies[min(len(self.sent), len(self.replies)) - 1]
            else:
                text = text_step(said, self.task, self.slip, self.invents)
            if self.honours_stop:
                cut = min((text.find(s) for s in stop or () if s in text), default=len(text))
                text = text[:cut]
            msg = AIMessage(content=text, usage_metadata=scripted_usage(chars, text, [], level))
            return ChatResult(generations=[ChatGeneration(message=msg)])

    _SCRIPTED_TEXT.append(ScriptedTextModel)
    return ScriptedTextModel


def scripted(question: str, tenant: str = "acme", run: int = 0, task: dict | None = None, slips_on: bool = False,
             pattern: str = "loop", invents: str | None = None):
    """The OFFLINE model for one turn of `pattern`: the row asking `question` (or `task`), at the desk agent's own
    thinking level. slips_on lets it write a figure itself on the runs slips() names; a single turn leaves it off. A
    pattern whose model writes text (react_text) gets ScriptedTextModel. invents, for react_text only, is the
    observation that model writes itself past its calculator's Action, as a model does whose stop sequence does not
    hold (lesson 10.1's Change-it), so its stop is not honoured: only the parser's cut keeps the invention out."""
    da = _da()
    task = task if task is not None else task_for(question, tenant)
    slip = bool(task) and slips_on and slips(task, run)
    if pattern in PATTERNS and PATTERNS[pattern].text:
        return _scripted_text_class()(model=da.AGENT_MODEL, thinking_level=da.THINKING_LEVEL, task=task, slip=slip,
                                      invents=invents, honours_stop=invents is None)
    if invents is not None:
        raise ValueError(f"invents is react_text's: the {pattern} pattern's model calls its tools natively")
    return _scripted_class()(model=da.AGENT_MODEL, thinking_level=da.THINKING_LEVEL, task=task, slip=slip)
