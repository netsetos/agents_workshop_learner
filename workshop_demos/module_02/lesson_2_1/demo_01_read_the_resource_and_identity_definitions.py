"""Lesson 2.1 / plan-1: Read the resource and identity definitions

Summary and purpose:
Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
