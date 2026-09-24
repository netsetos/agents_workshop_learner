"""Lesson 13.1 / s6: Trace it, name the cause, put it back

Summary and purpose:
Do it: put version 1 back

HTML instruction: bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it_the_versions_view_and_the_two_probes
Expected observation: >> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  [1] hr_policy_2026.md  version 497809ffbaa6  chunk 1  'serves a notice period of 60 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-restored.json
PASS: both Firestore filter modes verified. Evidence: operator-evidence/firestore-combined-filters.json

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html#L772

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/corpus/acme/hr_policy_2026.md
ask131 restored
GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py | tail -1
"""


def demonstrate(session):
    """Run Do it: put version 1 back at this checkpoint.

    Do it: put version 1 back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again).
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
