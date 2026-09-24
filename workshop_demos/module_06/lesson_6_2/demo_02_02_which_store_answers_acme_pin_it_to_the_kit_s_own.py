"""Lesson 6.2 / s2: Before you run anything: set up the shell

Summary and purpose:
Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The model, its location, the tuned base, the router, the backend, the prompt version and the answer's reserve live in the API's environment, each with a default the page names; a name the service does not set is unset rather than exported empty, because steps 3 and 6 import the kit. /version says what is actually serving.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: model: gemini-3.6-flash (default)  location: from the model: global for a name  base: none, no tuned endpoint
routing: off (default)  backend: vertex (default)  prompt: v3 (default)  answer: 2,048 (default)
version: gemini-3.6-flash | documind-rag@v3 | vertex

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L387

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The model, its location, the tuned base, the router, the backend, the prompt version and the answer's reserve live in the API's environment, each with a default the page names; a name the service does not set is unset rather than exported empty, because steps 3 and 6 import the kit. /version says what is actually serving.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT, once per shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.service_environment('documind-api', ['GENERATOR_MODEL', 'GENERATOR_LOCATION', 'RAG_MODEL_BASE', 'ROUTING', 'MODEL_BACKEND', 'PROMPT_VERSION', 'MAX_ANSWER_TOKENS'])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
