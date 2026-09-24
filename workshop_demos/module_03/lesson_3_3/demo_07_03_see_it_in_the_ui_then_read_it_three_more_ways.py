"""Lesson 3.3 / s7: Carry-over: re-issue the handbook, embed only what changed

Summary and purpose:
Refresh Documents. The handbook's row in the Versions table now reads reused 281, embedded 2, retired 283, with an effective date of 1 October 2026 that the revision declares in its first lines. The first call below is the same row from the API; the second reads the rows themselves and checks the thing the counts claim: an unchanged clause's new row carries the same numbers as its retired predecessor, and a changed clause's does not. The third asks the question the revision changed the answer to.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_do_it_on_the_lane_revision_2_over_the_same_name
Expected observation: acme/hr_policy_2026.md chunks 283 reused 281 embedded 2 retired 283 effective 2026-10-01 text-embedding-005@1
rows for the source: 566 | current: 283 | retired: 283
  LV-01     hash ff463cede286 -> ff463cede286   same vector: True
  NP-03     hash f4512754ae41 -> 876232171dec   same vector: False
  preamble  hash 903e2b39ee92 -> b4736d2f3e52   same vector: False
A confirmed employee at grade E3 or above serves a notice period of 90 days ... [Source 1]
[('1', 'hr_policy_2026.md'), ('2', 'hr_policy_2026.md')] vector

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L883

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; [print(r['name'], 'chunks', r['chunks'], 'reused', r['reused'], 'embedded', r['embedded'], 'retired', r['retired'], 'effective', r['effective_from'], r['embedding']) for r in json.load(sys.stdin)['sources'] if r['name'].endswith('hr_policy_2026.md')]"

python - <<'PY'
import os, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
PROJECT = os.environ["PROJECT"]
db = firestore.Client(project=PROJECT)
rows = [s.to_dict() for s in db.collection("chunks").where("tenant_id", "==", "acme")
        .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md").stream()]
print("rows for the source:", len(rows), "| current:", sum(r["current"] for r in rows), "| retired:", sum(not r["current"] for r in rows))
for loc in ("LV-01", "NP-03", "preamble"):
    cur = next(r for r in rows if r["locator"] == loc and r["current"])
    old = max((r for r in rows if r["locator"] == loc and not r["current"]), key=lambda r: r["indexed_at"])
    print(f"  {loc:9} hash {old['chunk_hash'][:12]} -> {cur['chunk_hash'][:12]}   same vector: {list(old['embedding']) == list(cur['embedding'])}")
PY

curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"How many days of notice does a confirmed employee at grade E3 serve?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:140]); print([(c['chunk_id'].split('#')[1], c['source_uri'].split('/')[-1]) for c in j['citations'][:2]], j['stages']['retrieval_backend'])"
"""


def demonstrate(session):
    """Run See it in the UI, then read it three more ways at this checkpoint.

    Refresh Documents. The handbook's row in the Versions table now reads reused 281, embedded 2, retired 283, with an effective date of 1 October 2026 that the revision declares in its first lines. The first call below is the same row from the API; the second reads the rows themselves and checks the thing the counts claim: an unchanged clause's new row carries the same numbers as its retired predecessor, and a changed clause's does not. The third asks the question the revision changed the answer to.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
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
