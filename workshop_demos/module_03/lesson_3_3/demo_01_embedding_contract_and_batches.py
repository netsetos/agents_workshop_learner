"""Lesson 3.3: demo 01 embedding contract and batches

Trace the declared embedding, embed a clause under both task types and inspect batching.

Run order inside this file:
1. Call it: three reads of one pair (source window 11)
2. Do it: embed one clause yourself, both ways (source window 14)
3. Do it: plan the handbook, Rs 0 (source window 18)

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


# Original CLI workflow for step_01_three_reads_of_one_pair.
COMMANDS_01 = """gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep -E 'EMBEDDING_MODEL|EMBEDDING_VERSION'

curl -s "$API/version" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; j=json.load(sys.stdin); print('api serves embedding', j['embedding'], '| generator', j['generator_model'], '| retrieval', j['retrieval_mode'], j['retrieval_backend'])"

curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; [print(f\\"{r['name']:44} chunks {r['chunks']:>4}  reused {r['reused']:>4}  embedded {r['embedded']:>4}  {r['embedding']}\\") for r in json.load(sys.stdin)['sources']]"

"""

def step_01_three_reads_of_one_pair(session):
    """Run Call it: three reads of one pair at this checkpoint.

    All read-only. The first prints the worker's environment, the second asks the API what it is serving, the third reads the pair off the ledger rows the Versions table renders.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_embed_one_clause_yourself_both_ways(session):
    """Run Do it: embed one clause yourself, both ways at this checkpoint.

    This cell costs money, a very small amount: two calls on a 234-character clause, about a tenth of a paisa. It reads NP-03's text and stored vector off the lane, embeds the same text under the document profile with the worker's exact settings, and compares by cosine. Then it embeds the same text under the query profile and compares again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash; two paid calls).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, math, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    from google import genai
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    row = next(db.collection("chunks").where("tenant_id", "==", "acme")
                 .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md")
                 .where("current", "==", True).where("locator", "==", "NP-03").stream()).to_dict()
    lane = list(row["embedding"])
    client = genai.Client(enterprise=True, project=PROJECT, location="us-central1")   # embeddings are regional
    def embed(text, task):
        r = client.models.embed_content(model="text-embedding-005", contents=[text],
                                        config={"output_dimensionality": 768, "task_type": task})
        return list(r.embeddings[0].values)
    def cosine(a, b):
        return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    doc, qry = embed(row["text"], "RETRIEVAL_DOCUMENT"), embed(row["text"], "RETRIEVAL_QUERY")
    print("lane vector:", len(lane), "numbers; first three", [round(v, 4) for v in lane[:3]])
    print("same text, RETRIEVAL_DOCUMENT: cosine to the lane's vector", round(cosine(doc, lane), 4))
    print("same text, RETRIEVAL_QUERY:    cosine to the lane's vector", round(cosine(qry, lane), 4))

def step_03_plan_the_handbook_rs_0(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_11', step_01_three_reads_of_one_pair),
        ('source_14', step_02_embed_one_clause_yourself_both_ways),
        ('source_18', step_03_plan_the_handbook_rs_0),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
