"""Lesson 5.1: demo 03 current version evidence

Compare the question answered by successive document versions.

Run order inside this file:
1. Do it: the question the revisions answered differently (source window 25)

Prerequisites: demo_02_filters_and_backend_selection.
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


# Original CLI workflow for step_01_the_question_the_revisions_answered_differ.
COMMANDS_01 = """curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:80]); print('cited', j['citations'][0]['chunk_id'])" | tee /tmp/q51.txt

python - <<'PY'
import os, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
db = firestore.Client(project=os.environ["PROJECT"])
cid = open("/tmp/q51.txt").read().split("cited ")[-1].strip()
row = db.collection("chunks").document(cid).get().to_dict() or {}
print("the cited row:", row.get("locator"), "| current:", row.get("current"), "| doc_key:", str(row.get("doc_key"))[:13] + "...", "| text starts:", row.get("text", "")[:60].replace("\\n", " "))
uri = f"gs://{os.environ['PROJECT']}-uploads/acme/hr_policy_2026.md"
rows = [r.to_dict() for r in db.collection("chunks").where("tenant_id", "==", "acme").where("source_uri", "==", uri).where("locator", "==", "NP-03").stream()]
print("NP-03 rows on the lane:", len(rows), "| current:", sum(bool(r.get("current")) for r in rows), "| saying 90 days:", sum("90 days" in r.get("text", "") for r in rows), "(retired, never cited)")
PY

"""

def step_01_the_question_the_revisions_answered_differ(session):
    """Run Do it: the question the revisions answered differently at this checkpoint.

    Do it: the question the revisions answered differently

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question, then the cited row read off Firestore).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_25', step_01_the_question_the_revisions_answered_differ),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
