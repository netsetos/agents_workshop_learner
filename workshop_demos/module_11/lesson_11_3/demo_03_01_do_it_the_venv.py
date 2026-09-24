"""Lesson 11.3 / s3: Isolation, on the kit's own app

Summary and purpose:
Do it: the venv

HTML instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and 11.2's connector)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: graph-venv ok: fastapi 0.141.1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.3-restart-isolation/Netsetos_GCP_Capstone_11.3_Restart_Isolation_WIX.html#L414

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """[ -x ~/graph-venv/bin/python ] || python -m venv ~/graph-venv   # lesson 10.2's venv, made here if it is missing
~/graph-venv/bin/pip install -q "langchain==1.4.0" "langchain-core==1.6.2" "requests==2.34.2" "google-auth==2.57.1" "fastapi==0.141.1" \\
  "cloud-sql-python-connector[pg8000]==1.22.0" "pg8000==1.31.5"   # the chat image's pins, and 11.2's connector
~/graph-venv/bin/python -c 'import fastapi.testclient, google.cloud.sql.connector; print("graph-venv ok: fastapi", fastapi.__version__)'
"""


def demonstrate(session):
    """Run Do it: the venv at this checkpoint.

    Do it: the venv

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and 11.2's connector).
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
