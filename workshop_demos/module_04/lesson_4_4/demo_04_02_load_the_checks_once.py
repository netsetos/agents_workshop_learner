"""Lesson 4.4 / s4: Create this chapter's note and the checks

Summary and purpose:
The helper block is preparation, not a slide to type live. It stops on failed uploads, polls the exact source and generation, checks citations, and refuses to apply an unexplained tenant-wide plan. The log filter includes both the version key and generation, so another acme upload cannot satisfy the wait. To resume after reopening a shell, first run the shared shell setup, then source this directory's session.env and helpers.sh; do not create a new note midway through a restore.

HTML instruction: bash — save and load the chapter checks; no cloud writes in this block
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_create_this_chapter_s_note_and_the_checks
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L544

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """cat > "$DEMO_DIR/helpers.sh" <<'SH'
set -o pipefail

ch44_source() {
  local token
  token="$(tok "$API")" || return
  curl -fsS "$API/v1/sources?tenant_id=acme" \\
    -H "Authorization: Bearer $token" |
    python -c 'import json,sys
j=json.load(sys.stdin)
r=next((r for r in j["sources"] if r["name"]==sys.argv[1]),None)
print(json.dumps(r,indent=2))' "$SOURCE" > "$DEMO_DIR/source.json" || return
  cat "$DEMO_DIR/source.json"
}

ch44_ask() {
  local token
  token="$(tok "$API")" || return
  curl -fsS "$API/v1/query" -H "Authorization: Bearer $token" \\
    -H "Content-Type: application/json" \\
    --data-binary @"$DEMO_DIR/query.json" > "$DEMO_DIR/answer.json" || return
  python - "$1" <<'PY'
import json, os, sys
from pathlib import Path
j=json.loads(Path(os.environ["DEMO_DIR"], "answer.json").read_text())
backend=j.get("stages", {}).get("retrieval_backend")
cited=any(c.get("source_uri")==os.environ["OBJECT"] for c in j.get("citations", []))
print("retrieval:", backend, "| answerable:", j["answerable"], "| fixture cited:", cited)
print(j["answer"])
for c in j.get("citations", []):
    print("citation:", c.get("source_uri"), "|", c.get("quote", ""))
assert backend=="vector", "Wait for the backend pin to refresh; inspect the returned stages."
if sys.argv[1]=="present":
    assert j["answerable"] and cited, "The answer must cite this exact fixture."
    assert "Q7" in j["answer"] and "Jaipur" in j["answer"], "Check the fixture's stated location."
else:
    assert not cited, "The retired fixture is still cited; inspect retrieval and propagation."
    if j["answerable"]:
        print("Another source answered. This is not proof that the fixture is still indexed.")
PY
}

ch44_logs() {
  gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.doc_key=\\"$DOC_KEY\\" AND jsonPayload.generation=\\"$CH44_GENERATION\\" AND timestamp>=\\"$CH44_SINCE\\"" \\
    --project "$PROJECT" --limit 10 \\
    --format='table(timestamp,jsonPayload.event,jsonPayload.chunks,jsonPayload.reused,jsonPayload.embedded,jsonPayload.error)'
}

ch44_upload() {
  sha256sum -c "$DEMO_DIR/note.sha256" || return
  export CH44_SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  gcloud storage cp "$NOTE" "$OBJECT" || return
  CH44_GENERATION="$(gcloud storage objects describe "$OBJECT" --format='value(generation)')" || return
  export CH44_GENERATION
  [ -n "$CH44_GENERATION" ] || return 1
  for attempt in $(seq 1 30); do
    ch44_source > /dev/null || return
    if python - <<'PY'
import json, os, sys
from pathlib import Path
r=json.loads(Path(os.environ["DEMO_DIR"], "source.json").read_text()) or {}
ready=(r.get("status")=="indexed"
       and str(r.get("generation"))==os.environ["CH44_GENERATION"]
       and r.get("doc_key")==os.environ["DOC_KEY"])
sys.exit(0 if ready else 1)
PY
    then cat "$DEMO_DIR/source.json"; return 0; fi
    sleep 10
  done
  echo "STOP: this upload did not reach indexed state within five minutes."
  ch44_logs
  return 1
}

ch44_plan() {
  make --no-print-directory reconcile PROJECT="$PROJECT" TENANT_ONLY=acme \\
    > "$DEMO_DIR/plan.txt" || { cat "$DEMO_DIR/plan.txt"; return 1; }
  cat "$DEMO_DIR/plan.txt"
  python - "$1" <<'PY'
import json, os, sys
from pathlib import Path
rows=[json.loads(s) for s in Path(os.environ["DEMO_DIR"], "plan.txt").read_text().splitlines()
      if s.startswith("{")]
summary=next(r for r in reversed(rows) if r.get("event")=="reconcile_done")
repairs=[r for r in rows if r.get("reconcile") in ("retire","reingest","backfill","touch")]
assert summary.get("applied") is False, "Expected a read-only plan."
if sys.argv[1]=="clean":
    assert summary["drift"]==0 and not repairs, "Resolve unrelated repairs before the live demo."
else:
    assert len(repairs)==1 and repairs[0]["reconcile"]=="retire" \\
        and repairs[0]["name"]==os.environ["SOURCE"], "STOP: plan includes unexpected work."
    assert summary["drift"]==1
print("Checkpoint passed:", sys.argv[1])
PY
}
SH
source "$DEMO_DIR/helpers.sh"
ch44_plan clean
"""


def demonstrate(session):
    """Run Load the checks once at this checkpoint.

    The helper block is preparation, not a slide to type live. It stops on failed uploads, polls the exact source and generation, checks citations, and refuses to apply an unexplained tenant-wide plan. The log filter includes both the version key and generation, so another acme upload cannot satisfy the wait. To resume after reopening a shell, first run the shared shell setup, then source this directory's session.env and helpers.sh; do not create a new note midway through a restore.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — save and load the chapter checks; no cloud writes in this block.
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
