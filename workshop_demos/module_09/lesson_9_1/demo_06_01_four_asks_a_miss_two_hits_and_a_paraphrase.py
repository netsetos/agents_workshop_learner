"""Lesson 9.1 / s6: Four asks: a miss, two hits and a paraphrase

Summary and purpose:
One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

HTML instruction: bash — run in the operator shell, in the kit (four asks to the candidate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: backend vertex cache_hit none     tokens_in  43071  cached_tokens  41259   2590 ms  | Employees may work remotely up to eight days
  backend cache  cache_hit semantic tokens_in      0  cached_tokens      0    182 ms  | Employees may work remotely up to eight days
  backend cache  cache_hit semantic tokens_in      0  cached_tokens      0    176 ms  | Employees may work remotely up to eight days
  backend vertex cache_hit none     tokens_in  43053  cached_tokens  41259   2720 ms  | Employees may work remotely up to eight days

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html#L681

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask91 "$CAND" "$Q91"                                   # 1: a miss - retrieved, generated, stored
ask91 "$CAND" "$Q91"                                   # 2: the same words - the exact rung
ask91 "$CAND" "how many days a month can i work remotely"      # 3: other case, no "?" - the same qhash
ask91 "$CAND" "How many days per month am I allowed to work from home?"   # 4: a paraphrase - the near rung, if it is 0.95 close
"""


def demonstrate(session):
    """Run Four asks: a miss, two hits and a paraphrase at this checkpoint.

    One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four asks to the candidate).
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
