"""Lesson 9.2 / s7: The corpus comes back: version 1, and the old answer with it

Summary and purpose:
Every row of the walk

HTML instruction: bash — run in the operator shell, in the kit (every acme usage row since the start; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_the_corpus_comes_back_version_1_and_the_old_answ
Expected observation: 00041-kqz  vertex  in  43109  cached  41259  Rs 1.0201   2480 ms
  00045-tqm  vertex  in  43109  cached  41259  Rs 1.0201   2530 ms
  00045-tqm  cache   in      0  cached      0  Rs 0.0000    170 ms
  00045-tqm  vertex  in  43349  cached  41259  Rs 1.0507   2610 ms
  00045-tqm  vertex  in  43109  cached  41259  Rs 1.0201   2440 ms
  00041-kqz  vertex  in   1880  cached      0  Rs 0.4978   2390 ms
  00045-tqm  vertex  in   1880  cached      0  Rs 0.4978   2455 ms
  00041-kqz  vertex  in  43139  cached  41259  Rs 1.0239   2575 ms
  00045-tqm  cache   in      0  cached      0  Rs 0.0000    165 ms

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L642

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Every row of the walk at this checkpoint.

    Every row of the walk

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every acme usage row since the start; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
         f'AND jsonPayload.tenant="acme" AND timestamp>="{os.environ["SINCE92"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    for e in json.loads(out or "[]"):
        j, rev = e["jsonPayload"], e["resource"]["labels"]["revision_name"]
        print(f"  {rev[-9:]}  {j['model_backend']:6}  in {j['tokens_in']:>6}  cached {j['cached_tokens']:>6}  Rs {j['cost_usd'] * 85:.4f}  {j['latency_ms']:>5} ms")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
