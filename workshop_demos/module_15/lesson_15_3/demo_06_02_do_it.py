"""Lesson 15.3 / s6: globex stays home: the skip, the ledger row, and a pin the policy overrides

Summary and purpose:
Then read what the worker's mirror said about the note, and the ledger row it stamped:

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: the worker's mirror lines for globex since 2026-09-24T07:30:00Z:
  07:30:09 mirror_policy_skipped  store rag_engine    region us-central1 data_region in
  07:30:10 mirror_policy_skipped  store vertex_search region global      data_region in
the ledger row for globex/globex_visitor_note_2026.md: status indexed, mirrored {}
globex's data_region, as GET /v1/sources reports it: in

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L765

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Then read what the worker's mirror said about the note, and the ledger row it stamped:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import datetime as dt, json, os, subprocess, urllib.request
    P, API, SINCE = os.environ["PROJECT"], os.environ["API"], os.environ["SINCE"]
    NAME = "globex/globex_visitor_note_2026.md"
    
    
    def logs(extra, limit=20):
        flt = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" '
               'AND jsonPayload.tenant="globex" AND ' + extra)
        out = subprocess.run(["gcloud", "logging", "read", flt, "--project", P, "--format=json", f"--limit={limit}"],
                             capture_output=True, text=True, check=True).stdout
        return sorted(json.loads(out or "[]"), key=lambda e: e["timestamp"])
    
    
    def show(e):
        j = e["jsonPayload"]
        print(f"  {e['timestamp'][11:19]} {j['event']:22} store {j.get('store', '-'):13} region {j.get('region', '-'):11} data_region {j.get('data_region', '-')}")
    
    
    lines = logs(f'jsonPayload.event:"mirror_" AND timestamp>="{SINCE}"')
    print(f"the worker's mirror lines for globex since {SINCE}:")
    for e in lines:
        show(e)
    if not any(e["jsonPayload"]["event"] == "mirror_policy_skipped" for e in lines):
        week = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        print("  none since the upload: this worker instance had said it already (once per tenant and store per instance); the last 7 days:")
        for e in logs(f'jsonPayload.event="mirror_policy_skipped" AND timestamp>="{week}"', 4):
            show(e)
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                         capture_output=True, text=True, check=True).stdout.strip()
    src = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/v1/sources?tenant_id=globex", headers={"Authorization": "Bearer " + tok}), timeout=60))
    row = next(r for r in src["sources"] if r["name"] == NAME)
    print(f"the ledger row for {NAME}: status {row['status']}, mirrored {row['mirrored']}")
    print(f"globex's data_region, as GET /v1/sources reports it: {src['data_region']}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
