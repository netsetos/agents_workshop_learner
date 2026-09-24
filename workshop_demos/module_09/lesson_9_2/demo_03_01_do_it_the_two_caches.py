"""Lesson 9.2 / s3: Both caches, and the corpus they follow

Summary and purpose:
Do it: the two caches

HTML instruction: bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \\
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  cache projects/NUMBER/locations/global/cachedContents/CACHE_ID
  location global (global or regional: the answer to CLAUDE.md's question)
  model gemini-3.6-flash | tokens 41259 | expires YYYY-MM-DD HH:MM:SS.ssssss+00:00 | corpus 75b21a03f12f | ledger fingerprint 1ef46119bd89b143
  the next /v1/query for acme carries cached_content; read cached_tokens in its usage row
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=on|..."
...
>> candidate revision: documind-api-00045-tqm (deploy/.cand

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L426

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make cache PROJECT="$PROJECT" TENANT=acme
make candidate PROJECT="$PROJECT" SEMANTIC_CACHE=on
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"
"""


def demonstrate(session):
    """Run Do it: the two caches at this checkpoint.

    Do it: the two caches

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on).
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
