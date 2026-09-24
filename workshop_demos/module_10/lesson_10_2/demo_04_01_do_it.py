"""Lesson 10.2 / s4: The refuse node, forced to fire

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (three scripted turns through the kit's own graph; no network, no model)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_the_graph
Expected observation: plain    agent -> tools -> agent          tool_calls ['retrieve']  refusals []
           answer: After five years of continuous service [1].
  blocked  agent -> refuse -> agent         tool_calls ['delete_document']  refusals ['delete_document']
           error result for delete_document: {"error": "delete_document requires manual approval"}
           answer: I could not delete the invoice: deleting a document requires manual approval, so
  mixed    agent -> refuse -> agent         tool_calls ['retrieve', 'delete_document']  refusals ['retrieve', 'delete_document']
           error result for retrieve: {"error": "retrieve requires manual approval"}
           error result for delete_document: {"error": "delete_document requires manual approval"}
           answer: Nothing was done: that request needs manual approval.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.2-langgraph/Netsetos_GCP_Capstone_10.2_LangGraph_WIX.html#L473

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import sys, warnings
warnings.filterwarnings("ignore")
sys.path[:0] = [".", "services/chat"]
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
import shared.documind_tools as dt
dt.retrieve = lambda *a, **k: {"citations": [{"chunk_id": "acme:SHA#12", "quote": "not less than five years"}], "answerable": True, "confidence": "high"}
import brains
class Scripted(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kw):
        return self
def run(label, turns):
    b = brains.LangGraphBrain(InMemorySaver(), llm=Scripted(responses=turns))
    cfg = {"configurable": {"thread_id": "acme:you:" + label}}
    path = [list(u)[0] for u in b.graph.stream({"messages": [{"role": "user", "content": "..."}]}, cfg, context={"tenant_id": "acme"}, stream_mode="updates")]
    msgs = b.graph.get_state(cfg).values["messages"]
    out = brains._summary(msgs)
    print(f"  {label:8} {' -> '.join(path):32} tool_calls {out['tool_calls']}  refusals {out['refusals']}")
    for m in msgs:
        if isinstance(m, ToolMessage) and m.status == "error":
            print(f"           error result for {m.name}: {m.content}")
    print(f"           answer: {out['answer'][:80]}")
call = lambda name, i, **a: {"name": name, "args": a, "id": f"c{i}"}
run("plain", [AIMessage("", tool_calls=[call("retrieve", 1, query="gratuity continuous service")]), AIMessage("After five years of continuous service [1].")])
run("blocked", [AIMessage("", tool_calls=[call("delete_document", 1, doc="inv_2026_0412")]),
                AIMessage("I could not delete the invoice: deleting a document requires manual approval, so nothing was removed.")])
run("mixed", [AIMessage("", tool_calls=[call("retrieve", 1, query="April invoice"), call("delete_document", 2, doc="inv_2026_0412")]),
              AIMessage("Nothing was done: that request needs manual approval.")])
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three scripted turns through the kit's own graph; no network, no model).
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
