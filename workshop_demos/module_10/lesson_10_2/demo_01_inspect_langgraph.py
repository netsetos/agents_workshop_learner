"""Lesson 10.2: demo 01 inspect langgraph

Build and inspect the graph in its isolated framework environment.

Run order inside this file:
1. Do it: the graph (source window 9)

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


# Original CLI workflow for step_01_the_graph.
COMMANDS_01 = """~/graph-venv/bin/python - <<'PY'
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

def step_01_the_graph(session):
    """Run Do it: the graph at this checkpoint.

    Do it: the graph

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's graph, built and listed; no network, no model).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_the_graph),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
