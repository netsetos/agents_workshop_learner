"""Lesson 9.2 / s4: Scope: the same words under other settings

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_the_state_and_three_asks
Expected observation: vertex none     in  43349 cached  41259  2610 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2440 ms | A confirmed employee at grade E3 or above serves a
  scope as asked   7a0875abc72b0f7b
  scope top_k 8    bcc480117460bf66
  scope kind: text 8d8d4a1d9912dc52
  scope prompt v4  1d409edacc15c1d1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L509

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask92 "$CAND" 8                     # top_k 8: another scope
ask92 "$CAND" 6 '{"kind": "text"}'   # a filter: another scope
python - <<'PY'
import sys
sys.path.insert(0, "services/rag-api")
from semantic_cache import scope_of
for label, f, k, p in [("as asked", None, 6, "v3"), ("top_k 8", None, 8, "v3"), ("kind: text", {"kind": "text"}, 6, "v3"), ("prompt v4", None, 6, "v4")]:
    print(f"  scope {label:10} {scope_of(f, k, p)}")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes).
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
