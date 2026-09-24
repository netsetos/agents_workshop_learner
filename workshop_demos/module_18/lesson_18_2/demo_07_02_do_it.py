"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a no-traffic revision; the live one keeps its settings)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it
Expected observation: gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=documind-slm|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=gateway|ARMOR=off|SEMANTIC_CACHE=off|RETRIEVAL_CURRENT_ONLY=off|RETRIEVAL_GRAPH=off|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-xxx (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L757

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make candidate PROJECT="$PROJECT" MODEL_BACKEND=gateway GENERATOR_MODEL=documind-slm
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a no-traffic revision; the live one keeps its settings).
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
