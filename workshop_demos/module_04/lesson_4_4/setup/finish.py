"""Lesson 4.4: finish

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

Run order inside this file:
1. Verify the story and restore the original backend (source window 44)

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


def step_01_verify_the_story_and_restore_the_original(session):
    """Run Verify the story and restore the original backend at this checkpoint.

    Use the state transition and the exact evidence, then return the tenant to its saved configuration. Before reporting the chapter complete, check the final source and plan. If the optional incomplete-undo variation was run, record its fresh ingestion separately from the successful reuse in step 8. Leave the verified fixture and local original available for the audience to inspect.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — finish the demo, then restore the pin saved before it began.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    try:
        session.shell("ch44_source && ch44_plan clean")
    finally:
        session.shell('ch44_restore_backend() {\n  local previous\n  previous="$(cat "$DEMO_DIR/backend-before.txt")" || return\n  case "$previous" in\n    vector|firestore|rag_engine|vertex_search|default) ;;\n    *) echo "STOP: saved backend is missing or invalid."; return 1 ;;\n  esac\n  make tenant-backend PROJECT="$PROJECT" TENANT=acme RETRIEVAL_BACKEND="$previous"\n}\nch44_restore_backend')
        session.state["backend_restore_required"] = False
        session.save()

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_44', step_01_verify_the_story_and_restore_the_original),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=True)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
