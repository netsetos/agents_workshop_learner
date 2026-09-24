"""Lesson 10.1 / s7: The loop: the model chooses its tools

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the LangChain loop on the same question, then a cost question on both brains)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: langchain tool_calls ['retrieve']  refusals []  citations 0  7240 ms
      After five years of continuous service, under the Payment of Gratuity Act, 1972.
  langchain tool_calls ['retrieve', 'calculate_processing_cost']  refusals []  citations 0  11350 ms
      At the priority tier (USD 0.12 a page), 283 pages cost USD 33.96, about Rs 2,886.60.
  direct    tool_calls ['retrieve']  refusals []  citations 3  3420 ms
      The documents give no per-page price for processing the handbook; the April invoice bills priori

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L628

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """chat10 langchain "After how many years of continuous service does gratuity become payable?"
chat10 langchain "The ACME handbook has 283 pages. What would processing it cost at the priority tier?"
chat10 direct "The ACME handbook has 283 pages. What would processing it cost at the priority tier?"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the LangChain loop on the same question, then a cost question on both brains).
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
