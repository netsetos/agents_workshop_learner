"""Lesson 4.4 / s7: Plan retirement, apply it, then prove zero drift

Summary and purpose:
Keep preview, mutation and verification as three visible operations. The action must be retire for $SOURCE, with reason gone from the bucket, applied: false and drift 1. A plan is evidence, not a repair. Pause other uploads during the demonstration; the kit's apply does not execute a saved, source-scoped plan.

HTML instruction: bash — recheck immediately before the tenant-wide apply
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_plan_retirement_apply_it_then_prove_zero_drift
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L669

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ch44_plan retire &&
  make reconcile PROJECT="$PROJECT" TENANT_ONLY=acme APPLY=1 &&
  ch44_source
"""


def demonstrate(session):
    """Run Plan retirement, apply it, then prove zero drift at this checkpoint.

    Keep preview, mutation and verification as three visible operations. The action must be retire for $SOURCE, with reason gone from the bucket, applied: false and drift 1. A plan is evidence, not a repair. Pause other uploads during the demonstration; the kit's apply does not execute a saved, source-scoped plan.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — recheck immediately before the tenant-wide apply.
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
