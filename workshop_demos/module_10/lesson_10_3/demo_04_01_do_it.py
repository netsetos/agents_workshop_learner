"""Lesson 10.3 / s4: Access failures at the chat service's door

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (three identities at the chat service's door)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_five_failures
Expected observation: 403  {"detail":"not a member of any tenant"}
  401  {"detail":"the bearer token carries no verified email"}
  200  {"answer":"Gratuity becomes payable after not less than five years of continuous service [1].","tool

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.3-tool-failures/Netsetos_GCP_Capstone_10.3_Tool_Failures_WIX.html#L524

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
chatas() {   # one /v1/chat turn with the token in $1: the status, then the start of the body
  code=$(curl -s -o /tmp/chat103.json -w "%{http_code}" -X POST "$CHAT/v1/chat" -H "Authorization: Bearer $1" \\
    -H "Content-Type: application/json" -d '{"question": "After how many years of continuous service does gratuity become payable?", "session_id": "lesson103"}')
  echo "  $code  $(head -c 100 /tmp/chat103.json)"
}
chatas "$(gcloud auth print-identity-token --include-email --audiences="$CHAT" \\
    --impersonate-service-account="documind-outsider-sa@$PROJECT.iam.gserviceaccount.com" 2>/dev/null)"   # admitted by IAM, on no roster
chatas "$(gcloud auth print-identity-token --audiences="$CHAT" \\
    --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" 2>/dev/null)"          # no --include-email
chatas "$(tok "$CHAT")"                                                                                  # a roster member
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three identities at the chat service's door).
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
