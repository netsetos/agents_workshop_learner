"""Lesson 7.3 / s3: The candidate: a new revision with no traffic, and the proof that one setting differs

Summary and purpose:
The cell finds the revision serving traffic and the one tagged candidate, reads both revisions' settings, and prints every setting that differs.

HTML instruction: bash — run in the operator shell, in the kit (reads both revisions; changes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_candidate
Expected observation: live documind-api-000NN-xxx   candidate documind-api-000NN-yyy
  GENERATOR_MODEL        gemini-3.6-flash           -> gemini-3.1-flash-lite
1 setting(s) differ

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html#L431

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: prove it is one change at this checkpoint.

    The cell finds the revision serving traffic and the one tagged candidate, reads both revisions' settings, and prints every setting that differs.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads both revisions; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gcloud(*a):
        cmd = ["gcloud", *a, "--region", os.environ["REGION"], "--project", os.environ["PROJECT"], "--format=json"]
        return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    traffic = gcloud("run", "services", "describe", "documind-api")["status"]["traffic"]
    live = max((t for t in traffic if t.get("percent")), key=lambda t: t["percent"])["revisionName"]
    cand = next(t["revisionName"] for t in traffic if t.get("tag") == "candidate")
    env = lambda rev: {e["name"]: e.get("value", "") for e in gcloud("run", "revisions", "describe", rev)["spec"]["containers"][0].get("env", [])}
    a, b = env(live), env(cand)
    print(f"live {live}   candidate {cand}")
    diff = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
    for k in diff:
        print(f"  {k:22} {a.get(k, '(unset)'):26} -> {b.get(k, '(unset)')}")
    print(f"{len(diff)} setting(s) differ" + ("" if len(diff) == 1 else " - not one controlled change yet"))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
