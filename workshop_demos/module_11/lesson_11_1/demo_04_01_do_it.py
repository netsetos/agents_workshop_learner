"""Lesson 11.1 / s4: The memory checkpointer, and the line it logs

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the chat service's checkpointer with CHECKPOINT_DSN=memory, then a restart)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_one_turn
Expected observation: 1. the chat service's own checkpointer, with CHECKPOINT_DSN=memory
WARNING documind.chat.agent: CHECKPOINT_DSN=memory: conversations die with the instance (8.5). Tests only - never a deployment.
   InMemorySaver: 2 messages in acme:you@example.com:lesson111
WARNING documind.chat.agent: CHECKPOINT_DSN=memory: conversations die with the instance (8.5). Tests only - never a deployment.
   after a restart: 0 messages
2. the laptop lane's SqliteSaver, a file (agent.py's DOCUMIND_PROFILE=local branch)
   after a restart: 2 messages

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html#L502

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the chat service's checkpointer with CHECKPOINT_DSN=memory, then a restart).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
