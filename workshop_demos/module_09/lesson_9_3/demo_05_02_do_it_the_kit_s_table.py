"""Lesson 9.3 / s5: Avoided calls in rupees, and the latency of a hit

Summary and purpose:
Do it: the kit's table

HTML instruction: bash — run in the operator shell, in the kit (the kit's own table of the last hour, by model and backend)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_the_candidate_s_rows
Expected observation: by model and backend (what answered, through which door)
model                 model_backend          answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------------------------------
gemini-3.6-flash      vertex                      55     97661    20783    0.3024     25.70    3187   0.00
gemini-3.6-flash      cache                       10         0        0    0.0000      0.00     236   0.00

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L616

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make usage PROJECT="$PROJECT" HOURS=1 | sed -n '/by model and backend/,/^$/p'
"""


def demonstrate(session):
    """Run Do it: the kit's table at this checkpoint.

    Do it: the kit's table

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's own table of the last hour, by model and backend).
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
