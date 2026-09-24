"""Lesson 5.2 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index endpoint, the deployed index and the retrieval settings live in the API's environment; steps 3, 4 and 7 use them. An empty value means the setting's default, which the page names where it matters; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and step 8's cell imports the kit. The ablation's sparse leg needs rank_bm25, which the kit's images do not carry because no service runs it; the pip line puts it in the venv once.

HTML instruction: bash — run in the operator shell, once per shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
mode: dense (default)  backend: vector

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L395

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index endpoint, the deployed index and the retrieval settings live in the API's environment; steps 3, 4 and 7 use them. An empty value means the setting's default, which the page names where it matters; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and step 8's cell imports the kit. The ablation's sparse leg needs rank_bm25, which the kit's images do not carry because no service runs it; the pip line puts it in the venv once.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, once per shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.service_environment('documind-api', ['VECTOR_INDEX_ENDPOINT', 'VECTOR_DEPLOYED_INDEX_ID', 'RETRIEVAL_MODE', 'RETRIEVAL_BACKEND'])
    session.shell('python -m pip install -q rank-bm25==0.2.2')


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
