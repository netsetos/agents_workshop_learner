"""Lesson 4.4 / s10: The nightly job, the number it ends on, and the lane older than the ledger

Summary and purpose:
Read the deployed job and backfill plan

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (all read-only; the backfill is printed, not applied)
Category: optional. Read the matching README checkpoint before Run.
Prerequisites: demo_08_01_restore_the_exact_bytes_and_prove_reuse
Expected observation: no nightly job on this lane: make reconcile-job declares and schedules it (RECONCILE_JOB=true, a Terraform apply)
no schedule either: make reconcile from a shell is the walk until then
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}

documind-reconcile
30 23 * * *	Asia/Kolkata	ENABLED
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L939

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run jobs describe documind-reconcile --region "$REGION" --project "$PROJECT" --format='value(name)' 2>/dev/null \\
  || echo "no nightly job on this lane: make reconcile-job declares and schedules it (RECONCILE_JOB=true, a Terraform apply)"
gcloud scheduler jobs describe documind-reconcile-nightly --location "$REGION" --project "$PROJECT" --format='value(schedule,timeZone,state)' 2>/dev/null \\
  || echo "no schedule either: make reconcile from a shell is the walk until then"

python services/ingest/reconcile.py --project "$PROJECT" --backfill
"""


def demonstrate(session):
    """Run Read the deployed job and backfill plan at this checkpoint.

    Read the deployed job and backfill plan

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (all read-only; the backfill is printed, not applied).
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
