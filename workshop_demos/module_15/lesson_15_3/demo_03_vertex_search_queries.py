"""Lesson 15.3: demo 03 vertex search queries

Query the Vertex AI Search mirror, compare its records and restore the pin.

Run order inside this file:
1. Do it (source window 21)
2. Do it (source window 23)
3. Do it (source window 25)

Prerequisites: demo_02_rag_engine_queries.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """cat > "$HOME/globex_visitor_note.md" <<EOF
# Globex visitor note

Visitors to the Globex office sign the register at reception and wear a visitor badge at all times.

Written by $ME on $(date -u +%Y-%m-%dT%H:%M:%SZ) for lesson 15.3.
EOF
export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make reindex PROJECT="$PROJECT" TENANT=globex FILE="$HOME/globex_visitor_note.md" NAME=globex_visitor_note_2026.md

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a note to globex, whose text may not leave India).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_example(session):
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

# Original CLI workflow for step_03_example.
COMMANDS_03 = """make tenant-backend PROJECT="$PROJECT" TENANT=globex RETRIEVAL_BACKEND=rag_engine
sleep 60      # the API reads a tenant's settings once a minute per instance
ask153 globex
make tenant-backend PROJECT="$PROJECT" TENANT=globex RETRIEVAL_BACKEND=default

"""

def step_03_example(session):
    """Run Do it at this checkpoint.

    If your lines are missing, the worker instance that took the note had already said it: the skip is said once per tenant and store per instance. The cell then prints the last week's lines instead, and the empty mirrored on the row is the record for this document. Last, try to move globex's text with a pin:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (globex pinned to a store for one question, then unpinned).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_example),
        ('source_23', step_02_example),
        ('source_25', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
