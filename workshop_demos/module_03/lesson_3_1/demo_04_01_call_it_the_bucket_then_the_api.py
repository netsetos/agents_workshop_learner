"""Lesson 3.1 / s4: Source: the object path is the document's identity

Summary and purpose:
The source lives in two places that must agree: the object in the bucket, and the ledger row. Cloud Storage numbers every rewrite of an object with a generation; the ledger records the generation it indexed. List the tenant's folder, describe one object, then ask the API for the ledger.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_03_read_it_in_firestore
Expected observation: gs://documind-ai-YOUR-ID-uploads/acme/annual_report_2026.md
gs://documind-ai-YOUR-ID-uploads/acme/code_on_wages_2019.pdf
gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md
...
1758540123456789    40096    text/markdown
{
    "tenant_id": "acme",
    "versions": 18,
    "fingerprint": "3fd2258b1264f744",
    "last_event": "ingest_ok",
    "data_region": "any",
    "sources": [
        {
            "name": "acme/hr_policy_2026.md",
            "status": "indexed",
            "doc_key": "acme_497809ff...",
            "generation": "1758540123456789",
            "chunks": 283,
            "reused": 0,
            "embedded": 283,
            "retired": 0,
            "effective_from": null,
            "embedding": "text-embedding-005@1",
            "indexed_at": "2026-09-22T...",
            "mirrored": {}
        },
        ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L557

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud storage ls gs://$PROJECT-uploads/acme/
gcloud storage objects describe gs://$PROJECT-uploads/acme/hr_policy_2026.md \\
  --format='value(generation,size,content_type)'
curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok $API)" | python -m json.tool | head -40
"""


def demonstrate(session):
    """Run Call it: the bucket, then the API at this checkpoint.

    The source lives in two places that must agree: the object in the bucket, and the ledger row. Cloud Storage numbers every rewrite of an object with a generation; the ledger records the generation it indexed. List the tenant's folder, describe one object, then ask the API for the ledger.

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
