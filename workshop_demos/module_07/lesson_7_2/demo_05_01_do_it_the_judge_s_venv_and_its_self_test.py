"""Lesson 7.2 / s5: The judge: the lane's own answers, read with the context they cite

Summary and purpose:
Do it: the judge's venv and its self-test

HTML instruction: bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_03_do_it_the_live_gate_with_a_report
Expected observation: selftest: the cited chunk's text replaces its quote as the context and a miss keeps the quote; the prompt the judge reads carries the context then the question; the frame carries the six judge columns plus the baseline; the trajectory maths is right on the three cases

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L698

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m venv "$HOME/judge-venv"            # its own venv: the SDK is a major version ahead of the kit's
"$HOME/judge-venv/bin/python" -m pip install -q "google-cloud-aiplatform[evaluation]==2.1.0" pandas google-cloud-firestore
"$HOME/judge-venv/bin/python" evals/judge.py --selftest
"""


def demonstrate(session):
    """Run Do it: the judge's venv and its self-test at this checkpoint.

    Do it: the judge's venv and its self-test

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test).
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
