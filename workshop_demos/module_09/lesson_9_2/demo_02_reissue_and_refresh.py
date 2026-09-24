"""Lesson 9.2: demo 02 reissue and refresh

Release revision 2, observe both cache reactions and refresh the context cache.

Run order inside this file:
1. Do it: the release (source window 17)
2. Do it: the state, both asks, and the log (source window 19)
3. Do it (source window 22)

Prerequisites: demo_01_cache_state_and_scope.
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


# Original CLI workflow for step_01_the_release.
COMMANDS_01 = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/demo/hr_policy_2026_v2.md NAME=hr_policy_2026.md

"""

def step_01_the_release(session):
    """Run Do it: the release at this checkpoint.

    Do it: the release

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_state_both_asks_and_the_log.
COMMANDS_02 = """state92
ask92 "$API"            # the live revision
ask92 "$CAND"           # the candidate
python - <<'PY'
import json, os, subprocess
f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="cache_stale" '
     f'AND timestamp>="{os.environ["SINCE92"]}"')
out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "5",
                      "--format", "json"], capture_output=True, text=True, check=True).stdout
for e in json.loads(out or "[]"):
    j = e["jsonPayload"]
    print(f"  cache_stale {j['tenant']}: packed from {j['cache_fingerprint']}, ledger now {j['ledger_fingerprint']}")
PY

"""

def step_02_the_state_both_asks_and_the_log(session):
    """Run Do it: the state, both asks, and the log at this checkpoint.

    Do it: the state, both asks, and the log

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_example.
COMMANDS_03 = """make cache PROJECT="$PROJECT" TENANT=acme
state92
ask92 "$API"

"""

def step_03_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the pack again, under the new fingerprint).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_the_release),
        ('source_19', step_02_the_state_both_asks_and_the_log),
        ('source_22', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
