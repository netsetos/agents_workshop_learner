"""Lesson 15.4 / s5: A new version, then the undo

Summary and purpose:
Now the undo: the same name, with the first version's bytes, straight from the kit's corpus. This is the worker's branch for a version it has seen before:

HTML instruction: bash — run in the operator shell, in the kit (the first version's bytes again, then the check)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: ...
>> gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a	283	283	0	283	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_zeta_2026.md API=<candidate url>
the mirror's doc.mirror events for zeta since 2026-09-24T08:10:00Z (the audit bucket):
  08:10:48  upsert            rag_engine    us-central1 zeta_e920a147...
  08:10:48  upsert            vertex_search global      zeta_e920a147...
  08:10:49  delete:superseded rag_engine    us-central1 zeta_025c4143...
  08:10:49  delete:superseded vertex_search global      zeta_025c4143...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook indexed):
 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L766

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make reindex PROJECT="$PROJECT" TENANT=zeta FILE=evals/corpus/zeta/hr_policy_zeta_2026.md NAME=hr_policy_zeta_2026.md
fresh154 indexed
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Now the undo: the same name, with the first version's bytes, straight from the kit's corpus. This is the worker's branch for a version it has seen before:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the first version's bytes again, then the check).
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
