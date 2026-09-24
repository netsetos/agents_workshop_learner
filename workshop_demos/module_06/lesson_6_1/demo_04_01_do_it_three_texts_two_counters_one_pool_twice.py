"""Lesson 6.1 / s4: The model's counter beside the estimate: English, Hindi, and a pool trimmed by the exact count

Summary and purpose:
Do it: three texts, two counters, one pool twice

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; a handful of count_tokens calls)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_lines_then_two_pools_twice_then_a_coun
Expected observation: NP-03, English     chars   234  estimate  58  counted  1xx  ratio x.xx  (near one)
a clause in Hindi  chars    72  estimate   18  counted   xx  ratio x.xx  (well above one)
one Act page       chars  2000  estimate  500  counted  4xx  ratio x.xx  (near one)
twenty Act pages under the estimate     : packed 15, dropped 5, context 7633 tokens by that counter
twenty Act pages under the model's count: packed 1x, dropped x, context 7xxx tokens by that counter

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L563

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
