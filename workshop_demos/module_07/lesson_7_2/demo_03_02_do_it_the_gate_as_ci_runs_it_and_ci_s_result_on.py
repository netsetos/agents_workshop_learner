"""Lesson 7.2 / s3: The offline half: on every push, and CI's verdict on the commit you run

Summary and purpose:
The next cell asks GitHub's public API which commits the dry run has judged, and marks the one your clone is at.

HTML instruction: bash — run in the operator shell, in the kit (one unauthenticated call to GitHub's public API)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on
Expected observation: your kit is at b89bbd8
  b89bbd8  push  success  2026-09-23  <- the commit you run
  6999d24  push  success  2026-09-22

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L446

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the gate as CI runs it, and CI's result on your commit at this checkpoint.

    The next cell asks GitHub's public API which commits the dry run has judged, and marks the one your clone is at.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one unauthenticated call to GitHub's public API).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, subprocess, urllib.request
    url = "https://api.github.com/repos/netsetos/agents_workshop_learner/actions/workflows/documind-dryrun.yml/runs?per_page=3"
    runs = json.load(urllib.request.urlopen(url, timeout=30))["workflow_runs"]
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    print("your kit is at", head[:7])
    for r in runs:
        mark = "  <- the commit you run" if r["head_sha"] == head else ""
        print(f"  {r['head_sha'][:7]}  {r['event']:5} {r['conclusion'] or r['status']:8} {r['created_at'][:10]}{mark}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
