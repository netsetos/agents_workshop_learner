"""Lesson 9.2 / s6: make cache again: attached again, and what it packed

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the pack again, under the new fingerprint)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it_the_state_both_asks_and_the_log
Expected observation: cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \\
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  cache projects/NUMBER/locations/global/cachedContents/CACHE_ID
  location global (global or regional: the answer to CLAUDE.md's question)
  model gemini-3.6-flash | tokens 41259 | expires YYYY-MM-DD HH:MM:SS.ssssss+00:00 | corpus 75b21a03f12f | ledger fingerprint 1441fb4775d21e13
  the next /v1/query for acme carries cached_content; read cached_tokens in its usage row
  ledger 1441fb4775d21e13 (17 versions, last ingest_reactivated) | context cache packed from 1441fb4775d21e13: current
  vertex none     in  43139 cached  41259  2575 ms | From 1 October 2026 the notice period for a confir

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L603

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make cache PROJECT="$PROJECT" TENANT=acme
state92
ask92 "$API"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the pack again, under the new fingerprint).
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
