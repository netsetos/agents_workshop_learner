"""Lesson 4.2 / s7: The gate goes red, and the two ways back to green

Summary and purpose:
Version 1's bytes again, through the same release command. The offline gate passes, the upload lands, and the worker finds a version it has retired within the window: ingest_reactivated, nothing embedded, revision 3 retired in turn. The live gate then passes with the rows as they are.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the undo, then ten questions again)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_the_live_gate_red
Expected observation: >> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
...
  [PASS] must_contain_rate     100.0%  (threshold 85%; 10 rows)
  ...
  shape        rows   ok   pass
  lookup          9    9      9
  version         1    1      1
  All thresholds met.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html#L690

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make reindex PROJECT=$PROJECT TENANT=acme FILE=evals/corpus/acme/hr_policy_2026.md

make eval-live PROJECT=$PROJECT SOURCE=hr_policy_2026.md
"""


def demonstrate(session):
    """Run The undo, then the gate, green at this checkpoint.

    Version 1's bytes again, through the same release command. The offline gate passes, the upload lands, and the worker finds a version it has retired within the window: ingest_reactivated, nothing embedded, revision 3 retired in turn. The live gate then passes with the rows as they are.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the undo, then ten questions again).
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
