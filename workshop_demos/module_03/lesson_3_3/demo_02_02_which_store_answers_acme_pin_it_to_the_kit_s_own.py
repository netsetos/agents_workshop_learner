"""Lesson 3.3 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. Steps 6 and 7 import the worker's own indexer.py, which imports the Vector Search and Gemini SDKs at the top. The setup block installed only the Firestore client; add the other two once. Nothing in this lesson writes to Vector Search.

HTML instruction: bash — run in the operator shell, once
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L428

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q google-cloud-aiplatform google-genai && python -c "import google.cloud.aiplatform, google.genai; print('ok')"
"""


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. Steps 6 and 7 import the worker's own indexer.py, which imports the Vector Search and Gemini SDKs at the top. The setup block installed only the Firestore client; add the other two once. Nothing in this lesson writes to Vector Search.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, once.
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
