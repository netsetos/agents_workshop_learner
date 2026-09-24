"""Lesson 18.3 / s5: The lane's cluster, inspected

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (it stops before changing anything on a Standard lab)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: STOP: the Standard CPU lab cannot run the L4 GPU lesson. Set gke_autopilot=true in Terraform, review cluster replacement and quota, and apply before make gke-up.
make: *** [Makefile:695: gke-up] Error 1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.3-vllm-gke/Netsetos_GCP_Capstone_18.3_VLLM_GKE_WIX.html#L685

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make gke-up PROJECT="$PROJECT"            # read-only on a Standard lab: it checks the mode and stops
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (it stops before changing anything on a Standard lab).
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
