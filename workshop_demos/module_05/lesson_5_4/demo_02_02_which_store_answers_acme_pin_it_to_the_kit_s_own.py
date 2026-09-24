"""Lesson 5.4 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index names and the retrieval settings live in the API's environment; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and steps 5 and 6 import the kit. The pins live in Firestore, one document per tenant, and the lane helper prints them.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
backend: vector  mode: dense (default)  current_only: off (default)  top_k_retrieve: 20 (default)
acme: retrieval_backend=vector
zeta: retrieval_backend=default (the deployment RETRIEVAL_BACKEND)
acme: data_region=any

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L404

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index names and the retrieval settings live in the API's environment; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and steps 5 and 6 import the kit. The pins live in Firestore, one document per tenant, and the lane helper prints them.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT, once per shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.service_environment('documind-api', ['VECTOR_INDEX_ENDPOINT', 'VECTOR_DEPLOYED_INDEX_ID', 'RETRIEVAL_BACKEND', 'RETRIEVAL_MODE', 'RETRIEVAL_CURRENT_ONLY', 'TOP_K_RETRIEVE'])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
