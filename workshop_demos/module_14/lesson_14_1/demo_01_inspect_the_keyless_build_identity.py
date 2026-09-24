"""Lesson 14.1: demo 01 inspect the keyless build identity

Read the kit's workload-identity and build definitions. Verify repository/ref conditions in the real deployment configuration before submitting a build; no service-account key is generated.

Run order inside this file:
1. Inspect the keyless build identity (source window plan-1)

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


def step_01_inspect_the_keyless_build_identity(session):
    """Run Inspect the keyless build identity at this checkpoint.

    Read the kit's workload-identity and build definitions. Verify repository/ref conditions in the real deployment configuration before submitting a build; no service-account key is generated.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from pathlib import Path
    for path in (Path("terraform/ci.tf"), Path("cloudbuild.yaml")):
        if path.exists():
            print("\n", path, "\n", path.read_text(encoding="utf-8"))
    for path in Path("terraform").glob("*.tf"):
        text = path.read_text(encoding="utf-8")
        if "workload_identity" in text:
            print(path, "\n", text)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_01_inspect_the_keyless_build_identity', step_01_inspect_the_keyless_build_identity),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
