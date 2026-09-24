"""Lesson 8.3 / s8: The audit tab: what the admin console reads, and what it misses

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it
Expected observation: {'tenant.create': 1} | doc.upload in it: 0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html#L728

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from collections import Counter
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    seen = Counter(d.to_dict().get("action") for d in db.collection("audit_index").limit(500).stream())
    print(dict(seen) if seen else "audit_index is empty", "| doc.upload in it:", seen.get("doc.upload", 0))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
