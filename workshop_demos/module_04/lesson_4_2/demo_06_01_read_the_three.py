"""Lesson 4.2 / s6: Inspect: the ledger row, the claims, the vectors

Summary and purpose:
Read the three

HTML instruction: bash — run in the operator shell (the ledger row from the API, then the claims and the vectors from Firestore)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: acme/hr_policy_2026.md chunks 283 reused 281 embedded 2 retired 283 effective 2026-11-01 text-embedding-005@1
3 claims (versions) for hr_policy_2026.md, oldest first
  acme_497809ff...  superseded chunks 283  reused 0  embedded 283  superseded_by acme_54337b4b...  reactivated once
  acme_55603088...  superseded chunks 283  reused 281  embedded 2  superseded_by acme_497809ff...
  acme_54337b4b...  indexed    chunks 283  reused 281  embedded 2
rows: 849 | current: 283 | retired: 566
  LV-01  current hash ff463cede286  version 1's hash ff463cede286  same vector: True
  NP-03  current hash 876232171dec  version 1's hash f4512754ae41  same vector: False

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html#L590

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
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


def demonstrate(session):
    """Run Read the three at this checkpoint.

    Read the three

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the ledger row from the API, then the claims and the vectors from Firestore).
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
