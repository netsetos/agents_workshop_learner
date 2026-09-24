"""Lesson 15.4: demo 02 update freshness

Change the source and inspect when each retrieval store sees the new version.

Run order inside this file:
1. Do it (source window 13)
2. Do it (source window 16)

Prerequisites: demo_01_mirror_freshness_contract.
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
COMMANDS_01 = """sed 's/serves a notice period of 30 days/serves a notice period of 45 days/' evals/corpus/zeta/hr_policy_zeta_2026.md > "$HOME/hr_policy_zeta_2026_v2.md"
export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make reindex PROJECT="$PROJECT" TENANT=zeta FILE="$HOME/hr_policy_zeta_2026_v2.md" NAME=hr_policy_zeta_2026.md
fresh154() {   # fresh154 STATUS: the mirror's audit trail since $SINCE, make managed-status until the stores match, zeta asked
python - "$@" <<'PY'
import datetime as dt, json, os, re, subprocess, sys, time, urllib.request
from google.cloud import firestore, storage
P, API, SINCE, WANT = os.environ["PROJECT"], os.environ["API"], os.environ["SINCE"], sys.argv[1]
NAME, Q = "zeta/hr_policy_zeta_2026.md", "How long is the notice period for a confirmed employee?"
short = lambda s: re.sub(r"([0-9a-f]{8})[0-9a-f]{56}", r"\\1...", s)
since = dt.datetime.fromisoformat(SINCE.replace("Z", "+00:00"))
audit, events = storage.Client(project=P).bucket(f"{P}-audit"), []
for day in sorted({since.date(), dt.datetime.now(dt.timezone.utc).date()}):
    for b in audit.list_blobs(prefix=f"{day:%Y/%m/%d}/zeta/doc.mirror-"):
        if b.time_created >= since:
            events.append(json.loads(b.download_as_text()))
print(f"the mirror's doc.mirror events for zeta since {SINCE} (the audit bucket):")
for e in sorted(events, key=lambda e: e["ts"]):
    m = e["meta"]
    print(f"  {e['ts'][11:19]}  {m['op']:17} {m['store']:13} {m['region']:11} {short(e['target']['id'])}")
if not events:
    print("  none")
print(f"make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook {WANT}):")
db, start, last = firestore.Client(project=P), time.monotonic(), None
while True:
    out = subprocess.run(["make", "-s", "managed-status", f"PROJECT={P}", "TENANT_ONLY=zeta"], capture_output=True, text=True, check=True).stdout
    lines = [json.loads(line) for line in out.splitlines() if line.startswith("{")]
    status = (db.collection("sources").document(NAME.replace("/", "~")).get().to_dict() or {}).get("status")
    state = f"handbook {status}; " + "; ".join(s["store"] + " " + s["status"] + "".join(
        f", {k} {' '.join(short(x) for x in s[k + '_doc_keys'])}" for k in ("missing", "orphan") if s.get(k + "_doc_keys")) for s in lines)
    t = int(time.monotonic() - start)
    if state != last:
        print(f"  {t // 60}:{t % 60:02d}  {state}")
        last = state
    if status == WANT and lines and all(s["status"] == "in sync" for s in lines):
        break
    if t > 900:
        raise SystemExit("still apart after 15 minutes: make managed-status TENANT_ONLY=zeta")
    time.sleep(20)
for s in lines:
    print(json.dumps(s))
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
req = urllib.request.Request(API + "/v1/query", data=json.dumps({"query": Q, "tenant_id": "zeta"}).encode(),
                             headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
a = json.load(urllib.request.urlopen(req, timeout=180))
print(f"zeta, answered from {a['stages']['retrieval_backend']}: {a['answer']}")
for c in a["citations"]:
    print(f"  cites {short(c['chunk_id'])}")
PY
}
fresh154 indexed

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a second version of zeta's handbook, then the check).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make reindex PROJECT="$PROJECT" TENANT=zeta FILE=evals/corpus/zeta/hr_policy_zeta_2026.md NAME=hr_policy_zeta_2026.md
fresh154 indexed

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Now the undo: the same name, with the first version's bytes, straight from the kit's corpus. This is the worker's branch for a version it has seen before:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the first version's bytes again, then the check).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_example),
        ('source_16', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
