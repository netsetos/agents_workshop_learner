"""Lesson 11.3 / s3: Isolation, on the kit's own app

Summary and purpose:
Do it: eight callers

HTML instruction: bash — run in the operator shell, in the kit (the kit's chat app on your machine; no model, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_venv
Expected observation: alice gives the word, lesson113        200  Got it: saffron.
  alice asks for it                      200  You asked me to remember saffron.
  alice, a new session                   200  I have no word from you in this conversation.
  bob, her tenant, same session name     200  I have no word from you in this conversation.
  carol, another tenant, the same name   200  I have no word from you in this conversation.
  alice, the body naming zeta            200  You asked me to remember saffron.
  alice, a session id with a colon       422  String should match pattern '^[A-Za-z0-9_-]{1,64}$'
  the outsider                           403  not a member of any tenant
  a token that names nobody              401  the bearer token carries no verified email
  the threads the checkpointer holds:
    acme:alice@acme.example:lesson113
    acme:alice@acme.example:lesson113-b
    acme:bob@acme.example:l

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.3-restart-isolation/Netsetos_GCP_Capstone_11.3_Restart_Isolation_WIX.html#L423

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
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


def demonstrate(session):
    """Run Do it: eight callers at this checkpoint.

    Do it: eight callers

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's chat app on your machine; no model, no network).
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
