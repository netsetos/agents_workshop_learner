"""Lesson 3.1 / s5: Version: the bytes decide, and the same file in two tenants proves it

Summary and purpose:
The UI wrote the object under your tenant's folder as its own service account; it never touched Firestore. The worker did the rest. "Upload complete" is not "indexed" - the page says so itself. From the shell, the same bytes to zeta. There is no UI session for zeta here, so the copy goes straight to the bucket, which is exactly what the UI does behind its Upload button.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_read_it_in_firestore
Expected observation: 5b62d236e0c1...  evals/demo/gratuity_amendment_2026.md
acme    acme_5b62d236e0c1...    3    3
zeta    zeta_5b62d236e0c1...    3    3

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L647

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud storage cp evals/demo/gratuity_amendment_2026.md gs://$PROJECT-uploads/zeta/
sha256sum evals/demo/gratuity_amendment_2026.md

# the worker's own line for each tenant (wait a few seconds after the copy)
for T in acme zeta; do
  gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" \\
    AND jsonPayload.event=\\"ingest_ok\\" AND jsonPayload.tenant=\\"$T\\"" \\
    --project $PROJECT --limit 1 --format='value(jsonPayload.tenant,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.embedded)'
done
"""


def demonstrate(session):
    """Run Do it: one file, two tenants at this checkpoint.

    The UI wrote the object under your tenant's folder as its own service account; it never touched Firestore. The worker did the rest. "Upload complete" is not "indexed" - the page says so itself. From the shell, the same bytes to zeta. There is no UI session for zeta here, so the copy goes straight to the bucket, which is exactly what the UI does behind its Upload button.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT.
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
