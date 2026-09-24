"""Lesson 9.3 / s5: Avoided calls in rupees, and the latency of a hit

Summary and purpose:
Do it: the candidate's rows

HTML instruction: bash — run in the operator shell, in the kit (the candidate's rows since the start: hits, p95, rupees; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_replay
Expected observation: 65 answers on the candidate: 10 from the answer cache, 55 from the model
  p95 latency: 236 ms for a hit, 3187 ms for a model answer
  a model answer cost Rs 0.4673 on average: the hits avoided 10 calls, about Rs 4.67
  of those hits, 2 served a wrong answer: pp-25, pp-31

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L592

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the candidate's rows at this checkpoint.

    Do it: the candidate's rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's rows since the start: hits, p95, rupees; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    rev = open(".candidate-revision").read().strip()
    f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
         f'AND resource.labels.revision_name="{rev}" AND timestamp>="{os.environ["SINCE93"]}"')
    rows = [e["jsonPayload"] for e in json.loads(subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"],
            "--limit", "500", "--format", "json"], capture_output=True, text=True, check=True).stdout or "[]")]
    hits, miss = [r for r in rows if r["model_backend"] == "cache"], [r for r in rows if r["model_backend"] != "cache"]
    p95 = lambda v: sorted(v)[max(0, int(round(0.95 * len(v))) - 1)] if v else 0
    rs = sum(r["cost_usd"] for r in miss) / len(miss) * 85 if miss else 0.0
    wrong = [o["id"] for o in json.load(open(os.path.expanduser("~/cache93_replay.json"), encoding="utf-8")) if o["verdict"] == "FALSE HIT"]
    print(f"  {len(rows)} answers on the candidate: {len(hits)} from the answer cache, {len(miss)} from the model")
    print(f"  p95 latency: {p95([r['latency_ms'] for r in hits])} ms for a hit, {p95([r['latency_ms'] for r in miss])} ms for a model answer")
    print(f"  a model answer cost Rs {rs:.4f} on average: the hits avoided {len(hits)} calls, about Rs {len(hits) * rs:.2f}")
    print(f"  of those hits, {len(wrong)} served a wrong answer: {', '.join(wrong) or 'none'}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
