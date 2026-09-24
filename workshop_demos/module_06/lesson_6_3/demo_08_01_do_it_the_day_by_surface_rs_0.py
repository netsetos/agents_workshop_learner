"""Lesson 6.3 / s8: What a stream costs, what its row says, and who reads it

Summary and purpose:
Do it: the day by surface, Rs 0

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_ranker_silent_for_one_revision_the_str
Expected observation: by surface
event                  answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
query                       NN     xxxxx     xxxx    0.0xxx      x.xx    4xxx   0.xx
stream                       4      xxxx      xxx    0.0xxx      x.xx    4xxx   0.25

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.3-streaming/Netsetos_GCP_Capstone_6.3_Streaming_WIX.html#L742

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make usage PROJECT=$PROJECT HOURS=24 | sed -n '/^by surface/,/^$/p'
"""


def demonstrate(session):
    """Run Do it: the day by surface, Rs 0 at this checkpoint.

    Do it: the day by surface, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one log read).
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
