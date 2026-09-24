"""Lesson 9.3 / s4: The replay: the same pairs, asked live at 0.95

Summary and purpose:
Do it: the candidate

HTML instruction: bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on at the kit's 0.95, and a start time)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=on|..."
...
>> candidate revision: documind-api-00046-wpk (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L494

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make candidate PROJECT="$PROJECT" SEMANTIC_CACHE=on
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app" SINCE93="$(date -u +%FT%TZ)"; echo "CAND=$CAND"
"""


def demonstrate(session):
    """Run Do it: the candidate at this checkpoint.

    Do it: the candidate

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on at the kit's 0.95, and a start time).
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
