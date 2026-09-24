"""Lesson 13.1 / s3: The trail, as the kit writes it down

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: the envelope on every answer, beyond the contract (schemas.py, RAGResponse):
  model, backend, cost_usd, tokens_in, tokens_out, cached_tokens, latency_ms, stages, cache_hit
stages, as query() fills them (main.py):
  generate_ms, graph_chunks, managed_chunks, policy_fallback, pool, rerank_fallback, rerank_ms, retrieval_backend, retrieve_ms, vector_chunks
found_by, the rung that put a chunk in the pool (retriever.py):
  firestore, graph, rag_engine, vector, vertex_search
GET /version, what is serving (main.py):
  model_backend, generator_model, prompt, retrieval_mode, retrieval_backend, retrieval_graph, graph_backend, embedding, retrieval_current_only, semantic_cache, git_sha
the events a degraded answer leaves in documind-api's log:
  routing_fallback         main.py:96
  retrieval_pin_ignored    main.py:135
  rag_engine_fallback      retriever.py:200
  rag_engine_fallback      retriever.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html#L464

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, re
    root = "services/rag-api/"
    main, ret = (open(root + f, encoding="utf-8").read() for f in ("main.py", "retriever.py"))
    tree = ast.parse(open(root + "schemas.py", encoding="utf-8").read())
    env = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "RAGResponse")
    print("the envelope on every answer, beyond the contract (schemas.py, RAGResponse):")
    print("  " + ", ".join(n.target.id for n in env.body if isinstance(n, ast.AnnAssign)))
    q = main[main.index("def query("):main.index("def _record(")]
    keys = set(re.findall(r'stages\["(\w+)"\]', q)) | {n + "_ms" for n in re.findall(r'stage\(stages, "(\w+)"\)', q)}
    print("stages, as query() fills them (main.py):")
    print("  " + ", ".join(sorted(keys)))
    print("found_by, the rung that put a chunk in the pool (retriever.py):")
    print("  " + ", ".join(sorted(set(re.findall(r'found_by"\]? ?[:=] ?"(\w+)"', ret)))))
    v = main[main.index("def version():"):main.index('@app.get("/v1/sources")')]
    print("GET /version, what is serving (main.py):")
    print("  " + ", ".join(re.findall(r'"(\w+)":', v)))
    print("the events a degraded answer leaves in documind-api's log:")
    for f in ("main.py", "retriever.py", "generator.py", "cache_manager.py"):
        for i, line in enumerate(open(root + f, encoding="utf-8"), 1):
            for ev in re.findall(r'"event": "(\w+(?:fallback|stale|ignored|exhausted|truncated))"', line):
                print(f"  {ev:24} {f}:{i}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
