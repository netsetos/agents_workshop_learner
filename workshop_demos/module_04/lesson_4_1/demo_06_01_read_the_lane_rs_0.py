"""Lesson 4.1 / s6: The batch lane: the 250-page decision, the queued claim, the job

Summary and purpose:
The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it_start_the_drill_then_watch_the_first_retri
Expected observation: 0 queued document(s)
no batch job on this lane: a queued claim waits until make batch-job declares it (BATCH_JOB=true, a Terraform apply)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L699

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make queued PROJECT=$PROJECT

if [ -n "$BATCH_JOB" ]; then
  gcloud run jobs describe "$BATCH_JOB" --region "$REGION" --project "$PROJECT" --format=json | python -c "
import json, sys
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('image', 'args', 'timeoutSeconds', 'maxRetries', 'taskCount'): print(f'{k}: {v}')
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(json.load(sys.stdin))"
  gcloud scheduler jobs describe documind-ingest-batch-hourly --location "$REGION" --project "$PROJECT" --format='value(schedule,timeZone,state)'
else
  echo "no batch job on this lane: a queued claim waits until make batch-job declares it (BATCH_JOB=true, a Terraform apply)"
fi
"""


def demonstrate(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only).
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
