"""Lesson 14.4 / plan-2: Write an evidence handover

Summary and purpose:
Summarize actual lesson attempts and retain the exact candidate gate, failures and evidence locations. This is an evidence index for a human capstone review, not an automatic rubric score.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_run_the_operational_gate
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Write an evidence handover at this checkpoint.

    Summarize actual lesson attempts and retain the exact candidate gate, failures and evidence locations. This is an evidence index for a human capstone review, not an automatic rubric score.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json
    from workshop_helpers.artifacts import write_json
    records = []
    for path in sorted(session.config.results_dir.glob("module_*/lesson_*/*/session.json")):
        state = json.loads(path.read_text(encoding="utf-8"))
        records.append({"lesson": state["lesson"], "project": state["identity"]["project"], "evidence": str(path),
                        "completed": state["completed"], "failed_attempts": [a for a in state["attempts"] if a["status"] == "failed"],
                        "backend_restore_required": state.get("backend_restore_required", False)})
    write_json(session.attempt / "handover.json", records)
    print("Evidence index:", session.attempt / "handover.json")
    print("Review the capstone rubric against the actual artifacts; no score was invented.")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
