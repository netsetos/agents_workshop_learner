"""Lesson 17.3: demo 01 clean baseline and candidate

Read baseline requirements, create the tuned candidate and audit the comparison.

Run order inside this file:
1. Do it (source window 9)
2. Do it: the candidate (source window 12)
3. Do it: the audit (source window 14)

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


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's own functions; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, datetime as dt, os, sys
    sys.path[:0] = ["evals"]
    from usage_rows import group, show
    EP = "projects/NUMBER/locations/us/endpoints/ENDPOINT_ID"
    # 1. the answer cache's test, lifted out of semantic_cache.py (which builds a Firestore client when imported)
    tree = ast.parse(open("services/rag-api/semantic_cache.py", encoding="utf-8").read())
    ns = {"datetime": dt.datetime}
    exec(compile(ast.Module([n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_alive"], []), "semantic_cache.py", "exec"), ns)
    now = dt.datetime.now(dt.timezone.utc)
    entry = {"model": "gemini-3.6-flash", "fingerprint": "f1", "scope": "s1", "expire_at": now + dt.timedelta(hours=20)}
    print(f"an answer gemini-3.6-flash cached, looked up for the tuned endpoint: alive {ns['_alive'](entry, 'f1', 's1', now)}")
    # 2. one answer on the tuned endpoint, priced by cost.py (lifted: it imports BigQuery when loaded) and by Google
    tree = ast.parse(open("services/rag-api/cost.py", encoding="utf-8").read())
    cns = {"os": os, "USD_INR": 85.0}
    cns["FALLBACK"] = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "FALLBACK")
    cns["_prices"] = lambda: cns["FALLBACK"]
    exec(compile(ast.Module([n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "price"], []), "cost.py", "exec"), cns)
    TIN, TOUT = 7400, 150
    for base in ("gemini-3.1-flash-lite", "gemini-3.6-flash"):
        os.environ["RAG_MODEL_BASE"] = base
        print(f"cost.py with RAG_MODEL_BASE={base:22} Rs {cns['price'](EP, TIN, TOUT)['inr']:.4f} an answer of {TIN:,} tokens in, {TOUT} out")
    usd_in, usd_out = cns["FALLBACK"]["gemini-3.1-flash-lite"]
    print(f"Google, a tuned endpoint at 1.5 x its base          Rs {1.5 * (TIN * usd_in + TOUT * usd_out) / 1e6 * 85:.4f}")
    # 3. what make usage prints for it
    rows = [{"model": "gemini-3.6-flash", "tokens_in": TIN, "tokens_out": 210, "cost_usd": 0.01268, "latency_ms": 2100},
            {"model": EP, "tokens_in": TIN, "tokens_out": TOUT, "cost_usd": 0.002075, "latency_ms": 1000}]
    show("make usage's model column", group(rows, ("model",)), ("model",))

# Original CLI workflow for step_02_the_candidate.
COMMANDS_02 = """export ENDPOINT="${ENDPOINT:-$(grep -o 'projects/[^ ]*/endpoints/[0-9]*' ~/poll172.log | head -1)}"     # lesson 17.2's endpoint
make candidate PROJECT="$PROJECT" GENERATOR_MODEL="$ENDPOINT" RAG_MODEL_BASE=gemini-3.1-flash-lite
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"

"""

def step_02_the_candidate(session):
    """Run Do it: the candidate at this checkpoint.

    Do it: the candidate

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a revision with no traffic; nothing is billed until it answers).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_the_audit(session):
    """Run Do it: the audit at this checkpoint.

    The cell makes the four checks from step 1:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads both revisions, ~/tune172.log, the bucket and Firestore).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, re, subprocess, sys
    sys.path[:0] = [".", "evals"]
    P, R = os.environ["PROJECT"], os.environ["REGION"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", P)
    
    
    def gcloud(*a):
        cmd = ["gcloud", *a, "--region", R, "--project", P, "--format=json"]
        return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    
    
    traffic = gcloud("run", "services", "describe", "documind-api")["status"]["traffic"]
    live = max((t for t in traffic if t.get("percent")), key=lambda t: t["percent"])["revisionName"]
    cand = next(t["revisionName"] for t in traffic if t.get("tag") == "candidate")
    env = lambda rev: {e["name"]: e.get("value", "") for e in gcloud("run", "revisions", "describe", rev)["spec"]["containers"][0].get("env", [])}
    a, b = env(live), env(cand)
    diff = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
    print(f"1. one change: {len(diff)} settings differ between {live} (live) and {cand}")
    for k in diff:
        print(f"   {k:16} {a.get(k, '(unset)')} -> {b.get(k, '(unset)')}")
    one = set(diff) == {"GENERATOR_MODEL", "RAG_MODEL_BASE"} and b["RAG_MODEL_BASE"] == "gemini-3.1-flash-lite"
    print("   " + ("the model and the base it is priced at, and nothing else" if one else "more than the model differs: run make candidate again with the live values"))
    cache = (a.get("SEMANTIC_CACHE", "off"), b.get("SEMANTIC_CACHE", "off"))
    print(f"2. the answer cache: {cache[0]} on the live revision, {cache[1]} on the candidate"
          + ("" if cache == ("off", "off") else " - its lookup never reads the model: turn it off on both first"))
    from google.cloud import firestore, storage
    import make_trainset as mt
    uri = re.search(r", dataset (gs://\S+\.vertex\.jsonl)", open(os.path.expanduser("~/tune172.log"), encoding="utf-8").read()).group(1)
    bucket_name, name = uri[len("gs://"):].split("/", 1)                       # what lesson 17.2 tuned on
    bucket = storage.Client(project=P).bucket(bucket_name)
    m = json.loads(bucket.blob(name.replace(".vertex.jsonl", ".manifest.json")).download_as_text())
    chunks = {c["text"].strip(): c for c in mt.load_chunks(m["tenant"])}
    rows = []
    for line in bucket.blob(name).download_as_text().splitlines():
        user = json.loads(line)["contents"][0]["parts"][0]["text"]
        c = chunks[user.split("[Source 1] ", 1)[1].rsplit("\n\nQuestion: ", 1)[0].strip()]
        rows.append({"chunk_id": c["chunk_id"], "source_uri": c["source_uri"], "text": c["text"], "question": user.rsplit("\n\nQuestion: ", 1)[1]})
    golden = [json.loads(l) for l in open("evals/golden.jsonl", encoding="utf-8") if l.strip()]
    left = mt.exclude_golden(rows, golden)[1]
    print(f"3. the test set: the endpoint was tuned on {name.rsplit('/', 1)[-1]}, {len(rows)} rows; building it dropped "
          f"{m['dropped_golden_overlap']} for the golden set, and today's golden set would drop {len(left)} more")
    rec = firestore.Client(project=P).collection("tenant_caches").document(m["tenant"]).get()
    print("4. the context cache: " + (f"{m['tenant']} has one, made for {rec.to_dict().get('model')}: the live revision reads it and the "
                                       f"candidate cannot - delete it for the hour (make cache TENANT={m['tenant']} CACHE_OP=delete)" if rec.exists
                                       else f"none for {m['tenant']}, so both revisions pay full price for their input"))
    clean = one and cache == ("off", "off") and not left and not rec.exists
    print("verdict: " + ("uncontaminated - one change, no answer cache, a training file the test set never entered, the same input price"
                         if clean else "not yet: fix the lines above, then run this cell again"))

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_12', step_02_the_candidate),
        ('source_14', step_03_the_audit),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
