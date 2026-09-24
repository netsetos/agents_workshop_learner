"""Lesson 10.3 / s3: Five failures through the kit's LangChain brain

Summary and purpose:
Do it: five failures

HTML instruction: bash — run in the operator shell, in the kit (five failures through the kit's LangChain brain; no model, no network beyond your machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_venv
Expected observation: blocked     0.0 s  refusals ['delete_document']
              result [error] {"error": "delete_document requires manual approval"}
  bad args    0.0 s  refusals ['calculate_processing_cost']
              result [error] Error invoking tool 'calculate_processing_cost' with kwargs {'total_page
  no such     0.0 s  refusals ['summon_rain']
              result [error] Error: summon_rain is not a valid tool, try one of [retrieve, calculate_
  timed out   0.5 s  refusals []
              result [success] {"error": "document search is unavailable", "citations": [], "answerable
  over budget 0.0 s  refusals []
              result [success] {"num_documents": 1, "total_pages": 283, "processing_type": "priority", 
  the log lines, from the guard, the adapter and the one retrieve():
    WARNING refused delete_document (blocked list)
    INFO    calculate_processing_cost took 0.00s (budget 10s)
   

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.3-tool-failures/Netsetos_GCP_Capstone_10.3_Tool_Failures_WIX.html#L438

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import io, logging, sys, threading, time, warnings
warnings.filterwarnings("ignore")                  # the framework warns about a dict context; harmless
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path[:0] = [".", "services/chat"]
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
import shared.documind_tools as dt
import tools, brains
class Slow(BaseHTTPRequestHandler):                # a rag-api that answers after two seconds
    def log_message(self, *a): pass
    def do_POST(self):
        time.sleep(2); self.send_response(200); self.end_headers(); self.wfile.write(b"{}")
srv = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
threading.Thread(target=srv.serve_forever, daemon=True).start()
dt.RAG_API_URL, dt.RAG_TIMEOUT_S, dt._id_token = f"http://127.0.0.1:{srv.server_address[1]}", 0.5, lambda aud: "TOKEN"
log = io.StringIO()
for name in ("documind.chat.brains", "documind.chat.tools", "documind.agents.tools"):
    h = logging.StreamHandler(log); h.setFormatter(logging.Formatter("%(levelname)-7s %(message)s"))
    logging.getLogger(name).addHandler(h); logging.getLogger(name).setLevel(logging.INFO)
class Scripted(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kw): return self
def run(label, name, **args):
    turns = [AIMessage("", tool_calls=[{"name": name, "args": args, "id": "c1"}]), AIMessage("(the model explains what it read)")]
    b = brains.LangChainBrain(InMemorySaver(), llm=Scripted(responses=turns))
    cfg = {"configurable": {"thread_id": "acme:you:" + label}}
    t = time.time()
    out = b.answer("...", config=cfg, context={"tenant_id": "acme", "brain": "langchain"})
    res = [m for m in b.agent.get_state(cfg).values["messages"] if isinstance(m, ToolMessage)][0]
    print(f"  {label:11} {time.time() - t:3.1f} s  refusals {out['refusals']}")
    print(f"              result [{res.status}] {str(res.content)[:72]}")
run("blocked", "delete_document", doc="inv_2026_0412")
run("bad args", "calculate_processing_cost", total_pages="many")
run("no such", "summon_rain")
run("timed out", "retrieve", query="gratuity")
tools.TIMEOUTS["calculate_processing_cost"] = 0    # a budget of zero seconds: every call is over it
run("over budget", "calculate_processing_cost", total_pages=283, processing_type="priority")
srv.shutdown()
print("  the log lines, from the guard, the adapter and the one retrieve():")
for line in log.getvalue().splitlines():
    print("   ", line[:92])
PY
"""


def demonstrate(session):
    """Run Do it: five failures at this checkpoint.

    Do it: five failures

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (five failures through the kit's LangChain brain; no model, no network beyond your machine).
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
