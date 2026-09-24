"""Lesson 10.2 / s3: The graph, in a venv of its own

Summary and purpose:
Do it: the graph

HTML instruction: bash — run in the operator shell, in the kit (the kit's graph, built and listed; no network, no model)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_venv
Expected observation: nodes: __start__, agent, tools, refuse, __end__
  __start__ -> agent    
      agent -> __end__    (route decides)
      agent -> refuse     (route decides)
      agent -> tools      (route decides)
     refuse -> agent    
      tools -> agent

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.2-langgraph/Netsetos_GCP_Capstone_10.2_LangGraph_WIX.html#L412

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import sys, warnings
warnings.filterwarnings("ignore")                 # the framework warns about a dict context; harmless
sys.path[:0] = [".", "services/chat"]
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
import brains
class Scripted(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kw):            # the graph binds the kit's tools; a scripted model ignores them
        return self
g = brains.LangGraphBrain(InMemorySaver(), llm=Scripted(responses=[AIMessage("")])).graph.get_graph()
print("  nodes:", ", ".join(g.nodes))
for e in sorted(g.edges, key=lambda e: (e.source, e.target)):
    print(f"  {e.source:>9} -> {e.target:<9}{'  (route decides)' if e.conditional else ''}")
PY
"""


def demonstrate(session):
    """Run Do it: the graph at this checkpoint.

    Do it: the graph

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's graph, built and listed; no network, no model).
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
