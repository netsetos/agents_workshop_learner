"""Lesson 4.1 / s7: Dead letters: reading the queue, deciding, cleaning up

Summary and purpose:
This dead letter deserves the second choice: the object was never meant to be indexed. Acknowledge the message to remove it from the queue, and delete the empty object from the bucket, because an object with no ledger row is exactly what the nightly walk of lesson 4.4 looks for, and it would rewrite the object onto itself and send the same poison round again every night. Both commands change your lane; both act only on the drill's own artefacts.

HTML instruction: bash — run in the operator shell (removes the dead letter and the empty object; nothing else)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_read_it_when_it_has_landed
Expected observation: acme/poison-1758542871.pdf
Removing gs://documind-ai-YOUR-ID-uploads/acme/poison-1758542871.pdf...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L789

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud pubsub subscriptions pull ingest-dlq-sub --project "$PROJECT" --limit 1 --auto-ack --format='value(message.attributes.objectId)'
gcloud storage rm "gs://$PROJECT-uploads/acme/poison-"*.pdf
"""


def demonstrate(session):
    """Run Decide, then clean up at this checkpoint.

    This dead letter deserves the second choice: the object was never meant to be indexed. Acknowledge the message to remove it from the queue, and delete the empty object from the bucket, because an object with no ledger row is exactly what the nightly walk of lesson 4.4 looks for, and it would rewrite the object onto itself and send the same poison round again every night. Both commands change your lane; both act only on the drill's own artefacts.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (removes the dead letter and the empty object; nothing else).
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
