"""Lesson 18.4 / s3: The table's maths, read

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the script's own check of its maths; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: backend            rows  groundedness  cite-precision   p95 ms  Rs/1k queries
------------------------------------------------------------------------------
documind-general      3         0.500           0.667     1200          42.00
documind-slm          3         1.000           0.500     3100        1951.33

selftest OK - groundedness excludes refusal rows, precision is per cited chunk, p95 is the 95th latency, Rs/1k is mean cost x 1000

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.4-compare-shutdown/Netsetos_GCP_Capstone_18.4_Compare_Shutdown_WIX.html#L450

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python services/slm/compare_backends.py --selftest
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the script's own check of its maths; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
