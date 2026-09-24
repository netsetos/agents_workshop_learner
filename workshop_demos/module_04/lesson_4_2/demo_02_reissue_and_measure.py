"""Lesson 4.2: demo 02 reissue and measure

Upload revision 3 and inspect its ledger, claims and reused vectors.

Run order inside this file:
1. Do it (source window 15)
2. Read the three (source window 17)

Prerequisites: demo_01_gate_and_reuse_plan.
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
COMMANDS_01 = """python - <<'PY'
import os, hashlib
v1 = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
r3 = v1.replace("# ACME Employee Handbook 2026\\n", "# ACME Employee Handbook 2026 (revision 3)\\n\\nEffective from: 2026-11-01. Revision 3 changes NP-03: the notice period for a confirmed E3 becomes 90 days.\\n", 1)
r3 = r3.replace("serves a notice period of 60 days", "serves a notice period of 90 days", 1)
path = os.path.expanduser("~/hr_policy_2026_rev3.md")
open(path, "w", encoding="utf-8", newline="\\n").write(r3)
print(path, "| version key acme_" + hashlib.sha256(r3.encode("utf-8")).hexdigest()[:12] + "...")
PY

make reindex PROJECT=$PROJECT TENANT=acme FILE=$HOME/hr_policy_2026_rev3.md NAME=hr_policy_2026.md

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (writes the revision to your home directory, then one re-issue).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_read_the_three.
COMMANDS_02 = """curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; [print(r['name'], 'chunks', r['chunks'], 'reused', r['reused'], 'embedded', r['embedded'], 'retired', r['retired'], 'effective', r['effective_from'], r['embedding']) for r in json.load(sys.stdin)['sources'] if r['name'].endswith('hr_policy_2026.md')]"

python - <<'PY'
import os, hashlib, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
PROJECT = os.environ["PROJECT"]
db = firestore.Client(project=PROJECT)
uri = f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md"
v1key = "acme_" + hashlib.sha256(open("evals/corpus/acme/hr_policy_2026.md", "rb").read()).hexdigest()
claims = sorted(((s.id, s.to_dict()) for s in db.collection("documents").where("gcs_uri", "==", uri).stream()),
                key=lambda kv: str(kv[1].get("claimed_at") or ""))
print(len(claims), "claims (versions) for hr_policy_2026.md, oldest first")
for key, d in claims:
    tail = (f"  superseded_by {str(d.get('superseded_by'))[:13]}..." if d.get("superseded_by") else "") + ("  reactivated once" if d.get("reactivated_at") else "")
    print(f"  {key[:13]}...  {d.get('status'):10} chunks {d.get('chunks')}  reused {d.get('reused')}  embedded {d.get('embedded')}{tail}")
rows = [r.to_dict() for r in db.collection("chunks").where("tenant_id", "==", "acme").where("source_uri", "==", uri).stream()]
cur = {r["locator"]: r for r in rows if r.get("current")}
v1 = {r["locator"]: r for r in rows if r.get("doc_key") == v1key}
print("rows:", len(rows), "| current:", len(cur), "| retired:", len(rows) - len(cur))
for loc in ("LV-01", "NP-03"):
    print(f"  {loc:6} current hash {cur[loc]['chunk_hash'][:12]}  version 1's hash {v1[loc]['chunk_hash'][:12]}  same vector: {list(cur[loc]['embedding']) == list(v1[loc]['embedding'])}")
PY

"""

def step_02_read_the_three(session):
    """Run Read the three at this checkpoint.

    Read the three

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the ledger row from the API, then the claims and the vectors from Firestore).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_15', step_01_example),
        ('source_17', step_02_read_the_three),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
