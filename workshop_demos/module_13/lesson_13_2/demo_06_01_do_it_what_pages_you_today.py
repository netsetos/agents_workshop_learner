"""Lesson 13.2 / s6: The alert the dead-letter queue never had

Summary and purpose:
Do it: what pages you today

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: log-based metrics on the lane: documind/ingest_embedded, documind/ingest_events, documind/ingest_reused, documind/queries, documind/reconcile_drift, documind/unanswerable
alert policies on the lane: 5, and what each one reads
  API p95 latency > 3s                                 request_latencies on documind-api
  Ingest failed                                        ingest_events on any service
  Unanswerable rate > 20% for a tenant                 unanswerable on any service
  documind-slm left warm: instances > 0 for 2 hours    instance_count on documind-slm
  documind-vllm left warm: instances > 0 for 2 hours   instance_count on documind-vllm
reads the dead-letter queue (ingest-dlq-sub): NOTHING - an upload the worker refused twelve times pages nobody

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.2-usage-reconcile/Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html#L674

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: what pages you today at this checkpoint.

    Do it: what pages you today

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, re, subprocess, urllib.request
    P = os.environ["PROJECT"]
    def gcloud(*a):
        return subprocess.run(["gcloud", *a], capture_output=True, text=True, check=True).stdout
    tok = gcloud("auth", "print-access-token").strip()
    req = urllib.request.Request(f"https://monitoring.googleapis.com/v3/projects/{P}/alertPolicies", headers={"Authorization": "Bearer " + tok})
    policies = json.load(urllib.request.urlopen(req, timeout=60)).get("alertPolicies", [])
    metrics = json.loads(gcloud("logging", "metrics", "list", "--project", P, "--format=json"))
    print("log-based metrics on the lane: " + ", ".join(sorted(m["name"] for m in metrics)))
    print(f"alert policies on the lane: {len(policies)}, and what each one reads")
    dlq = []
    for p in sorted(policies, key=lambda p: p["displayName"]):
        for c in p.get("conditions", []):
            f = (c.get("conditionThreshold") or {}).get("filter", "")
            metric = re.search(r'metric\.type="([^"]+)"', f)
            on = re.search(r'(?:service_name|subscription_id)="([^"]+)"', f)
            print(f"  {p['displayName'][:52]:52} {metric.group(1).rsplit('/', 1)[-1] if metric else '?'} on {on.group(1) if on else 'any service'}")
            if "ingest-dlq-sub" in f:
                dlq.append(p["displayName"])
    print("reads the dead-letter queue (ingest-dlq-sub): " + (", ".join(dlq) or "NOTHING - an upload the worker refused twelve times pages nobody"))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
