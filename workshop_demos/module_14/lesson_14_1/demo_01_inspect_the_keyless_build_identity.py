"""Lesson 14.1 / plan-1: Inspect the keyless build identity

Summary and purpose:
Read the kit's workload-identity and build definitions. Verify repository/ref conditions in the real deployment configuration before submitting a build; no service-account key is generated.

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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
