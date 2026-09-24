"""Lesson 9.1 / s7: What each cache is holding, and the clean-up

Summary and purpose:
The record behind the context cache, the entry behind the hit, and both caches put away. The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it.

HTML instruction: bash — run in the operator shell, in the kit (what each cache is holding; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_four_asks_a_miss_two_hits_and_a_paraphrase
Expected observation: context cache  (Firestore holds a pointer; the pack itself is on Google's side)
    cache_name: projects/NUMBER/locations/global/cachedContents/CACHE_ID
    location: global
    model: gemini-3.6-flash
    tokens: 41259
    expire_time: YYYY-MM-DD HH:MM:SS.ssssss+00:00
    corpus_fingerprint: FINGERPRINT
answer cache  (2 acme entries; 1 for this question's words)
    question: How many days a month can I work remotely?
    qhash: 79ae9ca70e9e21c4c23aca5b  scope: 7a0875abc72b0f7b  fingerprint: FINGERPRINT_
    model: gemini-3.6-flash  expire_at: YYYY-MM-DD HH:MM:SS+00:00  embedding: 768 numbers
    answer: Employees may work remotely up to eight days per month with   citations: 1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html#L717

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run What each cache is holding, and the clean-up at this checkpoint.

    The record behind the context cache, the entry behind the hit, and both caches put away. The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (what each cache is holding; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    sys.path.insert(0, "services/rag-api")
    from semantic_cache import qhash
    db = firestore.Client(project=os.environ["PROJECT"])
    c = db.collection("tenant_caches").document("acme").get().to_dict() or {}
    print("context cache  (Firestore holds a pointer; the pack itself is on Google's side)")
    for k in ("cache_name", "location", "model", "tokens", "expire_time", "corpus_fingerprint"):
        print(f"    {k}: {c.get(k)}")
    rows = [d.to_dict() for d in db.collection("answer_cache").where(filter=FieldFilter("tenant_id", "==", "acme")).stream()]
    mine = [r for r in rows if r.get("qhash") == qhash(os.environ["Q91"])]
    print(f"answer cache  ({len(rows)} acme entries; {len(mine)} for this question's words)")
    for r in mine[:1]:
        print(f"    question: {r['question']}\n    qhash: {r['qhash']}  scope: {r['scope']}  fingerprint: {r['fingerprint'][:12]}")
        print(f"    model: {r['model']}  expire_at: {r['expire_at']}  embedding: {len(r['embedding'])} numbers")
        print(f"    answer: {r['answer']['answer'][:60]}  citations: {len(r['answer']['citations'])}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
