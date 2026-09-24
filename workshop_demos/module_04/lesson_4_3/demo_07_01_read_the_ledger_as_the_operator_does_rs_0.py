"""Lesson 4.3 / s7: The three states side by side

Summary and purpose:
Read the ledger as the operator does, Rs 0

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_04_do_it_withdraw_the_note_test_the_tombstone_resto
Expected observation: source                                       status            gen chunks reused embed retired effective  embedding              indexed_at
acme/code_on_wages_2019.pdf                  indexed    ...2671234567     67      0    67       0 -          text-embedding-005@1   2026-09-20T09:14:02
acme/hr_policy_2026.md                       indexed    ...4107123456    283    283     0     283 -          text-embedding-005@1   2026-09-22T13:41:55
acme/smoke_note_v1.md                        indexed    ...5302345678      3      3     0       0 -          text-embedding-005@1   2026-09-22T15:21:40
...
{"ledger": "acme", "fingerprint": "3a9f0c17e5d2b846", "versions": 9, "last_event": "ingest_reactivated"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L777

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make sources PROJECT=$PROJECT TENANT_ONLY=acme
"""


def demonstrate(session):
    """Run Read the ledger as the operator does, Rs 0 at this checkpoint.

    Read the ledger as the operator does, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT.
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
