"""Lesson 7.2 / s4: The live half: every row, two identities, nine rates, three exit codes

Summary and purpose:
Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point. Last, what the run cost. The API priced every answer on its usage row; make usage groups the last hour of those rows. Run it straight after the gate, before step 5 asks the lane again.

HTML instruction: bash — run in the operator shell, in the kit (the usage rows of the last hour, priced)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_live_gate_with_a_report
Expected observation: 65 answers from documind-api in the last 1 h; USD_INR=85

by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------
acme                        47       ...      ...       ...       ...     ...    ...
zeta                        10       ...      ...       ...       ...     ...    ...
globex                       8       ...      ...       ...       ...     ...    ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L621

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make usage PROJECT="$PROJECT" HOURS=1 | sed -n '1,8p'
"""


def demonstrate(session):
    """Run Do it: the live gate, with a report at this checkpoint.

    Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point. Last, what the run cost. The API priced every answer on its usage row; make usage groups the last hour of those rows. Run it straight after the gate, before step 5 asks the lane again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the usage rows of the last hour, priced).
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
