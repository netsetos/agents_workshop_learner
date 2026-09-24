"""Lesson 2.1: demo 01 read the resource and identity definitions

Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

Run order inside this file:
1. Read the resource and identity definitions (source window plan-1)

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


def step_01_read_the_resource_and_identity_definitions(session):
    """Run Read the resource and identity definitions at this checkpoint.

    Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from pathlib import Path
    import re
    for path in sorted(Path("terraform").glob("*.tf")):
        resources = re.findall(r'resource\s+"([^"]+)"\s+"([^"]+)"', path.read_text(encoding="utf-8"))
        if resources:
            print(path.name, resources)
    print(Path("INFRASTRUCTURE.md").read_text(encoding="utf-8"))

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_01_read_the_resource_and_identity_definitions', step_01_read_the_resource_and_identity_definitions),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
