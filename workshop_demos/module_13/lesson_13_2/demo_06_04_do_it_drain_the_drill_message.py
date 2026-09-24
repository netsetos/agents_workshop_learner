"""Lesson 13.2 / s6: The alert the dead-letter queue never had

Summary and purpose:
The drill message must not stay in the queue, and a real message must not be thrown away with it. The cell pulls without acknowledging, acknowledges only the messages labelled drill=13.2, and leaves anything else for make dlq.

HTML instruction: bash — run in the operator shell, in the kit (acknowledges the drill message only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_03_do_it_the_drill
Expected observation: pulled 1; acknowledged 1 drill message(s); 0 other(s) left for make dlq

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.2-usage-reconcile/Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html#L823

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: drain the drill message at this checkpoint.

    The drill message must not stay in the queue, and a real message must not be thrown away with it. The cell pulls without acknowledging, acknowledges only the messages labelled drill=13.2, and leaves anything else for make dlq.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acknowledges the drill message only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    P = os.environ["PROJECT"]
    def gcloud(*a):
        return subprocess.run(["gcloud", *a], capture_output=True, text=True, check=True).stdout
    pulled = json.loads(gcloud("pubsub", "subscriptions", "pull", "ingest-dlq-sub", "--project", P, "--limit", "10", "--format=json") or "[]")
    drill = [m["ackId"] for m in pulled if (m["message"].get("attributes") or {}).get("drill") == "13.2"]
    if drill:
        gcloud("pubsub", "subscriptions", "ack", "ingest-dlq-sub", "--project", P, "--ack-ids=" + ",".join(drill))
    print(f"pulled {len(pulled)}; acknowledged {len(drill)} drill message(s); {len(pulled) - len(drill)} other(s) left for make dlq")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
