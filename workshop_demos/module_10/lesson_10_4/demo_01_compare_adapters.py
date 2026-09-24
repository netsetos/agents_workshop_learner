"""Lesson 10.4: demo 01 compare adapters

Run the LangChain and ADK adapters over the same tool contract.

Run order inside this file:
1. Do it: side by side (source window 12)

Prerequisites: setup_prepare.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_side_by_side.
COMMANDS_01 = """~/graph-venv/bin/python - <<'PY'
import json, logging, sys, textwrap, threading, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)   # the frameworks' notices; lesson 10.3 read the logs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path[:0] = [".", "services/chat"]
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.tools import FunctionTool
from google.genai import types as gt
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.utils.function_calling import convert_to_openai_tool
from langgraph.checkpoint.memory import InMemorySaver
import shared.documind_tools as dt
import tools, brains
SEEN = []
class Api(BaseHTTPRequestHandler):                 # a stand-in rag-api: it notes what it was sent, and answers
    def log_message(self, *a): pass
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append((req["tenant_id"], req.get("brain"), self.headers.get(dt.ASSERTION_HEADER)))
        body = {"answer": "Payable after five years [1].", "answerable": True, "confidence": "high",
                "citations": [{"chunk_id": "acme:gratuity#4", "quote": "not less than five years", "score": 0.9}]}
        self.send_response(200); self.end_headers(); self.wfile.write(json.dumps(body).encode())
srv = ThreadingHTTPServer(("127.0.0.1", 0), Api)
threading.Thread(target=srv.serve_forever, daemon=True).start()
dt.RAG_API_URL, dt._id_token = f"http://127.0.0.1:{srv.server_address[1]}", lambda aud: "TOKEN"
class Script(FakeMessagesListChatModel):           # a LangChain model that says what it is told
    def bind_tools(self, tools, **kw): return self
class AdkScript(BaseLlm):                          # the same for ADK, and it keeps what it was sent
    model: str = "script"
    turns: list = []
    sent: list = []
    async def generate_content_async(self, llm_request, stream=False):
        self.sent.append(llm_request); yield self.turns.pop(0)
def said(text=None, **call):
    part = gt.Part(text=text) if text else gt.Part(function_call=gt.FunctionCall(**call))
    return LlmResponse(content=gt.Content(role="model", parts=[part]))
ctx, adk = {"tenant_id": "acme", "user_id": "you", "assertion": ""}, brains.AdkBrain(None)
def lc(label, name, args):                         # one tool call through the LangChain brain: refusals, status, what it read
    b = brains.LangChainBrain(InMemorySaver(), llm=Script(responses=[
        AIMessage("", tool_calls=[{"name": name, "args": args, "id": "c1"}]), AIMessage("(the model explains)")]))
    cfg = {"configurable": {"thread_id": "acme:you:lc" + label}}
    out = b.answer("...", config=cfg, context={**ctx, "brain": "langchain"})
    res = [m for m in b.agent.get_state(cfg).values["messages"] if isinstance(m, ToolMessage)][0]
    return out["refusals"], res.status, res.content
def ak(label, name, args):                         # the same through the ADK brain
    adk.runner.agent.model = model = AdkScript(turns=[said(name=name, args=args), said("(the model explains)")], sent=[])
    try:
        out = adk.answer("...", config={"configurable": {"thread_id": "acme:you:ak" + label}}, context={**ctx, "brain": "adk"})
    except Exception as e:
        return None, "raises", f"{type(e).__name__}: {str(e).splitlines()[0]}"
    read = [p.function_response.response for c in model.sent[-1].contents for p in c.parts or [] if p.function_response]
    return out["refusals"], "success", json.dumps(read[0])
print("1. what each model is shown for retrieve (* = required)")
shown = {"langchain": convert_to_openai_tool(tools.retrieve)["function"],
         "adk": FunctionTool(dt.retrieve)._get_declaration().model_dump(mode="json", exclude_none=True)}
for name, d in shown.items():
    schema = d.get("parameters") or d["parameters_json_schema"]
    params = [p + ("*" if p in schema.get("required", []) else "") for p in schema["properties"]]
    print(f"   {name:9} {', '.join(params):54} {len(json.dumps(d)):,} characters")
print(f"   langchain tools: {', '.join(t.name for t in tools.TOOLS)}")
print(f"   adk tools:       {', '.join(t.name for t in adk.runner.agent.tools)}")
print('2. one retrieve(); the ADK model writes tenant_id "globex" and assertion "anything"')
for name, run, args in (("langchain", lc, {"query": "gratuity"}),
                        ("adk", ak, {"query": "gratuity", "tenant_id": "globex", "assertion": "anything"})):
    refusals, status, text = run("r", "retrieve", args)
    tenant, brain, assertion = SEEN[-1]
    print(f"   {name:9} rag-api got tenant {tenant}, brain {brain}, assertion header {assertion!r}")
    print(f"             the model read: {', '.join(json.loads(text))}")
print("3. three calls that go wrong")
for i, (call, name, args) in enumerate((('delete_document(doc="x")', "delete_document", {"doc": "x"}),
        ('calculate_processing_cost(total_pages="many")', "calculate_processing_cost", {"total_pages": "many"}),
        ('calculate_processing_cost(total_pages=10, processing_type="express")', "calculate_processing_cost",
         {"total_pages": 10, "processing_type": "express"}))):
    print("   " + call)
    for brain, run in (("langchain", lc), ("adk", ak)):
        refusals, status, text = run(str(i), name, args)
        said_ = f"the turn raises {text}" if status == "raises" else f"[{status}] {text}"
        print(f"     {brain:9} " + "\\n               ".join(textwrap.wrap(textwrap.shorten(said_, 150), 76)))
        if status != "raises":
            print(f"               refusals {refusals}")
print(f"4. ADK's sessions with no CHECKPOINT_DSN: {type(adk.svc).__name__}, at most {adk.run_config.max_llm_calls} model calls a turn")
srv.shutdown()
PY

"""

def step_01_side_by_side(session):
    """Run Do it: side by side at this checkpoint.

    Do it: side by side

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the two adapters side by side; no model, no network beyond your machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_12', step_01_side_by_side),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
