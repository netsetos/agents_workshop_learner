"""Lesson 6.3 / s5: The guard: a prompt refused before the stream, an answer held until it is screened

Summary and purpose:
Read the lane, Rs 0

HTML instruction: bash — run in the operator shell (two log reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_empty_pool_as_one_token_then_the_strea
Expected observation: NN off

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.3-streaming/Netsetos_GCP_Capstone_6.3_Streaming_WIX.html#L590

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="query" OR jsonPayload.event="stream")' \\
  --project "$PROJECT" --freshness 24h --limit 200 --format='value(jsonPayload.guard)' | sort | uniq -c
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="guard"' \\
  --project "$PROJECT" --freshness 7d --limit 3 --format='value(timestamp,jsonPayload.verdict,jsonPayload.reason)'
"""


def demonstrate(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    Read the lane, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two log reads).
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
