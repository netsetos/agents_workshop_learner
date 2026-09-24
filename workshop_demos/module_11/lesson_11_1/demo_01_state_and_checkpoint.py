"""Lesson 11.1: demo 01 state and checkpoint

Take apart one turn and inspect the memory-checkpointer record.

Run order inside this file:
1. Do it: one turn (source window 10)
2. Do it (source window 13)

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


# Original CLI workflow for step_01_one_turn.
COMMANDS_01 = """~/graph-venv/bin/python - <<'PY'
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

def step_01_one_turn(session):
    """Run Do it: one turn at this checkpoint.

    Do it: one turn

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one turn taken apart; no model, no network beyond your machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """~/graph-venv/bin/python - <<'PY'
import logging, os, sys, tempfile, warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s", stream=sys.stdout)
os.environ["CHECKPOINT_DSN"] = "memory"            # agent.py reads it at import, as the service does at start-up
sys.path[:0] = [".", "services/chat"]
from contextlib import ExitStack
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import agent, brains
class Script(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kw): return self
thread = agent.thread_config("acme", "you@example.com", "lesson111")
def talk(saver):                                   # one turn, no tool: a word to remember
    b = brains.LangChainBrain(saver, llm=Script(responses=[AIMessage("Got it: tamarind.")]))
    b.answer("Remember this word for me: tamarind.", config=thread, context={"tenant_id": "acme", "brain": "langchain"})
def held(saver):                                   # what the next turn would find in this thread
    return len(brains.LangChainBrain(saver, llm=Script(responses=[])).agent.get_state(thread).values.get("messages", []))
print("1. the chat service's own checkpointer, with CHECKPOINT_DSN=memory")
with ExitStack() as stack:
    saver = agent.build_checkpointer(stack)
    talk(saver)
    print(f"   {type(saver).__name__}: {held(saver)} messages in {thread['configurable']['thread_id']}")
with ExitStack() as stack:                         # a restart: the new instance builds its own checkpointer
    print(f"   after a restart: {held(agent.build_checkpointer(stack))} messages")
print("2. the laptop lane's SqliteSaver, a file (agent.py's DOCUMIND_PROFILE=local branch)")
path = os.path.join(tempfile.mkdtemp(), "threads.db")
with SqliteSaver.from_conn_string(path) as saver:
    talk(saver)
with SqliteSaver.from_conn_string(path) as saver:  # the process restarts, and opens the same file
    print(f"   after a restart: {held(saver)} messages")
PY

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the chat service's checkpointer with CHECKPOINT_DSN=memory, then a restart).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_one_turn),
        ('source_13', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
