"""Lesson 11.2 / s3: What a turn writes

Summary and purpose:
Do it: two turns

HTML instruction: bash — run in the operator shell, in the kit (two turns, their checkpoints and versions counted; no model, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_venv
Expected observation: a turn with no tool   +3 checkpoints, +2 versions of messages
a turn with retrieve  +5 checkpoints, +4 versions of messages
the messages channel, every version kept:
   version 1  1 message      211 bytes
   version 2  2 messages     472 bytes
   version 3  3 messages     687 bytes
   version 4  4 messages   1,001 bytes
   version 5  5 messages   2,720 bytes
   version 6  6 messages   2,981 bytes
   8,072 bytes kept, for a conversation whose latest version is 2,981 bytes
the ADK brain, given the lane's DSN, with google-adk and no SQLAlchemy - as the chat image has them:
WARNING documind.chat.brains: ADK DatabaseSessionService unavailable (The 'sqlalchemy' package is required to use this feature. Please install it by running: pip install google-adk[db]); using memory
   it keeps its sessions in InMemorySessionService

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.2-durable-storage/Netsetos_GCP_Capstone_11.2_Durable_Storage_WIX.html#L408

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import logging, os, sys, warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s", stream=sys.stdout)
sys.path[:0] = [".", "services/chat"]
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
import shared.documind_tools as dt
import brains
QUOTE = ("Gratuity shall be payable to an employee on the termination of his employment after he has rendered "
         "continuous service for not less than five years, on his superannuation, or on his retirement or resignation.")
dt.retrieve = lambda query, **kw: {"answerable": True, "confidence": "high", "citations": [   # five passages, no network
    {"chunk_id": f"acme:payment_of_gratuity_act_1972#{4 + i}", "quote": QUOTE, "score": 0.9} for i in range(5)]}
class Script(FakeMessagesListChatModel):           # a model that says what it is told
    def bind_tools(self, tools, **kw): return self
saver = InMemorySaver()                            # PostgresSaver's interface: a row per checkpoint, a blob per new version
thread = {"configurable": {"thread_id": "acme:you@example.com:lesson112"}}
def turn(question, tool):                          # one turn of the kit's LangChain brain, with or without retrieve
    said = [AIMessage("", tool_calls=[{"name": "retrieve", "args": {"query": question}, "id": "c1"}])] if tool else []
    brains.LangChainBrain(saver, llm=Script(responses=said + [AIMessage("Five years of continuous service [1].")])).answer(
        question, config=thread, context={"tenant_id": "acme", "brain": "langchain"})
def kept():                                        # the thread's checkpoints, and each version of messages they stored
    cps, versions = list(saver.list(thread))[::-1], {}
    for c in cps:
        v = c.checkpoint["channel_versions"].get("messages")
        if v and v not in versions:
            msgs = c.checkpoint["channel_values"]["messages"]
            versions[v] = (len(msgs), len(saver.serde.dumps_typed(msgs)[1]))
    return cps, versions
done = (0, 0)
for question, tool in (("Remember this word for me: tamarind.", False), ("After how many years is gratuity payable?", True)):
    turn(question, tool)
    cps, versions = kept()
    print(f"a turn {'with retrieve' if tool else 'with no tool':14} +{len(cps) - done[0]} checkpoints, +{len(versions) - done[1]} versions of messages")
    done = (len(cps), len(versions))
print("the messages channel, every version kept:")
for i, (n, size) in enumerate(versions.values(), 1):
    print(f"   version {i}  {n} message{'s' if n > 1 else ' '}  {size:>6,} bytes")
sizes = [size for _, size in versions.values()]
print(f"   {sum(sizes):,} bytes kept, for a conversation whose latest version is {sizes[-1]:,} bytes")
print("the ADK brain, given the lane's DSN, with google-adk and no SQLAlchemy - as the chat image has them:")
os.environ["CHECKPOINT_DSN"] = "postgresql://chat:PASSWORD@/documind?host=/cloudsql/PROJECT:REGION:documind-checkpoint"
print(f"   it keeps its sessions in {type(brains.AdkBrain._sessions()).__name__}")
PY
"""


def demonstrate(session):
    """Run Do it: two turns at this checkpoint.

    Do it: two turns

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two turns, their checkpoints and versions counted; no model, no network).
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
