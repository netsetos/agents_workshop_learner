"""Lesson 5.3: demo 01 answer pool and reranker

Compare top_k answers, then reconstruct and rerank their candidate pool.

Run order inside this file:
1. Do it: the same question at top_k 5 and top_k 20 (source window 10)
2. Do it: embed, pool, rank, compare (source window 13)

Prerequisites: setup_prepare.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_the_same_question_at_top_k_5_and_top_k_20(session):
    """Run Do it: the same question at top_k 5 and top_k 20 at this checkpoint.

    The cell asks the notice-period question twice and prints, for each answer, the stages block on one line and every citation with its score, its chunk position, its source and the start of its quote. The second answer offers the model twenty chunks instead of five.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.lesson31 import require_fresh_vector
    import os, json, subprocess, urllib.request
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = os.environ.get("Q", "What is the notice period for a confirmed E3?")
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"],
                         capture_output=True, text=True, check=True).stdout.strip()
    def ask(top_k):
        req = urllib.request.Request(f"{API}/v1/query", method="POST", data=json.dumps({"query": Q, "tenant_id": "acme", "stream": False, "top_k": top_k}).encode(),
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    for k in (5, 20):
        j = ask(k); s = j["stages"]
        require_fresh_vector(j)
        json.dump(j, open(f"/tmp/ans53_{k}.json", "w"))
        print(f"\ntop_k {k}: pool {s['pool']} | from the index {s['vector_chunks']} | retrieve {s['retrieve_ms']} + rerank {s['rerank_ms']} + generate {s['generate_ms']} ms of {j['latency_ms']} | rerank_fallback {s.get('rerank_fallback', 0)} | cache_hit {j['cache_hit']}")
        print(f"   {len(j['citations'])} citations: the sources the model used, in the order it used them; [N] in the answer is the packed position")
        for i, c in enumerate(j["citations"], 1):
            print(f"   [{i}] score {c['score']:.4f}  #{c['chunk_id'].rsplit('#', 1)[1]:>3}  {c['source_uri'].split('/')[-1][:26]:26} p.{c.get('page') or '-'}  {c['quote'][:44]!r}")
        print("   sorted by score, the ranker's order among them:", [f"#{c['chunk_id'].rsplit('#', 1)[1]}" for c in sorted(j["citations"], key=lambda c: -c["score"])])
    print("\nsaved /tmp/ans53_5.json and /tmp/ans53_20.json for steps 4, 7 and 8")

def step_02_embed_pool_rank_compare(session):
    """Run Do it: embed, pool, rank, compare at this checkpoint.

    Do it: embed, pool, rank, compare

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding and one rank request, well under a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, time, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google import genai
    from google.cloud import aiplatform, firestore
    from google.cloud import discoveryengine_v1 as discoveryengine
    from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
    PROJECT, REGION = os.environ["PROJECT"], os.environ["REGION"]
    ENDPOINT, DEPLOYED = os.environ["VECTOR_INDEX_ENDPOINT"], os.environ["VECTOR_DEPLOYED_INDEX_ID"]
    Q = os.environ.get("Q", "What is the notice period for a confirmed E3?")
    client = genai.Client(enterprise=True, project=PROJECT, location=REGION)              # the API embeds in its own region
    t = time.perf_counter()
    vec = list(client.models.embed_content(model="text-embedding-005", contents=[Q],
                                           config={"output_dimensionality": 768, "task_type": "RETRIEVAL_QUERY"}).embeddings[0].values)
    aiplatform.init(project=PROJECT, location=REGION)
    hits = aiplatform.MatchingEngineIndexEndpoint(ENDPOINT).find_neighbors(deployed_index_id=DEPLOYED, queries=[vec], num_neighbors=20,
                                                                          filter=[Namespace(name="tenant_id", allow_tokens=["acme"])])[0]
    db = firestore.Client(project=PROJECT)
    pool = []                                                        # _hydrate(): the payloads in the index's order, score = the distance
    for n in hits:
        row = db.collection("chunks").document(n.id).get().to_dict() or {}
        if row.get("current") is False:
            continue                                                 # prefer_current(): a retired row never reaches the ranker
        pool.append({"id": n.id, "score": n.distance, "text": row.get("text", ""), "locator": row.get("locator", "?"),
                     "source": row.get("source_uri", "").split("/")[-1], "found_by": "vector"})
    print(f"pool: {len(pool)} current ids from the index in {int((time.perf_counter() - t) * 1000)} ms, every one found_by vector")
    ranker = discoveryengine.RankServiceClient()                                          # retriever._ranker()
    config = ranker.ranking_config_path(project=PROJECT, location="global", ranking_config="default_ranking_config")
    records = [discoveryengine.RankingRecord(id=str(i), content=c["text"]) for i, c in enumerate(pool[:200])]
    t = time.perf_counter()
    resp = ranker.rank(request=discoveryengine.RankRequest(ranking_config=config, model="semantic-ranker-fast-004",
                                                            top_n=len(pool), query=Q, records=records), timeout=5.0)
    print(f"ranker: {len(resp.records)} of {len(pool)} back in {int((time.perf_counter() - t) * 1000)} ms, {len(records)} records sent, model semantic-ranker-fast-004")
    ranked = [(int(r.id), r.score) for r in resp.records]
    for rank, (i, score) in enumerate(ranked[:5], 1):
        print(f"   rank {rank}  score {score:.4f}  pool #{i + 1:>2}  {pool[i]['locator']:9} {pool[i]['source'][:28]}")
    try:
        ans = json.load(open("/tmp/ans53_5.json"))
        cited = [c["chunk_id"] for c in sorted(ans["citations"], key=lambda c: -c["score"])]
        hand = [pool[i]["id"] for i, _ in ranked[:5]]
        print("the API's cited ids, by score:", [f"#{c.rsplit('#', 1)[1]}" for c in cited], "| by hand, first 5:", [f"#{c.rsplit('#', 1)[1]}" for c in hand])
        print("every citation is in the by-hand top 5:", all(c in hand for c in cited), "| in the same relative order:", [c for c in hand if c in cited] == cited)
    except FileNotFoundError:
        print("run step 3 first to compare with the API's citations")
    json.dump({"question": Q, "pool": pool, "ranked": ranked}, open("/tmp/pool53.json", "w"))
    print("saved /tmp/pool53.json for steps 5, 7 and 8")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_the_same_question_at_top_k_5_and_top_k_20),
        ('source_13', step_02_embed_pool_rank_compare),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
