"""Lesson 4.4 / s11: Run the broader module validation separately

Summary and purpose:
The smoke leaves its own fixture indexed. That does not demonstrate that $SOURCE was retired or restored. Count embedding work from the worker's actual events; a refused undo can require fresh embeddings, while a successful reactivation reuses retained vectors. Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint)
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: 2026-09-2xT1x:xx:xx.xxxxxxZ	ingest_duplicate	acme_9c41d0e2b7f5...
1
https://documind-ingest-NUMBER.asia-south1.run.app

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L980

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" AND (jsonPayload.tenant="acme" OR jsonPayload.doc_key:"acme_")' \\
  --project "$PROJECT" --freshness 20m --limit 5 --format='value(timestamp,jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.tenant)'
git -C "$DEMO_ROOT" pull -q --ff-only && grep -c 'doc_key:' smoke/smoke_reindex.py
gcloud pubsub subscriptions describe documind-ingest-push --project "$PROJECT" --format='value(pushConfig.pushEndpoint)'
"""


def demonstrate(session):
    """Run Run the broader module validation separately at this checkpoint.

    The smoke leaves its own fixture indexed. That does not demonstrate that $SOURCE was retired or restored. Count embedding work from the worker's actual events; a refused undo can require fresh embeddings, while a successful reactivation reuses retained vectors. Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint).
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
