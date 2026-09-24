"""Lesson 4.1 / s4: The verdicts: the HTTP-code rule, and your last upload's request log

Summary and purpose:
Every delivery writes a request log entry (Cloud Run's, with the status the worker answered and how long it took) and, from the worker, a JSON line with the verdict. The first read below lists the last few POSTs the subscription made to the worker; the second lists the worker's own verdicts for the same window. Your note from lesson 3.4 should be there twice: once as the duplicate the unchanged bytes produced, once as the indexed version.

HTML instruction: bash — run in the operator shell (both read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_read_it_off_the_platform
Expected observation: TIMESTAMP                 REQUEST_METHOD  STATUS  LATENCY
2026-09-22T12:06:41.118Z  POST            200     7.412s
2026-09-22T11:58:07.902Z  POST            200     0.611s
TIMESTAMP                 EVENT             DOC_KEY                 CHUNKS  LANE
2026-09-22T12:06:41.001Z  ingest_ok         acme_9c41d0e2b7f5...    3       push
2026-09-22T11:58:07.844Z  ingest_duplicate  acme_111510fcf0a6...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L553

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND logName=\\"projects/$PROJECT/logs/run.googleapis.com%2Frequests\\" AND timestamp>=\\"$(date -u -d '-3 hours' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
  --project "$PROJECT" --limit 6 --format='table(timestamp,httpRequest.requestMethod,httpRequest.status,httpRequest.latency)'

gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$(date -u -d '-3 hours' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
  --project "$PROJECT" --limit 6 --format='table(timestamp,jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.lane)'
"""


def demonstrate(session):
    """Run Read the two records your 3.4 upload left at this checkpoint.

    Every delivery writes a request log entry (Cloud Run's, with the status the worker answered and how long it took) and, from the worker, a JSON line with the verdict. The first read below lists the last few POSTs the subscription made to the worker; the second lists the worker's own verdicts for the same window. Your note from lesson 3.4 should be there twice: once as the duplicate the unchanged bytes produced, once as the indexed version.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
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
