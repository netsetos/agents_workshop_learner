"""Lesson 15.4 / s6: A withdrawal, then the restore

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the handbook withdrawn by hand, then the check)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: {"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md", "fingerprint": "756528d4215dfc80", "retired_doc_keys": ["zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a"], "retired_ids": ["zeta:e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a#0", "...", "zeta:e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a#99"], "retired_chunks": 283, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}
the mirror's doc.mirror events for zeta since 2026-09-24T08:20:00Z (the audit bucket):
  08:20:24  delete:withdrawn  rag_engine    us-central1 zeta_e920a147...
  08:20:24  delete:withdrawn  vertex_search global      zeta_e920a147...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook withdrawn):
  0:00  handbook withdrawn;

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L813

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make retire PROJECT="$PROJECT" SOURCE=zeta/hr_policy_zeta_2026.md
fresh154 withdrawn
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook withdrawn by hand, then the check).
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
