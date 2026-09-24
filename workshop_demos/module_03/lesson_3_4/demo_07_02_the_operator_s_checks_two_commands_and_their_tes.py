"""Lesson 3.4 / s7: Verify: the two rungs that read the records

Summary and purpose:
The kit ships two read-only commands for exactly this lesson. verify-vector-index.py reads Terraform's outputs and asks the API whether the index Terraform declared is the one attached to the endpoint, streaming, 768-dimensional, deployed exactly once; it needs a checkout with Terraform state, and the two gcloud reads in step 5 are the same checks by hand. check-firestore-fallback.py takes the handbook, proves the ledger row names the bytes in your checkout, and runs the Firestore rung with combined filters in both current modes; it imports the API's own modules, so it needs the API's packages in your venv. Both write their evidence under operator-evidence/. Their tests run offline in a fraction of a second.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (all read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_the_fallback_rung_then_the_api
Expected observation: Project: documind-ai-YOUR-ID (NUMBER)
Terraform index: projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
Terraform endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321
API index: projects/NUMBER/locations/asia-south1/indexes/1234567890123456789
API endpoint: projects/NUMBER/locations/asia-south1/indexEndpoints/9876543210987654321
Index dimensions: 768; update method: STREAM_UPDATE
Global vector count: 1745
Deployment: documind_chunks_v1
Deployment sync time: 2026-09-22T10:41:07.000Z
PASS: the expected index is attached to the expected endpoint.
This verifies attachment and configuration; ingestion and query checks are separate.
{"project": "documind-ai-YOUR-ID", "collection": "chunks", "source_uri": "gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md", "source_status": "indexed", "source_doc_key": "acme_..."}
Ve

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L914

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python commands/verify-vector-index.py --deploy-root "$DEMO_ROOT" --project "$PROJECT" --region "$REGION"

GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py

python -m unittest discover -s commands/tests -p test_verify_vector_index.py
python -m unittest discover -s commands/tests -p test_check_firestore_fallback.py
"""


def demonstrate(session):
    """Run The operator's checks: two commands, and their tests at this checkpoint.

    The kit ships two read-only commands for exactly this lesson. verify-vector-index.py reads Terraform's outputs and asks the API whether the index Terraform declared is the one attached to the endpoint, streaming, 768-dimensional, deployed exactly once; it needs a checkout with Terraform state, and the two gcloud reads in step 5 are the same checks by hand. check-firestore-fallback.py takes the handbook, proves the ledger row names the bytes in your checkout, and runs the Firestore rung with combined filters in both current modes; it imports the API's own modules, so it needs the API's packages in your venv. Both write their evidence under operator-evidence/. Their tests run offline in a fraction of a second.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (all read-only).
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
