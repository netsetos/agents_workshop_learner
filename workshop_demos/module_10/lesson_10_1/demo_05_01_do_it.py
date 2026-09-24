"""Lesson 10.1 / s5: The one retrieve(), from your shell

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the one retrieve(), called from your shell as a roster member)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: 5 citations | answerable True | confidence high | 2.7 s
  first: {'chunk_id': 'acme:aaaaaaaa#0', 'page': 3, 'score': 0.94}
  rag-api's own answer: Gratuity is payable on termination after not less than five years of continuous service [1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L526

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export SINCE101="$(date -u +%FT%TZ)"
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" RAG_API_URL="$API" python - <<'PY'
import time
from shared.documind_tools import retrieve
t = time.time()
r = retrieve("After how many years of continuous service does gratuity become payable?", tenant_id="acme", top_k=5)
print(f"  {len(r['citations'])} citations | answerable {r['answerable']} | confidence {r['confidence']} | {time.time() - t:.1f} s")
if r["citations"]:
    print("  first:", {k: r["citations"][0].get(k) for k in ("chunk_id", "page", "score")})
print("  rag-api's own answer:", (r.get("answer") or r.get("error") or "")[:90])
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the one retrieve(), called from your shell as a roster member).
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
