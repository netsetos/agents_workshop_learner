"""Lesson 6.2: demo 01 answer contract and citations

Validate draft shapes and resolve a real answer's quotes against its rows.

Run order inside this file:
1. Do it: six drafts, one resolution, two refusals (source window 12)
2. Do it: one question, two halves, three rows (source window 16)

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


def step_01_six_drafts_one_resolution_two_refusals(session):
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

def step_02_one_question_two_halves_three_rows(session):
    """Run Do it: one question, two halves, three rows at this checkpoint.

    Do it: one question, two halves, three rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question and three Firestore reads, a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, re, json, subprocess, urllib.request, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"], capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(f"{API}/v1/query", method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                                 data=json.dumps({"query": "What is the notice period for a confirmed E3?", "tenant_id": "acme", "stream": False, "top_k": 3}).encode())
    j = json.load(urllib.request.urlopen(req, timeout=180))
    print("the contract:", json.dumps({"answer": j["answer"][:90] + "...", "citations": f"{len(j['citations'])} citations", "confidence": j["confidence"], "answerable": j["answerable"]}, ensure_ascii=False))
    print("the envelope:", {k: j[k] for k in ("model", "backend", "tokens_in", "tokens_out", "cached_tokens", "cost_usd", "latency_ms", "cache_hit")})
    print("[N] marks in the answer:", sorted(set(re.findall(r"\[(\d+)\]", j["answer"])), key=int), "| citations returned:", len(j["citations"]))
    db = firestore.Client(project=PROJECT)
    norm = lambda s: " ".join(s.split()).lower()
    for i, c in enumerate(j["citations"], 1):
        row = db.collection("chunks").document(c["chunk_id"]).get().to_dict() or {}
        print(f"   [{i}] #{c['chunk_id'].rsplit('#', 1)[1]:>3} {c['source_uri'].split('/')[-1][:24]:24} page {c['page']} score {c['score']:.4f} kind {c['kind']} | row found {bool(row)} | quote in the row {norm(c['quote']) in norm(row.get('text', ''))} | {len(c['quote'].split())} words")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_12', step_01_six_drafts_one_resolution_two_refusals),
        ('source_16', step_02_one_question_two_halves_three_rows),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
