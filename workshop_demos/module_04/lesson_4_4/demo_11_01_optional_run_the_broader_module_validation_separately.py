"""Lesson 4.4 / s11: Run the broader module validation separately

Summary and purpose:
The reindex smoke tests a different fixture and a wider lifecycle; it is not the proof of this chapter's deletion repair. make smoke-reindex uploads the kit's version 1 and version 2 under its own name, checks carry-over and reactivation, and asks the smoke-lantern question. Existing copies of that fact can affect the answer checks. Rehearse this separately, inspect its citations and fixture state, and report its actual pass/fail result. Do not replace the exact source and generation checks above with a green answer from this other note.

HTML instruction: bash — optional module smoke; retain its exit status and inspect any failure
Category: optional. Read the matching README checkpoint before Run.
Prerequisites: demo_08_01_restore_the_exact_bytes_and_prove_reuse
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L976

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make smoke-reindex PROJECT="$PROJECT" TENANT=acme
"""


def demonstrate(session):
    """Run Run the broader module validation separately at this checkpoint.

    The reindex smoke tests a different fixture and a wider lifecycle; it is not the proof of this chapter's deletion repair. make smoke-reindex uploads the kit's version 1 and version 2 under its own name, checks carry-over and reactivation, and asks the smoke-lantern question. Existing copies of that fact can affect the answer checks. Rehearse this separately, inspect its citations and fixture state, and report its actual pass/fail result. Do not replace the exact source and generation checks above with a green answer from this other note.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — optional module smoke; retain its exit status and inspect any failure.
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
