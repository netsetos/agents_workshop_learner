"""Lesson 4.1 / s5: Poison: a message that can never succeed, and the retries you can watch

Summary and purpose:
The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_read_the_two_records_your_3_4_upload_left
Expected observation: >> zero-byte object in: poison-1758542871.pdf
>> the worker refused it (400): 1 validation error for IngestMessage
size
  Input should be greater than or equal to 1 [type=greater_than_equal, input_value='0', input_type=str]
>> Pub/Sub retries a non-2xx with backoff (10 s to 600 s, twelve attempts: eventarc.tf), then ingest-dlq: make dlq about an hour after this line

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L598

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export POISON_SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
make poison PROJECT=$PROJECT TENANT=acme
"""


def demonstrate(session):
    """Run Do it: start the drill, then watch the first retries at this checkpoint.

    The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0).
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
