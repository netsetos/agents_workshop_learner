"""Lesson 9.1 / s3: The context cache: a pack, a cache, and the next answer

Summary and purpose:
Do it: the same question, with the cache

HTML instruction: bash — run in the operator shell, in the kit (the same question again, to the live API)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_the_cache
Expected observation: backend vertex cache_hit none     tokens_in  43071  cached_tokens  41259   2650 ms  | Employees may work remotely up to eight days

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html#L529

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask91 "$API" "$Q91"
"""


def demonstrate(session):
    """Run Do it: the same question, with the cache at this checkpoint.

    Do it: the same question, with the cache

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same question again, to the live API).
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
