"""Lesson 4.3 / s4: Superseded: the retired rows' bookkeeping, and the clock that removes them

Summary and purpose:
Do it: the purge plan, Rs 0

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only without APPLY=1)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_read_the_handbook_s_versions_rs_0
Expected observation: {"event": "reconcile_purge_plan", "expired": 0, "retired": 566, "applied": false, "note": "the TTL policy on chunks.expire_at (firestore_indexes.tf) deletes these on its own within a day; this is the manual twin for a lane that has not applied it"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L515

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make purge PROJECT=$PROJECT TENANT_ONLY=acme
"""


def demonstrate(session):
    """Run Do it: the purge plan, Rs 0 at this checkpoint.

    Do it: the purge plan, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only without APPLY=1).
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
