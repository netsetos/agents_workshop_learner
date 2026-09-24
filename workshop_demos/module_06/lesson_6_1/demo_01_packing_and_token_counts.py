"""Lesson 6.1: demo 01 packing and token counts

Run the kit packer and compare its estimate with exact model token counts.

Run order inside this file:
1. Do it: the lines, then two pools twice, then a counter (source window 14)
2. Do it: three texts, two counters, one pool twice (source window 17)

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


def step_01_the_lines_then_two_pools_twice_then_a_coun(session):
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

def step_02_three_texts_two_counters_one_pool_twice(session):
    """Run Do it: three texts, two counters, one pool twice at this checkpoint.

    Do it: three texts, two counters, one pool twice

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; a handful of count_tokens calls).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    sys.path[:0] = [".", "services/rag-api"]
    from google import genai
    from context_budget import estimate_tokens, pack_chunks
    from shared import documind_corpus as dc
    client = genai.Client(enterprise=True, project=os.environ["PROJECT"], location="global")        # 3.x counting is served from global, as generation is
    MODEL = os.environ.get("GENERATOR_MODEL", "gemini-3.6-flash")
    count = lambda s: client.models.count_tokens(model=MODEL, contents=s).total_tokens
    doc = lambda name: {"slug": name.rsplit(".", 1)[0], "doc_type": "policy", "source_uri": f"gs://uploads/acme/{name}", "text": open(f"evals/corpus/acme/{name}", encoding="utf-8").read()}
    handbook = dc.chunk_document(doc("hr_policy_2026.md"), "acme")
    act = sorted(dc.chunk_document(doc("cgst_act_2017.md"), "acme"), key=lambda c: (-len(c["text"]), c["locator"]))
    np03 = next(c for c in handbook if c["locator"] == "NP-03")["text"]
    hindi = "सूचना अवधि: पुष्टि किए गए कर्मचारी के लिए तीस दिन, परिवीक्षा पर सात दिन।"
    for name, s in (("NP-03, English", np03), ("a clause in Hindi", hindi), ("one Act page", act[0]["text"])):
        e, n = estimate_tokens(s), count(s)
        print(f"{name:18} chars {len(s):5}  estimate {e:4}  counted {n:4}  ratio {n / e:.2f}")
    for label, fn in (("the estimate", estimate_tokens), ("the model's count", count)):
        context, packed, dropped = pack_chunks(act[:20], 7832, fn)
        print(f"twenty Act pages under {label:17}: packed {len(packed)}, dropped {len(dropped)}, context {fn(context)} tokens by that counter")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_14', step_01_the_lines_then_two_pools_twice_then_a_coun),
        ('source_17', step_02_three_texts_two_counters_one_pool_twice),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
