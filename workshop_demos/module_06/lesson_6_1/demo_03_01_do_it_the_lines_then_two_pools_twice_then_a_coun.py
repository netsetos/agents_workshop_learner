"""Lesson 6.1 / s3: The budget's lines and the packer, offline on the kit's own documents

Summary and purpose:
Do it: the lines, then two pools twice, then a counter

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: 4.5's teaching split: system 1500 | tenant_pack 40000 | chunks 6000 | history 2000 | answer 2000 | input_total 49500
the API's, this question: system 168 (the fixed prompt, 672 characters) | chunks 7832 | tenant_pack 0 | history 0 | answer 2048 | input_total 8000

handbook sections, top_k 5: packed 5, dropped 0, context 301 tokens | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] hr_policy_2026.md, p.1  (32 tokens)

handbook sections, top_k 20: packed 20, dropped 0, context 2009 tokens | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] hr_policy_2026.md, p.1  (32 tokens)

full Act pages, top_k 5: packed 5, dropped 0, cont

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L482

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the lines, then two pools twice, then a counter at this checkpoint.

    Do it: the lines, then two pools twice, then a counter

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, sys
    sys.path[:0] = [".", "services/rag-api", "services/ingest"]
    from context_budget import TokenBudget, estimate_tokens, source_header, pack_chunks     # pure Python: no cloud calls
    from contracts import effective_from_of                                                # the worker's reader of a document's date
    from shared import documind_corpus as dc
    K = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(open("services/rag-api/generator.py", encoding="utf-8").read()).body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("SYSTEM", "DATED_RULE")}
    Q = "What is the notice period for a confirmed E3?"
    fixed = f"{K['SYSTEM']}{K['DATED_RULE']}\n\nContext:\n\n\nQuestion: {Q}"                 # generator._budget(), line for line
    b, t = TokenBudget.fit(8000, fixed, estimate_tokens, answer=2048), TokenBudget()
    print(f"4.5's teaching split: system {t.system} | tenant_pack {t.tenant_pack} | chunks {t.chunks} | history {t.history} | answer {t.answer} | input_total {t.input_total}")
    print(f"the API's, this question: system {b.system} (the fixed prompt, {len(fixed)} characters) | chunks {b.chunks} | tenant_pack {b.tenant_pack} | history {b.history} | answer {b.answer} | input_total {b.input_total}")
    def chunks_of(path, name):
        text = open(path, encoding="utf-8").read()
        out = dc.chunk_document({"slug": name.rsplit(".", 1)[0], "doc_type": "policy", "source_uri": f"gs://uploads/acme/{name}", "text": text}, "acme")
        date = effective_from_of(name, text)                                                # what indexer.py stamps on every row of a dated document
        for c in out:
            if date:
                c["effective_from"] = date
        return out
    handbook, note = chunks_of("evals/corpus/acme/hr_policy_2026.md", "hr_policy_2026.md"), chunks_of("evals/demo/smoke_note_v2.md", "smoke_note.md")
    act = sorted(chunks_of("evals/corpus/acme/cgst_act_2017.md", "cgst_act_2017.md"), key=lambda c: (-len(c["text"]), c["locator"]))
    anchor = [c for c in handbook if c["locator"] == "NP-03"]
    for name, pool in (("handbook sections", anchor + note[:1] + [c for c in handbook if c["locator"] != "NP-03"][:18]), ("full Act pages", anchor + note[:1] + act[:18])):
        for k in (5, 20):
            context, packed, dropped = pack_chunks(pool[:k], b.chunks, estimate_tokens)
            print(f"\n{name}, top_k {k}: packed {len(packed)}, dropped {len(dropped)}, context {estimate_tokens(context)} tokens"
                  + (f" | log: context_budget_drop packed={len(packed)} dropped={len(dropped)}" if dropped else "") + (" | the dated rule is added" if any(c.get("effective_from") for c in packed) else ""))
            for i, c in enumerate(packed[:3], 1):
                print("   " + source_header(i, c) + f"  ({estimate_tokens(source_header(i, c) + chr(10) + c['text'])} tokens)")
    worse = lambda s: int(len(s) / 2.5)                                                     # a counter for a script that costs more tokens a character
    context, packed, dropped = pack_chunks((anchor + note[:1] + act[:18])[:20], b.chunks, worse)
    print(f"\nfull Act pages, top_k 20, with a counter injected that reads 60 percent more: packed {len(packed)}, dropped {len(dropped)}, trimmed from the tail after the estimate had packed them")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
