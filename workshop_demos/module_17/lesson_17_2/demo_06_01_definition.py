"""Lesson 17.2 / s6: The endpoint, and where it answers

Summary and purpose:
The first cell polls the job once a minute until it ends. The poll only reads, so it costs nothing, and after a disconnect it is safe to run again: it takes the job from step 5's log. When the job succeeds, tune.py prints: The cell keeps the endpoint in ~/poll172.log and in ENDPOINT.

HTML instruction: bash — run in the operator shell, in the kit (waits for the job, a line a minute)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: 09:53:00 JobState.JOB_STATE_PENDING
  09:54:00 JobState.JOB_STATE_PENDING
  09:55:00 JobState.JOB_STATE_RUNNING
  ...      (a line a minute while the job runs: 33 more here)
  10:29:00 JobState.JOB_STATE_RUNNING
  JOB_STATE_SUCCEEDED
  tuned model : projects/NUMBER/locations/us/models/6156234374247085944@1
  endpoint    : projects/NUMBER/locations/us/endpoints/9136961803583303949

  serve it as a candidate revision, no traffic, and judge it:
    make candidate PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=projects/NUMBER/locations/us/endpoints/9136961803583303949 RAG_MODEL_BASE=gemini-3.1-flash-lite
    make eval-live PROJECT=documind-ai-YOUR-ID API=<the candidate url>
    make judge PROJECT=documind-ai-YOUR-ID API_B=<the candidate url>
ENDPOINT=projects/NUMBER/locations/us/endpoints/9136961803583303949

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.2-managed-tuning/Netsetos_GCP_Capstone_17.2_Managed_Tuning_WIX.html#L657

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """JOB="${JOB:-$(grep -o 'projects/[^ ]*/tuningJobs/[0-9]*' ~/tune172.log | head -1)}"     # after a reconnect: the job, from step 5's log
python evals/tune.py --project "$PROJECT" --poll "$JOB" | tee ~/poll172.log   # a line a minute until the job ends; safe to re-run
export ENDPOINT="$(grep -o 'projects/[^ ]*/endpoints/[0-9]*' ~/poll172.log | head -1)"; echo "ENDPOINT=$ENDPOINT"
"""


def demonstrate(session):
    """Run Definition at this checkpoint.

    The first cell polls the job once a minute until it ends. The poll only reads, so it costs nothing, and after a disconnect it is safe to run again: it takes the job from step 5's log. When the job succeeds, tune.py prints: The cell keeps the endpoint in ~/poll172.log and in ENDPOINT.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (waits for the job, a line a minute).
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
