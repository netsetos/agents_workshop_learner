"""Lesson 4.3: demo 02 stale event verdicts

Replay three simulated events and explain the generation guard.

Run order inside this file:
1. Do it: three events, three verdicts, Rs 0 (source window 19)

Prerequisites: demo_01_current_and_retired_versions.
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


# Original CLI workflow for step_01_three_events_three_verdicts_rs_0.
COMMANDS_01 = """GEN="$(curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; print(next(r['generation'] for r in json.load(sys.stdin)['sources'] if r['name'].endswith('hr_policy_2026.md')))")"
SIZE="$(stat -c %s evals/corpus/acme/hr_policy_2026.md)"; echo "the ledger's generation for the handbook: $GEN"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for G in $((GEN - 1)) $GEN $((GEN + 1)); do
  gcloud pubsub topics publish documind-ingest --project "$PROJECT" \\
    --message "{\\"bucket\\":\\"$PROJECT-uploads\\",\\"name\\":\\"acme/hr_policy_2026.md\\",\\"generation\\":\\"$G\\",\\"size\\":\\"$SIZE\\",\\"contentType\\":\\"text/markdown\\"}" >/dev/null
done
sleep 25
gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$SINCE\\"" \\
  --project "$PROJECT" --limit 5 --format='table(timestamp,jsonPayload.event,jsonPayload.generation,jsonPayload.ledger_generation,jsonPayload.reason)'

"""

def step_01_three_events_three_verdicts_rs_0(session):
    """Run Do it: three events, three verdicts, Rs 0 at this checkpoint.

    The block reads the handbook's generation off the ledger, then publishes three records into the ingest topic exactly as Cloud Storage would, with the generation before the ledger's, the ledger's own, and one after it. The push subscription delivers them to the worker, and the worker's three lines say what it did with each. Nothing on the lane changes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (three messages; nothing is indexed).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_19', step_01_three_events_three_verdicts_rs_0),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
