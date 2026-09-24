"""Lesson 14.3: demo 01 promote the gated revision

Require the saved gate from 14.2 to match this project, region and candidate, then use the kit's by-name promotion. The kit records the previous serving revision for rollback.

Run order inside this file:
1. Promote the gated revision (source window plan-1)

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


def step_01_promote_the_gated_revision(session):
    """Run Promote the gated revision at this checkpoint.

    Require the saved gate from 14.2 to match this project, region and candidate, then use the kit's by-name promotion. The kit records the previous serving revision for rollback.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, sys
    from pathlib import Path
    gate = json.loads((session.config.results_dir / "release_gate.json").read_text())
    candidate = Path(".candidate-revision").read_text().strip()
    assert gate["passed"] and gate["project"] == session.config.project and gate["region"] == session.config.cloud_run_region
    assert gate["revision"] == candidate, "A different candidate was gated; do not promote this one."
    session.command(["make", "promote", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_01_promote_the_gated_revision', step_01_promote_the_gated_revision),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
