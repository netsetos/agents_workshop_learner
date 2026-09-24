"""Lesson 6.2 / s3: The contract offline: drafts that pass, drafts that fail, and the resolver on the kit's chunks

Summary and purpose:
Do it: six drafts, one resolution, two refusals

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: resolved: 2 of 3 citations kept: source 7 was out of range and dropped, not raised
   acme:hr_policy_2026#NP-03      page 1 score 0.0 kind text quote 'NP-03 — Notice period A confirmed employee a'
   acme:hr_policy_2026#PB-02      page 1 score 0.0 kind text quote 'PB-02 — Probation New joiners serve six mont'
RAGAnswer: {"answer": "A confirmed employee in grade E3 serves the notice period in NP-03 [1]; probation is different [2].", "citations": [{" ...
refused (source 0, [Source N] is 1-based): citations.0.source: Input should be greater than or equal to 1
refused (confidence outside high|medium|low): confidence: Input should be 'high', 'medium' or 'low'
refused (a quote over the draft's limit): citations.0.quote: String should have at most 200 characters
the model's refusal, resolved: {'answer': 'The context does not contain the answer.', 'citations': [], 'confidence': 'low', 'answerabl

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L471

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: six drafts, one resolution, two refusals at this checkpoint.

    Do it: six drafts, one resolution, two refusals

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, sys, json
    sys.path[:0] = [".", "services/rag-api"]
    from pydantic import ValidationError
    from shared.documind_schemas import ModelDraft, resolve                                      # the one contract, imported everywhere
    from shared import documind_corpus as dc
    handbook = dc.chunk_document({"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://uploads/acme/hr_policy_2026.md",
                                  "text": open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()}, "acme")
    packed = [next(c for c in handbook if c["locator"] == L) for L in ("NP-03", "PB-02")]         # two packed chunks, as the packer hands them over
    words = lambda t, n: " ".join(t.split()[:n])
    good = {"answer": "A confirmed employee in grade E3 serves the notice period in NP-03 [1]; probation is different [2].",
            "citations": [{"source": 1, "quote": words(packed[0]["text"], 12)}, {"source": 2, "quote": words(packed[1]["text"], 10)},
                          {"source": 7, "quote": "a source that was never packed"}],
            "confidence": "high", "answerable": True}
    draft = ModelDraft.model_validate(good)
    ans = resolve(draft, packed)
    print("resolved:", len(ans.citations), "of", len(draft.citations), "citations kept: source 7 was out of range and dropped, not raised")
    for c in ans.citations:
        print(f"   {c.chunk_id:30} page {c.page} score {c.score} kind {c.kind} quote {c.quote[:44]!r}")
    print("RAGAnswer:", json.dumps(ans.model_dump(), ensure_ascii=False)[:130], "...")
    for bad, why in (({**good, "citations": [{"source": 0, "quote": "x"}]}, "source 0, [Source N] is 1-based"),
                     ({**good, "confidence": "certain"}, "confidence outside high|medium|low"),
                     ({**good, "citations": [{"source": 1, "quote": "w " * 120}]}, "a quote over the draft's limit")):
        try:
            ModelDraft.model_validate(bad); print("accepted?!", why)
        except ValidationError as e:
            print(f"refused ({why}): {'.'.join(str(x) for x in e.errors()[0]['loc'])}: {e.errors()[0]['msg']}")
    refusal = resolve(ModelDraft.model_validate({"answer": "The context does not contain the answer.", "citations": [], "confidence": "low", "answerable": False}), packed)
    print("the model's refusal, resolved:", refusal.model_dump())
    E = next(ast.literal_eval(n.value) for n in ast.parse(open("services/rag-api/main.py", encoding="utf-8").read()).body
             if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "EMPTY_POOL_ANSWER")
    print("the empty pool's, written by the API without a model:", E[:96], "...")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
