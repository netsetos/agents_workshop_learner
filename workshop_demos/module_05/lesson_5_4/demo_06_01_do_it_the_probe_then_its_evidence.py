"""Lesson 5.4 / s6: The probe: the kit's read-only check of the combined filters

Summary and purpose:
Do it: the probe, then its evidence

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one embedding read off a row, a few dozen Firestore reads; nothing written to the cloud)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it_a_candidate_that_cannot_reach_the_index
Expected observation: {"project": "documind-ai-YOUR-ID", "collection": "chunks", "source_uri": "gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md", "source_status": "indexed", "source_doc_key": "acme_497809ff..."}
Verified HR source: 283 current chunks; stored doc_type='unknown'; manifest doc_type='policy'
NOTE: stored metadata differs from the manifest. This probe tests the stored equality filters; it does not certify policy classification or repair metadata.
PASS: combined doc_type='unknown'+kind='text', current=off, rows=5
PASS: combined doc_type='unknown'+kind='text', current=on, rows=5
PASS: both Firestore filter modes verified. Evidence: operator-evidence/firestore-combined-filters.json
evidence: {'doc_type': 'unknown', 'kind': 'text'} | current off: 5 rows | current on: 5 rows | doc_key acme_497809ff...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L711

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export GOOGLE_CLOUD_PROJECT="$PROJECT"                                    # the probe insists the two agree
python commands/check-firestore-fallback.py
python -c "import json; r = json.load(open('operator-evidence/firestore-combined-filters.json')); print('evidence:', r['filters'], '| current off:', len(r['results']['off']['ids']), 'rows | current on:', len(r['results']['on']['ids']), 'rows | doc_key', r['doc_key'][:17] + '...')"
"""


def demonstrate(session):
    """Run Do it: the probe, then its evidence at this checkpoint.

    Do it: the probe, then its evidence

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one embedding read off a row, a few dozen Firestore reads; nothing written to the cloud).
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
