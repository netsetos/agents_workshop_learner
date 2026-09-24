"""Lesson 17.3 / s4: The candidate, audited

Summary and purpose:
The cell makes the four checks from step 1:

HTML instruction: bash — run in the operator shell, in the kit (reads both revisions, ~/tune172.log, the bucket and Firestore)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_candidate
Expected observation: 1. one change: 2 settings differ between documind-api-000NN-xxx (live) and documind-api-000NN-yyy
   GENERATOR_MODEL  gemini-3.6-flash -> projects/NUMBER/locations/us/endpoints/9136961803583303949
   RAG_MODEL_BASE   gemini-3.6-flash -> gemini-3.1-flash-lite
   the model and the base it is priced at, and nothing else
2. the answer cache: off on the live revision, off on the candidate
3. the test set: the endpoint was tuned on documind_sft_v2.vertex.jsonl, 315 rows; building it dropped 15 for the golden set, and today's golden set would drop 0 more
4. the context cache: none for acme, so both revisions pay full price for their input
verdict: uncontaminated - one change, no answer cache, a training file the test set never entered, the same input price

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L522

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
