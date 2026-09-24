"""Lesson 4.1: demo 02 poison retries

Start the poison drill and observe retries without mistaking a delayed dead letter for success.

Run order inside this file:
1. Do it: start the drill, then watch the first retries (source window 19)
2. Do it: start the drill, then watch the first retries (source window 21)

Prerequisites: demo_01_trace_upload_delivery.
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


def step_01_start_the_drill_then_watch_the_first_retri(session):
    """Run Do it: start the drill, then watch the first retries at this checkpoint.

    The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.poison import create_drill
    create_drill(session)

# Original CLI workflow for step_02_start_the_drill_then_watch_the_first_retri.
COMMANDS_02 = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND logName=\\"projects/$PROJECT/logs/run.googleapis.com%2Frequests\\" AND httpRequest.status=400 AND timestamp>=\\"$POISON_SINCE\\"" \\
  --project "$PROJECT" --limit 12 --format='table(timestamp,httpRequest.status,httpRequest.latency)'

echo "refusals logged so far: $(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event=\\"ingest_poison\\" AND timestamp>=\\"$POISON_SINCE\\"" --project "$PROJECT" --limit 12 --format='value(timestamp)' | wc -l) of 12"

"""

def step_02_start_the_drill_then_watch_the_first_retri(session):
    """Run Do it: start the drill, then watch the first retries at this checkpoint.

    The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, a few minutes later (read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint('The poison retries are asynchronous. Wait a few minutes after the drill, then type done to read its retry records. This does not prove a dead letter has arrived.')
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_19', step_01_start_the_drill_then_watch_the_first_retri),
        ('source_21', step_02_start_the_drill_then_watch_the_first_retri),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
