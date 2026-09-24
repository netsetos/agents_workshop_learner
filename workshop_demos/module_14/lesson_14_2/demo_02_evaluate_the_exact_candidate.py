"""Lesson 14.2 / plan-2: Evaluate the exact candidate

Summary and purpose:
Resolve the candidate tag and require it to name the recorded revision before the live gate. Save a project/region/revision-bound gate record only after the evaluator exits successfully.

HTML instruction: Course-plan experiment — live deployment
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_create_the_recorded_candidate
Expected observation: A successful live gate tied to the same recorded candidate revision.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Evaluate the exact candidate at this checkpoint.

    Resolve the candidate tag and require it to name the recorded revision before the live gate. Save a project/region/revision-bound gate record only after the evaluator exits successfully.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, sys
    from pathlib import Path
    from workshop_helpers.auth import gcloud
    from workshop_helpers.artifacts import write_json
    expected = Path(".candidate-revision").read_text().strip()
    service = json.loads(gcloud("run", "services", "describe", "documind-api", "--project=" + session.config.project, "--region=" + session.config.cloud_run_region, "--format=json"))
    tagged = next(row for row in service["status"]["traffic"] if row.get("tag") == "candidate")
    assert tagged["revisionName"] == expected, "The candidate tag moved; evaluate the intended revision."
    report = session.attempt / "candidate_gate.json"
    session.command(["make", "eval-live", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "API=" + tagged["url"], "REPORT=" + str(report), "PY=" + sys.executable])
    gate = {"project": session.config.project, "region": session.config.cloud_run_region, "revision": expected, "report": str(report), "passed": True}
    write_json(session.config.results_dir / "release_gate.json", gate)
    print("Gate passed for:", expected)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
