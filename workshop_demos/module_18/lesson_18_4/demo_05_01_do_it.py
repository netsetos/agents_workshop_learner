"""Lesson 18.4 / s5: Everything off

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit, when the comparison is done
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: ...
documind-slm scaled to zero
...
documind-gateway scaled to zero
...
vLLM workload removed; the cluster and any Standard lab node remain (gke.tf) - make down removes them
documind-slm: min-instances 0
documind-vllm: min-instances absent
documind-gateway: min-instances 0
documind-ui: min-instances 0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.4-compare-shutdown/Netsetos_GCP_Capstone_18.4_Compare_Shutdown_WIX.html#L612

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make off PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit, when the comparison is done.
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
