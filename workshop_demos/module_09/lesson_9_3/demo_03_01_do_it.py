"""Lesson 9.3 / s3: The curve: every candidate threshold on the labelled pairs

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (65 embeddings, about a minute; the report goes to your home folder)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: 42 pairs against 23 golden questions, text-embedding-005 @ us-central1

  threshold   hit rate (same)   false-hit rate (different)
       0.85      100% (24)          83% (15)
       0.88      100% (24)          67% (12)
       0.90       96% (23)          61% (11)
       0.92       62% (15)          50% ( 9)
       0.94       46% (11)          22% ( 4)
       0.95       33% ( 8)          11% ( 2)
       0.96       25% ( 6)           6% ( 1)
       0.97       17% ( 4)           0% ( 0)
       0.98        4% ( 1)           0% ( 0)

  lowest threshold with no false hit: 0.97
  nearest false pairs: pp-25 0.962, pp-31 0.955, pp-37 0.947, pp-35 0.941, pp-42 0.931, pp-41 0.929, pp-27 0.926, pp-30 0.926, pp-33 0.923, pp-40 0.914, pp-26 0.908, pp-36 0.885, pp-38 0.864, pp-39 0.858, pp-34 0.852, pp-29
  report: /home/you/cache93_curve.json

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L446

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python evals/cache_threshold.py --project "$PROJECT" --report ~/cache93_curve.json
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (65 embeddings, about a minute; the report goes to your home folder).
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
