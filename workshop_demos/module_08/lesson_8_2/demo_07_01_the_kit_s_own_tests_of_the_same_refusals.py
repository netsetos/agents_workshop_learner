"""Lesson 8.2 / s7: The kit's own tests of the same refusals

Summary and purpose:
The smoke test's check 3b, and the chat service's check 4. The kit asserts these refusals itself, so a deploy that opened a door would fail its own smoke test. smoke/smoke.py sends its question again with no token and passes only on 401 or 403. smoke/smoke_chat.py asks the chat service as the outsider and passes only on a 403 from the roster, not a 401 from the verifier. The MCP server's smoke test does the same. The cell runs the API's smoke test and keeps two of its lines.

HTML instruction: bash — run in the operator shell, in the kit (the kit's smoke test, two of its lines)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_the_policy_against_a_pin_a_tenant_kept_in_india
Expected observation: [PASS] no token refused  status=403
  N pass · 0 fail

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html#L609

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """DOCUMIND_API_URL="$API" DOCUMIND_PROJECT="$PROJECT" DOCUMIND_TENANT=acme make smoke | grep -E "no token|pass ·"
"""


def demonstrate(session):
    """Run The kit's own tests of the same refusals at this checkpoint.

    The smoke test's check 3b, and the chat service's check 4. The kit asserts these refusals itself, so a deploy that opened a door would fail its own smoke test. smoke/smoke.py sends its question again with no token and passes only on 401 or 403. smoke/smoke_chat.py asks the chat service as the outsider and passes only on a 403 from the roster, not a 401 from the verifier. The MCP server's smoke test does the same. The cell runs the API's smoke test and keeps two of its lines.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's smoke test, two of its lines).
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
