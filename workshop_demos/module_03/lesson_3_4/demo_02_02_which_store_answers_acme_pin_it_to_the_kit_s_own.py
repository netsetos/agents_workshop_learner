"""Lesson 3.4 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index, the endpoint, the BigQuery table and the audit bucket are named in the environment of the two services that use them. Read them once into the shell; every cell below uses these variables. Both reads are read-only.

HTML instruction: bash — run in the operator shell, once per shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: index:    projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
mirror:   documind-ai-YOUR-ID.rag_data.chunk_source  audit: documind-ai-YOUR-ID-audit

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L383

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """svc_env() { gcloud run services describe "$1" --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep "'name': '$2'" | sed -nE "s/.*'value': '([^']*)'.*/\\1/p"; }   # -n ... p: an entry with an empty value prints nothing
export VECTOR_INDEX_NAME="$(svc_env documind-ingest VECTOR_INDEX_NAME)" BQ_CHUNK_TABLE="$(svc_env documind-ingest BQ_CHUNK_TABLE)" AUDIT_BUCKET="$(svc_env documind-ingest AUDIT_BUCKET)"
export VECTOR_INDEX_ENDPOINT="$(svc_env documind-api VECTOR_INDEX_ENDPOINT)" VECTOR_DEPLOYED_INDEX_ID="$(svc_env documind-api VECTOR_DEPLOYED_INDEX_ID)"
echo "index:    $VECTOR_INDEX_NAME"; echo "endpoint: $VECTOR_INDEX_ENDPOINT  deployed: $VECTOR_DEPLOYED_INDEX_ID"
echo "mirror:   $BQ_CHUNK_TABLE  audit: $AUDIT_BUCKET"
"""


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index, the endpoint, the BigQuery table and the audit bucket are named in the environment of the two services that use them. Read them once into the shell; every cell below uses these variables. Both reads are read-only.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, once per shell.
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
