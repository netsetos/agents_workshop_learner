"""Lesson 4.4: repair module baseline

Explicit recovery: repair module baseline

Run order inside this file:
1. Run the broader module validation separately (source window 40)

Prerequisites: workshop setup; see this lesson README.
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


# Original CLI workflow for step_01_run_the_broader_module_validation_separate.
COMMANDS_01 = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" AND (jsonPayload.tenant="acme" OR jsonPayload.doc_key:"acme_")' \\
  --project "$PROJECT" --freshness 20m --limit 5 --format='value(timestamp,jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.tenant)'
git -C "$DEMO_ROOT" pull -q --ff-only && grep -c 'doc_key:' smoke/smoke_reindex.py
gcloud pubsub subscriptions describe documind-ingest-push --project "$PROJECT" --format='value(pushConfig.pushEndpoint)'

"""

def step_01_run_the_broader_module_validation_separate(session):
    """Run Run the broader module validation separately at this checkpoint.

    The smoke leaves its own fixture indexed. That does not demonstrate that $SOURCE was retired or restored. Count embedding work from the worker's actual events; a refused undo can require fresh embeddings, while a successful reactivation reuses retained vectors. Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_40', step_01_run_the_broader_module_validation_separate),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
