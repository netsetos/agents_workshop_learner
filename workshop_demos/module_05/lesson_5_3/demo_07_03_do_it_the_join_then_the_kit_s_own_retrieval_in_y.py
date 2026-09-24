"""Lesson 5.3 / s7: found_by: stamped on every chunk, counted on the answer, absent from the citation

Summary and purpose:
Do it: the join, then the kit's own retrieval in your process, then the smoke

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_do_it_the_join_then_the_kit_s_own_retrieval_in_y
Expected observation: [PASS] health  {"status":"ok"}
  [PASS] ready  ...
  [PASS] query  answerable=True citations=3  '...'
  [PASS] vector tier  20 of 20 chunks came from the index
  [PASS] no token refused  status=403
  ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L840

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme \\
DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep -E "query|vector tier|no token|PASS|FAIL"
"""


def demonstrate(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee).
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
