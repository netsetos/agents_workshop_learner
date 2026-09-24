"""Lesson 13.3 / s6: Off at night, and the ceiling under it

Summary and purpose:
Do it: the floor, then the switch

HTML instruction: bash — run in the operator shell, in the kit (a floor, then the switch, then the nightly job's entry)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_03_do_it_undo_the_candidate
Expected observation: gcloud run services update documind-slm --region us-central1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
ERROR: (gcloud.run.services.update) Service [documind-slm] could not be found.
make[1]: [Makefile:659: slm-off] Error 1 (ignored)
...
gcloud run services update documind-ui --region asia-south1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
Deploying...
...
Done.
...
documind-slm: min-instances absent
documind-vllm: min-instances absent
documind-gateway: min-instances absent
documind-ui: min-instances 0
0 23 * * *	Asia/Kolkata	ENABLED	2026-09-23T17:30:03.184Z

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L658

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-ui --region "$REGION" --project "$PROJECT" --min-instances 1 --quiet   # a session day's floor
make off PROJECT="$PROJECT"
gcloud scheduler jobs describe documind-off-nightly --location "$REGION" --project "$PROJECT" \\
  --format='value(schedule,timeZone,state,lastAttemptTime)'
"""


def demonstrate(session):
    """Run Do it: the floor, then the switch at this checkpoint.

    Do it: the floor, then the switch

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a floor, then the switch, then the nightly job's entry).
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
