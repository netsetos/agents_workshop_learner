"""Lesson 8.3 / s4: The findings: types and offsets, in Firestore and in the DLP tab

Summary and purpose:
The console sits behind IAP and admits only the addresses the lane was deployed with as ADMIN_EMAILS. If it answers 403 - Admins only, your address is not among them; the cell above has already read the records the tab draws.

HTML instruction: bash — run in the operator shell, in the kit (the admin console's address)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_records
Expected observation: https://documind-admin-NUMBER.asia-south1.run.app   <- open in your browser, then the DLP tab

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html#L491

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services describe documind-admin --region "$REGION" --project "$PROJECT" --format='value(metadata.name)' >/dev/null 2>&1 \\
  && echo "https://documind-admin-$NUMBER.$REGION.run.app   <- open in your browser, then the DLP tab" \\
  || echo "documind-admin is not deployed on this lane"
"""


def demonstrate(session):
    """Run Do it: the DLP tab at this checkpoint.

    The console sits behind IAP and admits only the addresses the lane was deployed with as ADMIN_EMAILS. If it answers 403 - Admins only, your address is not among them; the cell above has already read the records the tab draws.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the admin console's address).
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
