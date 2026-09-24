"""Lesson 11.1 / s3: One turn, taken apart

Summary and purpose:
Do it: one turn

HTML instruction: bash — run in the operator shell, in the kit (one turn taken apart; no model, no network beyond your machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_venv
Expected observation: 1. turn 1, the LangChain brain, thread acme:you@example.com:lesson111
   kept  HumanMessage What is the notice period?
   kept  AIMessage    retrieve(...)
   kept  ToolMessage  {"citations": [{"chunk_id": "acme:hr_policy_2026#NP-03", "quote"
   kept  AIMessage    Sixty days [1].
   the system prompt among them: False; checkpoints written: 5
2. turn 2, the LangGraph brain, the same thread: 6 messages, turn 1's among them
   the history still quotes: The notice period is 60 days.
   the corpus now says:      The notice period is 90 days.
3. a new session, the same person: 0 messages

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html#L412

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import json, logging, sys, threading, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path[:0] = [".", "services/chat"]
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
import shared.documind_tools as dt
import brains
CORPUS = {"NP-03": "The notice period is 60 days."}   # what a stand-in rag-api's corpus says today
class Api(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        body = {"answerable": True, "confidence": "high",
                "citations": [{"chunk_id": "acme:hr_policy_2026#NP-03", "quote": CORPUS["NP-03"], "score": 0.9}]}
        self.send_response(200); self.end_headers(); self.wfile.write(json.dumps(body).encode())
srv = ThreadingHTTPServer(("127.0.0.1", 0), Api)
threading.Thread(target=srv.serve_forever, daemon=True).start()
dt.RAG_API_URL, dt._id_token = f"http://127.0.0.1:{srv.server_address[1]}", lambda aud: "TOKEN"
class Script(FakeMessagesListChatModel):           # a model that says what it is told
    def bind_tools(self, tools, **kw): return self
saver = InMemorySaver()                            # one checkpointer for both brains, as in the chat service
thread = {"configurable": {"thread_id": "acme:you@example.com:lesson111"}}   # agent.thread_config's shape
ctx = {"tenant_id": "acme", "user_id": "you@example.com", "assertion": ""}
lc = brains.LangChainBrain(saver, llm=Script(responses=[
    AIMessage("", tool_calls=[{"name": "retrieve", "args": {"query": "notice period"}, "id": "c1"}]), AIMessage("Sixty days [1].")]))
lc.answer("What is the notice period?", config=thread, context={**ctx, "brain": "langchain"})
kept = lc.agent.get_state(thread).values["messages"]
print("1. turn 1, the LangChain brain, thread", thread["configurable"]["thread_id"])
for m in kept:
    what = m.tool_calls[0]["name"] + "(...)" if getattr(m, "tool_calls", None) else str(m.content)[:64]
    print(f"   kept  {type(m).__name__:12} {what}")
print(f"   the system prompt among them: {any(type(m).__name__ == 'SystemMessage' for m in kept)};"
      f" checkpoints written: {len(list(saver.list(thread)))}")
CORPUS["NP-03"] = "The notice period is 90 days."    # the corpus changes: lesson 9.2's second handbook
lg = brains.LangGraphBrain(saver, llm=Script(responses=[AIMessage("(the model answers)")]))
lg.answer("And what was the answer?", config=thread, context={**ctx, "brain": "langgraph"})
kept = lg.graph.get_state(thread).values["messages"]
print(f"2. turn 2, the LangGraph brain, the same thread: {len(kept)} messages, turn 1's among them")
print("   the history still quotes:", [json.loads(m.content)["citations"][0]["quote"] for m in kept if isinstance(m, ToolMessage)][0])
print("   the corpus now says:     ", dt.retrieve("notice period", tenant_id="acme")["citations"][0]["quote"])
other = {"configurable": {"thread_id": "acme:you@example.com:lesson111-b"}}
print(f"3. a new session, the same person: {len(lc.agent.get_state(other).values.get('messages', []))} messages")
srv.shutdown()
PY
"""


def demonstrate(session):
    """Run Do it: one turn at this checkpoint.

    Do it: one turn

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one turn taken apart; no model, no network beyond your machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
