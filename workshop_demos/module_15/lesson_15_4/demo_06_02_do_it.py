"""Lesson 15.4 / s6: A withdrawal, then the restore

Summary and purpose:
Then the restore:

HTML instruction: bash — run in the operator shell, in the kit (the handbook brought back, then the check)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: {"event": "reconcile_restored", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md", "generation": "1758000000021000", "next": "ingest_reactivated inside the undo window, ingest_ok (a fresh version) after it"}
the mirror's doc.mirror events for zeta since 2026-09-24T08:30:00Z (the audit bucket):
  08:30:39  upsert            rag_engine    us-central1 zeta_e920a147...
  08:30:39  upsert            vertex_search global      zeta_e920a147...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook indexed):
  0:00  handbook indexed; rag_engine in sync; vertex_search drift, missing zeta_e920a147...
  0:20  handbook indexed; rag_engine in sync; vertex_search in sync
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant"

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L837

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make restore PROJECT="$PROJECT" SOURCE=zeta/hr_policy_zeta_2026.md
fresh154 indexed
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Then the restore:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook brought back, then the check).
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
