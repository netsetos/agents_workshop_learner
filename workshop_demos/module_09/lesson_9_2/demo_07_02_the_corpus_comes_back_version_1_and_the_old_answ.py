"""Lesson 9.2 / s7: The corpus comes back: version 1, and the old answer with it

Summary and purpose:
Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

HTML instruction: bash — run in the operator shell, in the kit (the state, and the candidate's ask)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_the_corpus_comes_back_version_1_and_the_old_answ
Expected observation: ledger 1ef46119bd89b143 (17 versions, last ingest_reactivated) | context cache packed from 1441fb4775d21e13: STALE
  cache  semantic in      0 cached      0   165 ms | A confirmed employee at grade E3 or above serves a

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L631

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """state92
ask92 "$CAND"
"""


def demonstrate(session):
    """Run The corpus comes back: version 1, and the old answer with it at this checkpoint.

    Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the state, and the candidate's ask).
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
