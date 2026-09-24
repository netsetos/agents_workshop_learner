"""Lesson 10.4 / s6: The half the rows cannot see

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: langchain 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  langgraph 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  adk       2 model calls  in  2,477  out    47 (thinking     0)  Rs 0.3458
the four cost lines, whole: the brain's own model calls + rag-api's, from step 5
  direct    Rs 0.0000 + Rs 0.3699 = Rs 0.3699
  langchain Rs 0.2147 + Rs 0.3593 = Rs 0.5740
  langgraph Rs 0.2147 + Rs 0.3613 = Rs 0.5760
  adk       Rs 0.3458 + Rs 0.3687 = Rs 0.7145

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.4-adapters/Netsetos_GCP_Capstone_10.4_Adapters_WIX.html#L655

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """GOOGLE_CLOUD_PROJECT="$PROJECT" RAG_API_URL="$API" RAG_TIMEOUT_S=90 \\
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" ~/graph-venv/bin/python - <<'PY'
import asyncio, json, logging, os, sys, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
sys.path[:0] = [".", "services/chat"]
from langgraph.checkpoint.memory import InMemorySaver
import brains
Q = "After how many years of continuous service does gratuity become payable?"
IN, OUT = 1.50, 7.50                               # cost.py's rate for gemini-3.6-flash, USD per 1M tokens; thinking bills as output
own = {}
for name in ("langchain", "langgraph", "adk"):
    b = brains.build(name, InMemorySaver())
    cfg = {"configurable": {"thread_id": f"acme:lesson104:{name}"}}
    b.answer(Q, config=cfg, context={"tenant_id": "acme", "user_id": "lesson104", "assertion": "", "brain": name})
    if name == "adk":                              # ADK keeps each model call's usage on the session's events
        s = asyncio.run(b.svc.get_session(app_name="documind", user_id="lesson104", session_id=cfg["configurable"]["thread_id"]))
        calls = [(u.prompt_token_count or 0, (u.candidates_token_count or 0) + (u.thoughts_token_count or 0), u.thoughts_token_count or 0)
                 for u in (e.usage_metadata for e in s.events) if u]
    else:                                          # LangChain keeps it on each AIMessage; output_tokens already counts thinking
        g = b.agent if name == "langchain" else b.graph
        calls = [(u["input_tokens"], u["output_tokens"], u.get("output_token_details", {}).get("reasoning", 0))
                 for u in (getattr(m, "usage_metadata", None) for m in g.get_state(cfg).values["messages"]) if u]
    tin, tout, think = (sum(c[i] for c in calls) for i in range(3))
    own[name] = (tin * IN + tout * OUT) / 1e6 * 85
    print(f"  {name:9} {len(calls)} model calls  in {tin:>6,}  out {tout:>5,} (thinking {think:>5,})  Rs {own[name]:.4f}")
lines = json.load(open(os.path.expanduser("~/lesson104_lines.json")))
print("the four cost lines, whole: the brain's own model calls + rag-api's, from step 5")
for name in ("direct", "langchain", "langgraph", "adk"):
    mine, rag = own.get(name, 0.0), lines.get(name, {}).get("rs", 0.0)
    print(f"  {name:9} Rs {mine:.4f} + Rs {rag:.4f} = Rs {mine + rag:.4f}")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted).
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
