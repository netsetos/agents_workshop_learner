"""Lesson 13.2: demo 02 reports and alert policy

Reconcile reported values and inspect the current paging policy.

Run order inside this file:
1. Do it (source window 13)
2. Do it: what pages you today (source window 15)

Prerequisites: demo_01_usage_events_and_features.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only: Cloud Logging and one small BigQuery query).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import datetime as dt, json, os, subprocess, sys
    sys.path.insert(0, "evals")
    from usage_rows import USD_INR, group                       # make usage's own GROUP BY, and its rate
    P = os.environ["PROJECT"]
    KEYS = ("tenant", "surface", "model_backend", "prompt_version", "retrieval_mode", "retrieval_backend", "modality")   # the view's, less the day
    IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
    midnight = dt.datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0)
    since = midnight.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    flt = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND '
           f'(jsonPayload.event="query" OR jsonPayload.event="stream" OR jsonPayload.event="media") AND timestamp>="{since}"')
    log = subprocess.run(["gcloud", "logging", "read", flt, "--project", P, "--limit", "5000", "--format=json"],
                         capture_output=True, text=True, check=True).stdout
    rows = [e["jsonPayload"] for e in json.loads(log or "[]")]
    tool = {tuple(str(g[k]) for k in KEYS): g for g in group(rows, KEYS)}
    sql = "SELECT * EXCEPT(day) FROM `documind_observability.tenant_daily` WHERE day = CURRENT_DATE('Asia/Kolkata')"
    out = subprocess.run(["bq", "--project_id", P, "query", "--use_legacy_sql=false", "--format=json", "--max_rows=1000", sql],
                         capture_output=True, text=True, check=True).stdout
    view = {tuple(str(r[k]) for k in KEYS): r for r in json.loads(out or "[]")}
    print(f"today since 00:00 IST: {len(rows)} usage rows in Cloud Logging, {len(view)} tenant_daily rows")
    print(f"  {'group (the view GROUP BY)':42} {'answers':>9} {'refused':>7} {'tokens in':>11} {'Rs':>11}")
    agree, totals = True, {}
    for k in sorted(set(tool) | set(view)):
        t, v = tool.get(k), view.get(k)
        tv = (t["answers"], round(t["unanswerable_rate"] * t["answers"]), t["tokens_in"], t["tokens_out"], t["inr"]) if t else None
        vv = (int(v["queries"]), int(v["unanswerable"]), int(v["tokens_in"]), int(v["tokens_out"]), float(v["cost_inr"])) if v else None
        same = tv is not None and vv is not None and tv[:4] == vv[:4] and abs(tv[4] - vv[4]) < 0.005
        agree &= same
        for side, x in (("view", vv), ("tool", tv)):
            totals.setdefault(k[0], {"view": 0.0, "tool": 0.0})[side] += x[4] if x else 0.0
        cell = lambda a, b: f"{a}/{b}"
        print(f"  {' '.join(k)[:42]:42} {cell(vv and vv[0], tv and tv[0]):>9} {cell(vv and vv[1], tv and tv[1]):>7} "
              f"{cell(vv and vv[2], tv and tv[2]):>11} {cell(vv and vv[4], tv and tv[4]):>11}  {'equal' if same else 'DIFFERENT'}")
    print("  (each pair is tenant_daily/make usage's grouping; p95 is left out: the view's APPROX_QUANTILES is not the tool's nearest rank)")
    for tenant, s in sorted(totals.items()):
        print(f"{tenant}: tenant_daily Rs {s['view']:.2f}, make usage's grouping Rs {s['tool']:.2f} - " + ("equal" if abs(s['view'] - s['tool']) < 0.005 else "DIFFERENT"))
    media = [r for r in rows if r.get("event") == "media"]
    print(f"media rows today: {len(media)}" + (f" (Rs {sum(r['cost_usd'] for r in media) * USD_INR:.2f}) - make usage counts them, the sink never copies them" if media else ""))
    print("RECONCILED: every group equal in answers, refusals, tokens and rupees" if agree else "NOT RECONCILED: read the DIFFERENT rows")

def step_02_what_pages_you_today(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_example),
        ('source_15', step_02_what_pages_you_today),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
