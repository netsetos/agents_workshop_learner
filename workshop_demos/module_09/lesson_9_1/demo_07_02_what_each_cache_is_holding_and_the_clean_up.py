"""Lesson 9.1 / s7: What each cache is holding, and the clean-up

Summary and purpose:
The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it. The two records show where each cache keeps its weight. For the context cache, Firestore holds only a pointer and a few facts, and the pack's forty-odd thousand tokens sit on Google's side, billed by the hour until they expire or are deleted. For the answer cache, Firestore holds everything: the answer, its citations and the question's 768-number embedding. That costs Firestore storage and reads, for 24 hours. The clean-up removes the candidate's tag and recorded name, and deletes the context cache. The next acme question to the live API finds no record and runs uncached at once.

HTML instruction: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_what_each_cache_is_holding_and_the_clean_up
Expected observation: Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-00041-kqz      (the live revision, as before; no candidate tag)
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \\
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  deleted acme's cache

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html#L752

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate
rm -f .candidate-revision      # make promote would otherwise flip traffic to the recorded revision
make cache PROJECT="$PROJECT" TENANT=acme CACHE_OP=delete
"""


def demonstrate(session):
    """Run What each cache is holding, and the clean-up at this checkpoint.

    The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it. The two records show where each cache keeps its weight. For the context cache, Firestore holds only a pointer and a few facts, and the pack's forty-odd thousand tokens sit on Google's side, billed by the hour until they expire or are deleted. For the answer cache, Firestore holds everything: the answer, its citations and the question's 768-number embedding. That costs Firestore storage and reads, for 24 hours. The clean-up removes the candidate's tag and recorded name, and deletes the context cache. The next acme question to the live API finds no record and runs uncached at once.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted).
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
