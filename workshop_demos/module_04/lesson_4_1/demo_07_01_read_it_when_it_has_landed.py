"""Lesson 4.1 / s7: Dead letters: reading the queue, deciding, cleaning up

Summary and purpose:
The poison message from step 5 reaches the queue about an hour after its first refusal. Run the first line then; an empty listing earlier is the retries still running, not a fault. The second read decodes the message's own record, the same JSON the worker refused, to see the size of zero with your own eyes.

HTML instruction: bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_read_the_lane_rs_0
Expected observation: MESSAGE_ID         OBJECT_ID                    EVENT_TIME                DELIVERY_ATTEMPT
12345678901234567  acme/poison-1758542871.pdf   2026-09-22T12:17:52.318Z  1
{'name': 'acme/poison-1758542871.pdf', 'size': '0', 'contentType': 'application/pdf', 'generation': '1758542872123456', 'timeCreated': '2026-09-22T12:17:52.101Z'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L778

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make dlq PROJECT=$PROJECT

gcloud pubsub subscriptions pull ingest-dlq-sub --project "$PROJECT" --limit 1 --format='value(message.data)' \\
  | base64 -d | python -c "import json,sys; r=json.load(sys.stdin); print({k: r.get(k) for k in ('name','size','contentType','generation','timeCreated')})"
"""


def demonstrate(session):
    """Run Read it, when it has landed at this checkpoint.

    The poison message from step 5 reaches the queue about an hour after its first refusal. Run the first line then; an empty listing earlier is the retries still running, not a fault. The second read decodes the message's own record, the same JSON the worker refused, to see the size of zero with your own eyes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged).
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
