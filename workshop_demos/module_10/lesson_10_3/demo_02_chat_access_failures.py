"""Lesson 10.3: demo 02 chat access failures

Test access failures at the chat service's admission and identity gates.

Run order inside this file:
1. Do it (source window 15)

Prerequisites: demo_01_tool_failure_cases.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_example.
COMMANDS_01 = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
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

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three identities at the chat service's door).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_15', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
