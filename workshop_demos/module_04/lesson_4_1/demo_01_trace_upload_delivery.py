"""Lesson 4.1: demo 01 trace upload delivery

Read upload notification, push identity and the previous upload's request/event records.

Run order inside this file:
1. Read it off the platform (source window 10)
2. Read the two records your 3.4 upload left (source window 16)

Prerequisites: setup_prepare.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_off_the_platform.
COMMANDS_01 = """gcloud storage buckets notifications list "gs://$PROJECT-uploads" --project "$PROJECT"

gcloud pubsub subscriptions describe documind-ingest-push --project "$PROJECT" \\
  --format='yaml(pushConfig.pushEndpoint,pushConfig.oidcToken.serviceAccountEmail,ackDeadlineSeconds,retryPolicy,deadLetterPolicy)'

gcloud pubsub subscriptions describe ingest-dlq-sub --project "$PROJECT" --format='value(topic)'

gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='yaml(spec.template.spec.timeoutSeconds,spec.template.spec.containerConcurrency,spec.template.metadata.annotations)'

"""

def step_01_off_the_platform(session):
    """Run Read it off the platform at this checkpoint.

    Read it off the platform

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (all read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_read_the_two_records_your_3_4_upload_left.
COMMANDS_02 = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND logName=\\"projects/$PROJECT/logs/run.googleapis.com%2Frequests\\" AND timestamp>=\\"$(date -u -d '-3 hours' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
  --project "$PROJECT" --limit 6 --format='table(timestamp,httpRequest.requestMethod,httpRequest.status,httpRequest.latency)'

gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$(date -u -d '-3 hours' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
  --project "$PROJECT" --limit 6 --format='table(timestamp,jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.lane)'

"""

def step_02_read_the_two_records_your_3_4_upload_left(session):
    """Run Read the two records your 3.4 upload left at this checkpoint.

    Every delivery writes a request log entry (Cloud Run's, with the status the worker answered and how long it took) and, from the worker, a JSON line with the verdict. The first read below lists the last few POSTs the subscription made to the worker; the second lists the worker's own verdicts for the same window. Your note from lesson 3.4 should be there twice: once as the duplicate the unchanged bytes produced, once as the indexed version.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_off_the_platform),
        ('source_16', step_02_read_the_two_records_your_3_4_upload_left),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
