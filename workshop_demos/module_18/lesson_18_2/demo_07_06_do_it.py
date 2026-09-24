"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit, when you are done
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_05_do_it
Expected observation: ...
gcloud run services update documind-slm --region us-central1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
...
documind-slm scaled to zero

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L850

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
rm -f .candidate-revision      # make promote flips to the revision this file names, tag or no tag
make slm-off PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit, when you are done.
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
