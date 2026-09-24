"""Lesson 5.1 / s7: Current is the ledger's filter, never the caller's

Summary and purpose:
Do it: the question the revisions answered differently

HTML instruction: bash — run in the operator shell (one question, then the cited row read off Firestore)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_tenant_s_pin_and_policy_then_a_full_st
Expected observation: A confirmed employee at grade E3 or above serves a notice period of 60 days ... [Source 1]
cited acme:497809ffbaa6...#1
the cited row: NP-03 | current: True | doc_key: acme_497809ff... | text starts: NP-03 — Notice period A confirmed employee at grade E3 or above
NP-03 rows on the lane: 3 | current: 1 | saying 90 days: 2 (retired, never cited)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L860

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
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


def demonstrate(session):
    """Run Do it: the question the revisions answered differently at this checkpoint.

    Do it: the question the revisions answered differently

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question, then the cited row read off Firestore).
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
