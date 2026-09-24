"""Lesson 5.4 / s7: The tier from the rows: vector-status, backfill-vectors, and the rows that count the rung

Summary and purpose:
Do it: count the tier, plan its refill, read the rows by rung, Rs 0

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only: the plan writes nothing without --apply)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_probe_then_its_evidence
Expected observation: index: documind-chunks  datapoints: 4xxx  shards: 1  update: STREAM_UPDATE
endpoint: documind-endpoint  deployed: documind_chunks_v1  synced: 2026-09-2xT1x:xx:xx.xxxxxxZ
{"event": "backfill_vectors_plan", "index": "projects/NUMBER/locations/asia-south1/indexes/1234567890123456789", "tenant": "acme", "current_chunks": 1xxx, "needs_document_embedding": 0, "invalid_chunks": 0, "embedding_task_type": "RETRIEVAL_DOCUMENT", "note": "Pause uploads/undo/batch writers; keep answer caches off during repair and validation."}

by retrieval backend (which store served the pool; 13 September 2026)
retrieval_backend      answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
firestore                    5      xxxx      xxx    0.0xxx      x.xx    2xxx   0.20
vector                       6      xxxx      xxx    0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L763

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python commands/lane.py vector-status                             # the same as: make vector-status PROJECT=$PROJECT
python commands/lane.py backfill-vectors --tenant acme            # the same as: make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme
make usage PROJECT=$PROJECT HOURS=1 | sed -n '/by retrieval backend/,/^$/p'
"""


def demonstrate(session):
    """Run Do it: count the tier, plan its refill, read the rows by rung, Rs 0 at this checkpoint.

    Do it: count the tier, plan its refill, read the rows by rung, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only: the plan writes nothing without --apply).
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
