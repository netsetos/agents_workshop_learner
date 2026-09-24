"""Lesson 6.4 / s3: The front door: IAP, the UI's settings, and who may sign in

Summary and purpose:
Do it: the service's account, IAP's flag, who may sign in, and a request without one

HTML instruction: bash — run in the operator shell (four reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    run.googleapis.com/iap-enabled: 'true'
roles/iap.httpsResourceAccessor	user:you@example.com
without a sign-in: HTTP 302 -> https://accounts.google.com/o/oauth2/v2/auth?client_id=...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L471

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services describe documind-ui --region "$REGION" --project "$PROJECT" --format='value(spec.template.spec.serviceAccountName)'
gcloud run services describe documind-ui --region "$REGION" --project "$PROJECT" --format=yaml | grep -i "iap-enabled"
gcloud iap web get-iam-policy --resource-type=cloud-run --service=documind-ui --region "$REGION" --project "$PROJECT" \\
  --flatten=bindings --format='value(bindings.role,bindings.members)'
curl -s -o /dev/null -w "without a sign-in: HTTP %{http_code} -> %{redirect_url}\\n" "$UI/"
"""


def demonstrate(session):
    """Run Do it: the service's account, IAP's flag, who may sign in, and a request without one at this checkpoint.

    Do it: the service's account, IAP's flag, who may sign in, and a request without one

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (four reads).
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
