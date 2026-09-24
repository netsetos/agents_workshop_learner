"""Lesson 13.1 / s6: Trace it, name the cause, put it back

Summary and purpose:
Do it: the versions view and the two probes

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_trace
Expected observation: source                                       status                  gen chunks reused embed retired effective  embedding              indexed_at
acme/hr_policy_2026.md                       indexed    1758624067215604    283    283     0     283 -          text-embedding-005@1   2026-09-23T10:41:07
Project: documind-ai-YOUR-ID (NUMBER)
Terraform index: projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
Terraform endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321
API index: projects/NUMBER/locations/asia-south1/indexes/1234567890123456789
API endpoint: projects/NUMBER/locations/asia-south1/indexEndpoints/9876543210987654321
Index dimensions: 768; update method: STREAM_UPDATE
Global vector count: 1745
Deployment: documind_chunks_v1
Deployment sync time: 2026-09-23T10:42:18.000Z
PASS: the expected index is attached to

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html#L737

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make sources PROJECT="$PROJECT" TENANT_ONLY=acme | grep -E "^source|hr_policy_2026"
python commands/verify-vector-index.py --deploy-root "$DEMO_ROOT" --project "$PROJECT" --region "$REGION"
GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py
"""


def demonstrate(session):
    """Run Do it: the versions view and the two probes at this checkpoint.

    Do it: the versions view and the two probes

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only).
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
