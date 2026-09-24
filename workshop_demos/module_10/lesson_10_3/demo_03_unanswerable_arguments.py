"""Lesson 10.3: demo 03 unanswerable arguments

Send an argument the corpus cannot satisfy and inspect its returned failure.

Run order inside this file:
1. Do it (source window 17)

Prerequisites: demo_02_chat_access_failures.
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
COMMANDS_01 = """export SINCE103="$(date -u +%FT%TZ)"
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" RAG_API_URL="$API" python - <<'PY'
from shared.documind_tools import retrieve
for doc_type in (None, "invoice"):
    r = retrieve("What is the total payable on invoice INV-2026-0412?", tenant_id="acme", top_k=5, doc_type=doc_type)
    print(f"  doc_type {str(doc_type):8} {len(r['citations'])} citations | answerable {r['answerable']} | {(r.get('answer') or '')[:58]}")
PY
sleep 20   # Cloud Logging needs a moment to show the rows
python - <<'PY'
import json, os, subprocess
f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
     f'AND jsonPayload.tenant="acme" AND timestamp>="{os.environ["SINCE103"]}"')
out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "10",
                      "--format", "json"], capture_output=True, text=True, check=True).stdout
for e in json.loads(out or "[]"):
    j = e["jsonPayload"]
    print(f"  pool {j['pool']:>2}  answerable {str(j['answerable']):5}  backend {j['model_backend']:6}  Rs {j['cost_usd'] * 85:.4f}")
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one question with and without a doc_type filter, then rag-api's rows).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
