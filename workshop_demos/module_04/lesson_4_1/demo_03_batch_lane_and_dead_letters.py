"""Lesson 4.1: demo 03 batch lane and dead letters

Read the batch lane's queue and job, then inspect the drill's dead letter when it arrives.

Run order inside this file:
1. Read the lane, Rs 0 (source window 27)
2. Read it, when it has landed (source window 34)

Prerequisites: demo_02_poison_retries.
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


# Original CLI workflow for step_01_read_the_lane_rs_0.
COMMANDS_01 = """make queued PROJECT=$PROJECT

if [ -n "$BATCH_JOB" ]; then
  gcloud run jobs describe "$BATCH_JOB" --region "$REGION" --project "$PROJECT" --format=json | python -c "
import json, sys
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('image', 'args', 'timeoutSeconds', 'maxRetries', 'taskCount'): print(f'{k}: {v}')
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(json.load(sys.stdin))"
  gcloud scheduler jobs describe documind-ingest-batch-hourly --location "$REGION" --project "$PROJECT" --format='value(schedule,timeZone,state)'
else
  echo "no batch job on this lane: a queued claim waits until make batch-job declares it (BATCH_JOB=true, a Terraform apply)"
fi

"""

def step_01_read_the_lane_rs_0(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_when_it_has_landed(session):
    """Run Read it, when it has landed at this checkpoint.

    The poison message from step 5 reaches the queue about an hour after its first refusal. Run the first line then; an empty listing earlier is the retries still running, not a fault. The second read decodes the message's own record, the same JSON the worker refused, to see the size of zero with your own eyes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint("Dead-letter delivery can take about an hour. Inspect the drill's dead letter only once it has landed. Stop here and rerun this demo later; the steps already completed will not run again.")
    from workshop_helpers.poison import inspect_dead_letter
    inspect_dead_letter(session)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_27', step_01_read_the_lane_rs_0),
        ('source_34', step_02_when_it_has_landed),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
