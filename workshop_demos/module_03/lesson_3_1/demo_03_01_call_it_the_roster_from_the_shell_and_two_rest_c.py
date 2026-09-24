"""Lesson 3.1 / s3: Tenant: something you are, never something you send

Summary and purpose:
First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L459

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make roster PROJECT=$PROJECT TENANT=acme MEMBERS="$ME"
"""


def demonstrate(session):
    """Run Call it: the roster from the shell, and two REST calls at this checkpoint.

    First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
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
