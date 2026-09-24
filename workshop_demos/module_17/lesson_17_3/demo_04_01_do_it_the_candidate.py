"""Lesson 17.3 / s4: The candidate, audited

Summary and purpose:
Do it: the candidate

HTML instruction: bash — run in the operator shell, in the kit (a revision with no traffic; nothing is billed until it answers)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=projects/NUMBER/locations/us/endpoints/9136961803583303949|RAG_MODEL_BASE=gemini-3.1-flash-lite|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=off|RETRIEVAL_CURRENT_ONLY=off|RETRIEVAL_GRAPH=off|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L502

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export ENDPOINT="${ENDPOINT:-$(grep -o 'projects/[^ ]*/endpoints/[0-9]*' ~/poll172.log | head -1)}"     # lesson 17.2's endpoint
make candidate PROJECT="$PROJECT" GENERATOR_MODEL="$ENDPOINT" RAG_MODEL_BASE=gemini-3.1-flash-lite
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"
"""


def demonstrate(session):
    """Run Do it: the candidate at this checkpoint.

    Do it: the candidate

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a revision with no traffic; nothing is billed until it answers).
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
