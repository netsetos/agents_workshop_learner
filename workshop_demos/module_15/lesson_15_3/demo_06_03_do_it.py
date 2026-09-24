"""Lesson 15.3 / s6: globex stays home: the skip, the ledger row, and a pin the policy overrides

Summary and purpose:
If your lines are missing, the worker instance that took the note had already said it: the skip is said once per tenant and store per instance. The cell then prints the last week's lines instead, and the empty mirrored on the row is the record for this document. Last, try to move globex's text with a pin:

HTML instruction: bash — run in the operator shell, in the kit (globex pinned to a store for one question, then unpinned)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it
Expected observation: globex: retrieval_backend=rag_engine
globex: retrieval_backend vector, policy_fallback 1; pool 20, 0 from a managed store
  A: Either party may terminate the agreement for convenience on 120 days' written notice [1].
  cites globex:a0d13745...#2 (msa_globex_2026.md)
globex: retrieval_backend=default

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L814

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make tenant-backend PROJECT="$PROJECT" TENANT=globex RETRIEVAL_BACKEND=rag_engine
sleep 60      # the API reads a tenant's settings once a minute per instance
ask153 globex
make tenant-backend PROJECT="$PROJECT" TENANT=globex RETRIEVAL_BACKEND=default
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    If your lines are missing, the worker instance that took the note had already said it: the skip is said once per tenant and store per instance. The cell then prints the last week's lines instead, and the empty mirrored on the row is the record for this document. Last, try to move globex's text with a pin:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (globex pinned to a store for one question, then unpinned).
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
