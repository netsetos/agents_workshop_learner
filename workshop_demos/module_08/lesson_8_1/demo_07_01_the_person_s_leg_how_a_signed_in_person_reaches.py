"""Lesson 8.1 / s7: The person's leg: how a signed-in person reaches the API through the UI

Summary and purpose:
IAP in front of the UI, the assertion forwarded beside the UI's token, and every caller the API recorded in a day. A person never calls the API directly. They sign in at IAP in front of the UI, which admits only accounts granted the sign-in role. IAP hands the UI a signed assertion with every request. When the UI calls the API, it sends two credentials, as its _headers() shows in step 5: its own token, which gets past the door, and the person's assertion, forwarded unchanged. The API's verifier sees the assertion first and takes the person's email from it. The roster check and the usage row are then about the person, which is what lesson 6.4 saw in Chat. The cell counts every caller the API recorded in the last day.

HTML instruction: bash — run in the operator shell, in the kit (every caller the API recorded in the last day)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_one_request_end_to_end_a_forged_header_and_the_r
Expected observation: NN documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
      N you@example.com

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L719

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="query" OR jsonPayload.event="stream")' \\
  --project "$PROJECT" --freshness=1d --limit 1000 --format='value(jsonPayload.user)' | sort | uniq -c | sort -rn
"""


def demonstrate(session):
    """Run The person's leg: how a signed-in person reaches the API through the UI at this checkpoint.

    IAP in front of the UI, the assertion forwarded beside the UI's token, and every caller the API recorded in a day. A person never calls the API directly. They sign in at IAP in front of the UI, which admits only accounts granted the sign-in role. IAP hands the UI a signed assertion with every request. When the UI calls the API, it sends two credentials, as its _headers() shows in step 5: its own token, which gets past the door, and the person's assertion, forwarded unchanged. The API's verifier sees the assertion first and takes the person's email from it. The roster check and the usage row are then about the person, which is what lesson 6.4 saw in Chat. The cell counts every caller the API recorded in the last day.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every caller the API recorded in the last day).
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
