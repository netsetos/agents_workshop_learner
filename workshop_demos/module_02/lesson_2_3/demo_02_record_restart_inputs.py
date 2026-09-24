"""Lesson 2.3 / plan-2: Record restart inputs

Summary and purpose:
Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_check_readiness_and_smoke
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Record restart inputs at this checkpoint.

    Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from pathlib import Path
    from workshop_helpers.artifacts import write_json
    write_json(session.attempt / "restart_inputs.json", {"project": session.config.project, "region": session.config.cloud_run_region, "kit_root": str(session.config.kit_root)})
    print(Path("commands/session-restart.sh").read_text(encoding="utf-8"))
    print("Saved non-secret inputs:", session.attempt / "restart_inputs.json")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
