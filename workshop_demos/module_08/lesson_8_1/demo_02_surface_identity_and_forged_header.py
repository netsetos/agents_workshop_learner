"""Lesson 8.1: demo 02 surface identity and forged header

Trace shared verification across services and test a forged user header.

Run order inside this file:
1. Do it: which services call the shared verifier (source window 24)
2. One request, end to end: a forged header, and the row that ignores it (source window 27)

Prerequisites: demo_01_token_and_roster.
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


# Original CLI workflow for step_01_which_services_call_the_shared_verifier.
COMMANDS_01 = """grep -rl "iap.identity(" --include=*.py services smoke | sort

"""

def step_01_which_services_call_the_shared_verifier(session):
    """Run Do it: which services call the shared verifier at this checkpoint.

    Do it: which services call the shared verifier

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (which services call the shared verifier).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_one_request_end_to_end_a_forged_header_and.
COMMANDS_02 = """TOKEN="$(tok "$API")" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask
q = "What is the notice period for a confirmed E3?"
for header in ("eval@documind.in", "ceo@acme.example"):
    status, body, ms = ask(os.environ["API"], q, "acme", header, os.environ["TOKEN"])
    print(f"x-user-email {header:18} HTTP {status}, answerable {body.get('answerable')}")
PY
sleep 20
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" AND jsonPayload.tenant="acme"' \\
  --project "$PROJECT" --freshness=10m --limit 2 --format='value(timestamp,jsonPayload.user,jsonPayload.tenant)'

"""

def step_02_one_request_end_to_end_a_forged_header_and(session):
    """Run One request, end to end: a forged header, and the row that ignores it at this checkpoint.

    Two questions to acme, one claiming to be the CEO, and the two usage rows they leave. The cell asks the same question twice with run_eval.py's own ask(), which sets an x-user-email header on every request. The first names the eval account; the second claims to be ceo@acme.example. Both carry your token and no assertion, so the bearer leg names the caller. After twenty seconds for the logs to land, the cell reads the two newest query rows for acme.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_24', step_01_which_services_call_the_shared_verifier),
        ('source_27', step_02_one_request_end_to_end_a_forged_header_and),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
