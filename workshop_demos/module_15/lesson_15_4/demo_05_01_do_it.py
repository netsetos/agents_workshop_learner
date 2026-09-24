"""Lesson 15.4 / s5: A new version, then the undo

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a second version of zeta's handbook, then the check)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: ...
>> gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	zeta_025c4143c0a1115dda29f3556faff8cbe552249f4576c78036ea07a80f9be422	283	282	1	283	
>> retired (doc_keys, chunks, expire days): zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a	283	30
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_zeta_2026.md API=<candidate url>
the mirror's doc.mirror events for zeta since 2026-09-24T08:00:00Z (the audit bucket):
  08:00:48  upsert            rag_engine    us-central1 zeta_025c4143...
  08:00:48  upsert            vertex_search global      zeta_025c4143...
  08:00:49  delete:superseded rag_engine    us-central1 zeta_e920a147...
  08:00:49  delete:superseded vertex_search global      ze

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L670

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sed 's/serves a notice period of 30 days/serves a notice period of 45 days/' evals/corpus/zeta/hr_policy_zeta_2026.md > "$HOME/hr_policy_zeta_2026_v2.md"
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a second version of zeta's handbook, then the check).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
