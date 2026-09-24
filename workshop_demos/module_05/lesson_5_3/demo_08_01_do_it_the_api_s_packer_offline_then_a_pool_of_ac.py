"""Lesson 5.3 / s8: What the funnel costs, its knobs, and the packed set the citations come from

Summary and purpose:
The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: pure Python over the saved pool and a file in the kit)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_03_do_it_the_join_then_the_kit_s_own_retrieval_in_y
Expected observation: the budget: 7,832 tokens for the chunks, 168 for the fixed prompt, 2,048 reserved for the answer
your ranked pool, top_k 5    packed  5, dropped  0, context   7xx tokens
your ranked pool, top_k 20   packed 20, dropped  0, context  2xxx tokens
twenty full CGST Act pages   packed 15, dropped  5, context  7633 tokens
the first header the model reads: [Source 1] hr_policy_2026.md

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L896

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
