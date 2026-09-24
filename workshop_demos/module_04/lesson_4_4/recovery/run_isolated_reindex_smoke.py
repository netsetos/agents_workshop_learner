"""Lesson 4.4: run isolated reindex smoke

Explicit recovery: run isolated reindex smoke

Run order inside this file:
1. Run the broader module validation separately (source window 42)

Prerequisites: workshop setup; see this lesson README.
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


def step_01_run_the_broader_module_validation_separate(session):
    """Run Run the broader module validation separately at this checkpoint.

    Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL. The check wants the answer to say bay 7 and not bay 4. Lesson 3.4's note, acme/smoke_note_v1.md, which step 5 restored, carries the same clause with bay 4 and no date, so with it current the model reads two sources that disagree; rule six tells it to follow the dated one and say from when it applies, and an answer that mentions the old bay fails the check although it is right. Withdraw the note for the smoke and restore it after: both are the kit's own targets from lesson 4.3, and the restore embeds nothing.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the note withdrawn, the smoke, the note restored).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.shell("make retire PROJECT=$PROJECT SOURCE=acme/smoke_note_v1.md")
    try:
        session.shell("make smoke-reindex PROJECT=$PROJECT")
    finally:
        session.shell("make restore PROJECT=$PROJECT SOURCE=acme/smoke_note_v1.md")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_42', step_01_run_the_broader_module_validation_separate),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
