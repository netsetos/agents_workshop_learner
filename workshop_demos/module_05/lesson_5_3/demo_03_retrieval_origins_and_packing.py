"""Lesson 5.3: demo 03 retrieval origins and packing

Join citations to retrieval origins, run smoke and inspect the packed evidence set.

Run order inside this file:
1. Do it: the join, then the kit's own retrieval in your process, then the smoke (source window 35)
2. Do it: the join, then the kit's own retrieval in your process, then the smoke (source window 37)
3. Do it: the join, then the kit's own retrieval in your process, then the smoke (source window 39)
4. Do it: the API's packer offline, then a pool of Act pages on the lane (source window 43)
5. Do it: the API's packer offline, then a pool of Act pages on the lane (source window 45)

Prerequisites: demo_02_fallback_and_stage_latency.
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


def step_01_the_join_then_the_kit_s_own_retrieval_in_y(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; Rs 0: two files on disk).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json
    ans, d = json.load(open("/tmp/ans53_5.json")), json.load(open("/tmp/pool53.json"))
    stamp = {c["id"]: c["found_by"] for c in d["pool"]}
    s = ans["stages"]
    print(f"the answer's counts: pool {s['pool']} | vector_chunks {s['vector_chunks']} | graph_chunks {s['graph_chunks']} | managed_chunks {s['managed_chunks']} | retrieval_backend {s['retrieval_backend']}")
    print("a citation's fields:", sorted(ans["citations"][0]))
    for c in ans["citations"]:
        print(f"   #{c['chunk_id'].rsplit('#', 1)[1]:>3} {c['source_uri'].split('/')[-1][:26]:26} found_by {stamp.get(c['chunk_id'], 'not in the pool you fetched')}   (by the join)")

def step_02_the_join_then_the_kit_s_own_retrieval_in_y(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings, collections
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path[:0] = [".", "services/rag-api"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])          # settings.project_id; REGION and the index names are already exported
    for k in ("RETRIEVAL_MODE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY", "TOP_K_RETRIEVE", "RERANK_TIMEOUT_S", "SEMANTIC_CACHE"):
        if os.environ.get(k) == "":
            del os.environ[k]                                                      # an empty export from an earlier names box means the default
    from retriever import retrieve                                                # the kit's own path: the index, the Firestore fan-out, prefer_current, the stamps
    pool = retrieve("What is the notice period for a confirmed E3?", "acme", 5)
    print(len(pool), "chunks in the pool, found_by:", dict(collections.Counter(c["found_by"] for c in pool)))
    print("first three:", [(c.get("locator", "?"), c["found_by"], round(c["score"], 4)) for c in pool[:3]])

# Original CLI workflow for step_03_the_join_then_the_kit_s_own_retrieval_in_y.
COMMANDS_03 = """DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme \\
DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep -E "query|vector tier|no token|PASS|FAIL"

"""

def step_03_the_join_then_the_kit_s_own_retrieval_in_y(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def step_04_the_api_s_packer_offline_then_a_pool_of_ac(session):
    """Run Do it: the API's packer offline, then a pool of Act pages on the lane at this checkpoint.

    The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: pure Python over the saved pool and a file in the kit).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, sys, json
    sys.path[:0] = [".", "services/rag-api"]
    from context_budget import pack_chunks, estimate_tokens, TokenBudget, source_header     # pure Python: no cloud calls
    from shared import documind_corpus as dc
    d = json.load(open("/tmp/pool53.json"))
    tree = ast.parse(open("services/rag-api/generator.py", encoding="utf-8").read())
    consts = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
              if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("SYSTEM", "DATED_RULE")}
    fixed = f"{consts['SYSTEM']}{consts['DATED_RULE']}\n\nContext:\n\n\nQuestion: {d['question']}"     # generator._budget(), line for line
    budget = TokenBudget.fit(8000, fixed, estimate_tokens, answer=2048)
    print(f"the budget: {budget.chunks} tokens for the chunks, {budget.system} for the fixed prompt, {budget.answer} reserved for the answer")
    ranked = [dict(d["pool"][i], source_uri="gs://uploads/acme/" + d["pool"][i]["source"], rerank_score=s) for i, s in d["ranked"]]   # the ranker's order, step 4
    act = open("evals/corpus/acme/cgst_act_2017.md", encoding="utf-8").read()
    pages = dc.chunk_document({"slug": "cgst_act_2017", "doc_type": "policy", "source_uri": "gs://uploads/acme/cgst_act_2017.md", "text": act}, "acme")
    full = sorted(pages, key=lambda c: -len(c["text"]))[:20]                       # twenty full pages, the kit's mirror cut by the kit's chunker
    for name, chunks in (("your ranked pool, top_k 5", ranked[:5]), ("your ranked pool, top_k 20", ranked[:20]), ("twenty full CGST Act pages", full)):
        context, packed, dropped = pack_chunks(chunks, budget.chunks, estimate_tokens)
        print(f"{name:28} packed {len(packed):2}, dropped {len(dropped):2}, context {estimate_tokens(context):5} tokens")
    print("the first header the model reads:", source_header(1, ranked[0]))

# Original CLI workflow for step_05_the_api_s_packer_offline_then_a_pool_of_ac.
COMMANDS_05 = """curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the maximum rate of central tax the CGST Act allows?","tenant_id":"acme","stream":false,"top_k":20}' \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('pool', s['pool'], '| citations', len(j['citations']), '| generate_ms', s['generate_ms'], '| tokens_in', j['tokens_in'], '| sources', sorted({c['source_uri'].split('/')[-1][:20] for c in j['citations']}))"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="context_budget_drop"' \\
  --project "$PROJECT" --freshness 1h --limit 3 --format='value(timestamp,jsonPayload.packed,jsonPayload.dropped)'

"""

def step_05_the_api_s_packer_offline_then_a_pool_of_ac(session):
    """Run Do it: the API's packer offline, then a pool of Act pages on the lane at this checkpoint.

    The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_05)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_35', step_01_the_join_then_the_kit_s_own_retrieval_in_y),
        ('source_37', step_02_the_join_then_the_kit_s_own_retrieval_in_y),
        ('source_39', step_03_the_join_then_the_kit_s_own_retrieval_in_y),
        ('source_43', step_04_the_api_s_packer_offline_then_a_pool_of_ac),
        ('source_45', step_05_the_api_s_packer_offline_then_a_pool_of_ac),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
