"""Lesson 2.3: Record restart inputs

Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

Run order inside this file:
1. Record restart inputs (source window plan-2)

Prerequisites: demo_01_check_readiness_and_smoke.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
Example: open this file at the matching HTML heading, Run once, then inspect
the observations below before continuing to the next numbered section.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_record_restart_inputs(session):
    """Run Record restart inputs at this checkpoint.

    Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe the printed/saved evidence for this heading; a zero exit alone is not proof.
    """
    from pathlib import Path
    from workshop_helpers.artifacts import write_json
    write_json(session.attempt / "restart_inputs.json", {"project": session.config.project, "region": session.config.cloud_run_region, "kit_root": str(session.config.kit_root)})
    print(Path("commands/session-restart.sh").read_text(encoding="utf-8"))
    print("Saved non-secret inputs:", session.attempt / "restart_inputs.json")

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_02_record_restart_inputs', step_01_record_restart_inputs),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
