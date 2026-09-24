"""Lesson 9.2 / s5: The corpus moves: revision 2, and both caches react

Summary and purpose:
Do it: the release

HTML instruction: bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: >> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_5560308823a62dc8...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L555

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/demo/hr_policy_2026_v2.md NAME=hr_policy_2026.md
"""


def demonstrate(session):
    """Run Do it: the release at this checkpoint.

    Do it: the release

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release).
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
