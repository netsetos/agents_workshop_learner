"""Lesson 3.3 / s5: Batches: 250 texts and 15,000 tokens per request

Summary and purpose:
The loader's copy of the rule, on the chunks you cut in lesson 3.2. No call is made; a plan is printed.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_embed_one_clause_yourself_both_ways
Expected observation: handbook: 283 chunks, 158,692 chars -> 4 requests of [85, 78, 78, 42] texts, est tokens [14833, 14949, 14944, 8057]
wages mirror: 65 chunks, 102,444 chars -> 3 requests of [28, 28, 9] texts, est tokens [...]
the handbook in one request would carry about 52,783 estimated tokens: over 20,000, refused whole

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L621

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: plan the handbook, Rs 0 at this checkpoint.

    The loader's copy of the rule, on the chunks you cut in lesson 3.2. No call is made; a plan is printed.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path.insert(0, ".")
    from shared import documind_corpus as dc
    def cut(path, slug):
        text = open(path, encoding="utf-8").read()
        return [c["text"] for c in dc.chunk_document({"slug": slug, "doc_type": "x", "source_uri": "gs://x", "text": text}, "acme")]
    for name, texts in (("handbook", cut("evals/corpus/acme/hr_policy_2026.md", "hr_policy_2026")),
                        ("wages mirror", cut("evals/corpus/acme/code_on_wages_2019.md", "code_on_wages_2019"))):
        plan = dc.embed_batches(texts)
        est = [sum(max(1, len(t) // dc.CHARS_PER_TOKEN) for t in b) for b in plan]
        print(f"{name}: {len(texts)} chunks, {sum(map(len, texts)):,} chars -> {len(plan)} requests of {[len(b) for b in plan]} texts, est tokens {est}")
    one = sum(max(1, len(t) // 3) for t in cut("evals/corpus/acme/hr_policy_2026.md", "hr_policy_2026"))
    print(f"the handbook in one request would carry about {one:,} estimated tokens: over 20,000, refused whole")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
