"""Lesson 13.2 / s6: The alert the dead-letter queue never had

Summary and purpose:
Do it: plan and apply

HTML instruction: bash — run in the operator shell, in the checkout where make up ran (Terraform's state)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_what_pages_you_today
Expected observation: PASS: saved confirmed inputs to .../terraform/runbook-project.auto.tfvars.json
CI trust: OWNER/REPO (ID NUMBER) / refs/heads/main
...
Terraform will perform the following actions:

  # google_monitoring_alert_policy.dlq_depth will be created
  + resource "google_monitoring_alert_policy" "dlq_depth" {
      + combiner              = "OR"
      + display_name          = "Ingest dead-letter queue holds messages"
      + notification_channels = [
          + "projects/documind-ai-YOUR-ID/notificationChannels/NUMBER",
        ]
      ...
    }

Plan: 1 to add, 0 to change, 0 to destroy.
PASS: no deletes/replacements or existing CI trust changes. Reviewed plan: .../terraform/rag-20260924T060011Z-3f2a9c1d7e.tfplan
Review the displayed changes, then run this command with 'apply' instead of 'plan'.
PASS: selected plan, confirmed inputs, backend/workspace and state agree: .../terraform/rag-2026092

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.2-usage-reconcile/Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html#L738

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make plan PROJECT="$PROJECT" REGION="$REGION" ADMIN_EMAILS="$ME"   # the flags you gave make up; the plan refuses to delete
python commands/infrastructure.py apply --project "$PROJECT" --region "$REGION" --terraform-dir terraform   # make up's first line, alone
"""


def demonstrate(session):
    """Run Do it: plan and apply at this checkpoint.

    Do it: plan and apply

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the checkout where make up ran (Terraform's state).
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
