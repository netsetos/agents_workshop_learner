"""Lesson 17.2: demo 01 sanitize and validate

Run the sanitization/validation gates and inspect the accepted dataset.

Run order inside this file:
1. Do it (source window 9)
2. Do it (source window 12)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """python evals/make_trainset.py --selftest
python evals/tune.py --selftest
python - <<'PY'
import ast, re, sys, types
sys.path[:0] = ["evals"]
import tune                                          # stdlib only when imported: no SDK, no project, no network
for base, adapter in (("gemini-3.6-flash", 4), ("gemini-3.1-flash-lite", 3), ("gemini-3.1-flash-lite", 32)):
    try:
        print(f"{base}, adapter {adapter}: accepted, {tune.config_for(base, 3, adapter, 'documind-sft-v2')['adapter_size']}")
    except SystemExit as e:
        print(f"{base}, adapter {adapter}: refused before submission: {str(e).split(': ', 1)[1].split('. ', 1)[0]}")
print(f"make tune's defaults: {tune.config_for('gemini-3.1-flash-lite', 3, 4, 'documind-sft-v1')}")
fn = next(n for n in ast.parse(open("services/rag-api/generator.py", encoding="utf-8").read()).body
          if isinstance(n, ast.FunctionDef) and n.name == "_endpoint_location")


def location(model, override="", region="asia-south1"):     # generator.py builds its clients when imported: the rule is lifted out
    ns = {"re": re, "settings": types.SimpleNamespace(generator_location=override, region=region)}
    exec(compile(ast.Module([fn], []), "generator.py", "exec"), ns)
    return ns["_endpoint_location"](model)


EP = "projects/NUMBER/locations/us/endpoints/ENDPOINT_ID"
print(f"an endpoint whose path says us is called at: {location(EP)}; with GENERATOR_LOCATION=us-central1: {location(EP, 'us-central1')}")
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the two self-tests and the rules; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the bucket and Firestore; one DLP scan in asia-south1).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import hashlib, json, os, sys
    sys.path[:0] = [".", "evals", "services/rag-api"]
    P, V = os.environ["PROJECT"], "v2"
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", P)              # shared/pii and shared/tenancy find the project here
    from google.cloud import storage
    import make_trainset as mt
    from context_budget import estimate_tokens
    from shared import tenancy
    from shared.documind_schemas import ModelDraft
    from shared.pii import LOCATION, MIN_LIKELIHOOD, inspect_many
    bucket = storage.Client(project=P).bucket(f"{P}-datasets")
    m = json.loads(bucket.blob(f"sft/documind_sft_{V}.manifest.json").download_as_text())
    print(f"the file make tune VERSION={V} reads: gs://{P}-datasets/sft/documind_sft_{V}.vertex.jsonl")
    data, same = {}, True
    for fmt, f in m["files"].items():
        data[fmt] = bucket.blob("sft/" + os.path.basename(f["path"])).download_as_bytes()
        ok = hashlib.sha256(data[fmt]).hexdigest() == f["sha256"]
        same &= ok
        print(f"  {fmt:6} sha256 {'as the manifest says' if ok else 'DIFFERS FROM THE MANIFEST'}")
    vertex = [json.loads(l) for l in data["vertex"].decode("utf-8").splitlines()]
    chat = [json.loads(l) for l in data["chat"].decode("utf-8").splitlines()]
    shape = sum(bool(v["systemInstruction"]["parts"][0].get("text")) and [c["role"] for c in v["contents"]] == ["user", "model"]
                and all(list(p) == ["text"] for c in v["contents"] for p in c["parts"]) for v in vertex)
    twin = sum([x["content"] for x in c["messages"]] == [v["systemInstruction"]["parts"][0]["text"]] + [x["parts"][0]["text"] for x in v["contents"]]
               for v, c in zip(vertex, chat))
    drafts = [ModelDraft.model_validate_json(v["contents"][1]["parts"][0]["text"]) for v in vertex]
    print(f"1. the shape: {shape} of {len(vertex)} rows are a system instruction, a user turn and a model turn, text only; "
          f"the chat file says the same in {twin}; targets that parse as ModelDraft: {len(drafts)}")
    chunks = {c["text"].strip(): c for c in mt.load_chunks(m["tenant"])}
    rows = []
    for v, d in zip(vertex, drafts):
        user = v["contents"][0]["parts"][0]["text"]
        text = user.split("[Source 1] ", 1)[1].rsplit("\n\nQuestion: ", 1)[0]
        c = chunks[text.strip()]
        rows.append({"chunk_id": c["chunk_id"], "source_uri": c["source_uri"], "text": text,
                     "question": user.rsplit("\n\nQuestion: ", 1)[1], "answer": d.answer})
    golden = [json.loads(l) for l in open("evals/golden.jsonl", encoding="utf-8") if l.strip()]
    dropped = mt.exclude_golden(rows, golden)[1]
    print(f"2. the test set: the golden set ({len(golden)} rows) would drop {len(dropped)} of {len(rows)}")
    qa = inspect_many([x for r in rows for x in (r["question"], r["answer"])])
    qa_rows = sum(bool(qa[2 * i] or qa[2 * i + 1]) for i in range(len(rows)))
    hits = [(r["chunk_id"], sorted({f["info_type"] for f in fs})) for r, fs in zip(rows, inspect_many([r["text"] for r in rows])) if fs]
    n_rows = lambda n: f"{n} row" + ("" if n == 1 else "s")
    print(f"3. personal data, by the kit's own scan (DLP in {LOCATION}, {MIN_LIKELIHOOD} or above; findings, never the values):")
    print(f"   in the questions and answers, which make trainset scans: {n_rows(qa_rows)}")
    print(f"   in the chunks the user turns carry, which it does not: {n_rows(len(hits))}")
    for cid, kinds in hits:
        print(f"     {cid}: {', '.join(kinds)}")
    policy = tenancy.policy_for(m["tenant"])
    leaves = tenancy.permits(policy, "us-central1")
    print(f"4. residency: the rows are {m['tenant']}'s, whose data_region is {policy}; may they be held in us-central1? {leaves}")
    toks = [estimate_tokens(v["systemInstruction"]["parts"][0]["text"]) + sum(estimate_tokens(c["parts"][0]["text"]) for c in v["contents"])
            for v in vertex]
    EPOCHS, USD_M = 3, 3.00          # make tune's TUNE_EPOCHS; Google's price to tune gemini-3.1-flash-lite, USD a million training tokens
    print(f"5. the size: about {sum(toks):,} tokens an epoch by the kit's estimate (characters / 4); the longest row about "
          f"{max(toks):,} of the 131,072 Google allows")
    print(f"   {EPOCHS} epochs: about {sum(toks) * EPOCHS:,} training tokens, about Rs {sum(toks) * EPOCHS * USD_M / 1e6 * 85:,.0f} at USD {USD_M:.2f} a million")
    ready = same and shape == twin == len(drafts) == len(vertex) and not dropped and not qa_rows and leaves
    print("verdict: " + ("ready to tune: the manifest's bytes, the trainer's shape, no golden row, nothing where make trainset looks, "
                         f"and {m['tenant']} may leave India" if ready else "do not tune until every line above holds"))
    if ready and hits:
        verb = "carries" if len(hits) == 1 else "carry"
        print(f"         {n_rows(len(hits))} {verb} a finding make trainset never looked for: read the chunks before you pay")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_12', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
