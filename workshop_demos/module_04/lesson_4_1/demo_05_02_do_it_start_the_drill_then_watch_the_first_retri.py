"""Lesson 4.1 / s5: Poison: a message that can never succeed, and the retries you can watch

Summary and purpose:
The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

HTML instruction: bash — run in the operator shell, a few minutes later (read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_start_the_drill_then_watch_the_first_retri
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L607

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND logName=\\"projects/$PROJECT/logs/run.googleapis.com%2Frequests\\" AND httpRequest.status=400 AND timestamp>=\\"$POISON_SINCE\\"" \\
  --project "$PROJECT" --limit 12 --format='table(timestamp,httpRequest.status,httpRequest.latency)'

echo "refusals logged so far: $(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event=\\"ingest_poison\\" AND timestamp>=\\"$POISON_SINCE\\"" --project "$PROJECT" --limit 12 --format='value(timestamp)' | wc -l) of 12"
"""


def demonstrate(session):
    """Run Do it: start the drill, then watch the first retries at this checkpoint.

    The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, a few minutes later (read-only).
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
