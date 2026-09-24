"""Lesson 8.1 / s4: The roster: one document per member, two ways to read it, one writer

Summary and purpose:
Do it: the three rosters, as Firestore holds them

HTML instruction: bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_what_your_token_says_about_itself
Expected observation: acme    5 member(s)
    documind-agent-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    you@example.com
zeta    3 member(s)
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
globex  3 member(s)
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L567

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the three rosters, as Firestore holds them at this checkpoint.

    Do it: the three rosters, as Firestore holds them

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    for t in ("acme", "zeta", "globex"):
        members = sorted(d.id for d in db.collection("tenants").document(t).collection("members").stream())
        print(f"{t:7} {len(members)} member(s)")
        for m in members:
            print("   ", m)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
