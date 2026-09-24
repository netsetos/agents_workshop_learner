"""Lesson 6.4 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The UI's own environment says how it signs people in, where it uploads and which API it calls. The block prints the five names that matter and exports the UI's address for the steps below. An empty CHAT_URL means the chat service is not deployed on this lane, and then Chat has no brain picker. The page streams from the API directly, which is the journey this lesson follows.

HTML instruction: bash — run in the operator shell, once per shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: AUTH_MODE      iap
RAG_API_URL    https://documind-api-NUMBER.asia-south1.run.app
UPLOAD_BUCKET  documind-ai-YOUR-ID-uploads
IAP_AUDIENCE   /projects/NUMBER/locations/asia-south1/services/documind-ui
CHAT_URL       https://documind-chat-NUMBER.asia-south1.run.app
UI=https://documind-ui-NUMBER.asia-south1.run.app

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L403

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """svc_env() { gcloud run services describe "$1" --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep "'name': '$2'" | sed -nE "s/.*'value': '([^']*)'.*/\\1/p"; }
for N in AUTH_MODE RAG_API_URL UPLOAD_BUCKET IAP_AUDIENCE CHAT_URL; do printf '%-14s %s\\n' "$N" "$(svc_env documind-ui $N)"; done
export UI="https://documind-ui-$NUMBER.$REGION.run.app"; echo "UI=$UI"
"""


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The UI's own environment says how it signs people in, where it uploads and which API it calls. The block prints the five names that matter and exports the UI's address for the steps below. An empty CHAT_URL means the chat service is not deployed on this lane, and then Chat has no brain picker. The page streams from the API directly, which is the journey this lesson follows.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, once per shell.
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
