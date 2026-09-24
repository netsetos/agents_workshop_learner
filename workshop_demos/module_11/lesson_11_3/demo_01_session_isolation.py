"""Lesson 11.3: demo 01 session isolation

Exercise eight callers against the kit's own session-isolation implementation.

Run order inside this file:
1. Do it: eight callers (source window 11)

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


# Original CLI workflow for step_01_eight_callers.
COMMANDS_01 = """~/graph-venv/bin/python - <<'PY'
import logging, os, sys, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
os.environ.update(CHECKPOINT_DSN="memory", SELF_URL="https://documind-chat.example")   # the app's own start-up, in memory
sys.path[:0] = [".", "services/chat"]
from fastapi.testclient import TestClient
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from shared import iap
import agent, brains
class Recall(BaseChatModel):                       # a model that can answer only from the history it is sent
    @property
    def _llm_type(self): return "recall"
    def bind_tools(self, tools, **kw): return self
    def _generate(self, messages, stop=None, run_manager=None, **kw):
        asked = [str(m.content) for m in messages if m.type == "human"]
        text = ("Got it: saffron." if "Remember" in asked[-1] else "You asked me to remember saffron."
                if any("saffron" in a for a in asked[:-1]) else "I have no word from you in this conversation.")
        return ChatResult(generations=[ChatGeneration(message=AIMessage(text))])
PEOPLE = {"alice": ("alice@acme.example", "acme"), "bob": ("bob@acme.example", "acme"),
          "carol": ("carol@zeta.example", "zeta"), "outsider": ("outsider@example.com", None)}
def identity(headers, bearer_audience=None):       # stands in for the token check: the bearer names the person
    who = headers.get("authorization", "").removeprefix("Bearer ")
    if who not in PEOPLE:
        raise iap.IapError("the bearer token carries no verified email")
    return {"email": PEOPLE[who][0], "via": "iam", "aud": bearer_audience}
iap.identity, brains.build_llm = identity, Recall
agent.tenant_for = lambda email: next((t for e, t in PEOPLE.values() if e == email), None)   # stands in for the roster
def ask(c, who, question, session="lesson113", **extra):
    r = c.post("/v1/chat", headers={"Authorization": f"Bearer {who}"},
               json={"question": question, "session_id": session, "brain": "langchain", **extra})
    said = r.json().get("answer") or r.json().get("detail")
    return f"{r.status_code}  {said[0]['msg'] if isinstance(said, list) else said}"
WORD, ASK = "Remember this word for me: saffron.", "Which word did I ask you to remember?"
with TestClient(agent.app) as c:                   # one instance of the kit's chat service
    print(f"  alice gives the word, lesson113        {ask(c, 'alice', WORD)}")
    print(f"  alice asks for it                      {ask(c, 'alice', ASK)}")
    print(f"  alice, a new session                   {ask(c, 'alice', ASK, session='lesson113-b')}")
    print(f"  bob, her tenant, same session name     {ask(c, 'bob', ASK)}")
    print(f"  carol, another tenant, the same name   {ask(c, 'carol', ASK)}")
    print(f"  alice, the body naming zeta            {ask(c, 'alice', ASK, tenant_id='zeta')}")
    print(f"  alice, a session id with a colon       {ask(c, 'alice', ASK, session='lesson113:x')}")
    print(f"  the outsider                           {ask(c, 'outsider', ASK)}")
    print(f"  a token that names nobody              {ask(c, 'nobody', ASK)}")
    print("  the threads the checkpointer holds:")
    for t in sorted({t.config["configurable"]["thread_id"] for t in agent.app.state.checkpointer.list(None)}):
        print("    " + t)
with TestClient(agent.app) as c:                   # a restart: the lifespan builds a new checkpointer
    print(f"  after a restart, alice asks again      {ask(c, 'alice', ASK)}")
PY

"""

def step_01_eight_callers(session):
    """Run Do it: eight callers at this checkpoint.

    Do it: eight callers

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's chat app on your machine; no model, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_11', step_01_eight_callers),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
