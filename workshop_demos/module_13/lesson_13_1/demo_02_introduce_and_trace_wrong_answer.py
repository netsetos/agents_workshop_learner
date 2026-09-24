"""Lesson 13.1: demo 02 introduce and trace wrong answer

Introduce the lesson's version change and follow the resulting answer trace.

Run order inside this file:
1. Do it (source window 13)
2. Do it: the trace (source window 15)
3. Do it: the versions view and the two probes (source window 17)

Prerequisites: demo_01_inspect_debugging_instruments.
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
COMMANDS_01 = """export SINCE131="$(date -u +%FT%TZ)"     # the trace reads the log from here
make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/demo/hr_policy_2026_v2.md NAME=hr_policy_2026.md
ask131 after

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (revision 2 re-issued, then the same question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_the_trace(session):
    """Run Do it: the trace at this checkpoint.

    Do it: the trace

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the trace: reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import hashlib, json, os, subprocess, urllib.request
    from google.cloud import firestore
    P, R, API, SINCE = os.environ["PROJECT"], os.environ["REGION"], os.environ["API"], os.environ["SINCE131"]
    def gcloud(*a):
        return subprocess.run(["gcloud", *a], capture_output=True, text=True, check=True).stdout
    tok = gcloud("auth", "print-identity-token", "--include-email", f"--audiences={API}",
                 f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com").strip()
    def api(path):
        return json.load(urllib.request.urlopen(urllib.request.Request(API + path, headers={"Authorization": "Bearer " + tok}), timeout=60))
    DECIDED = 20      # the pool's depth: config.py's TOP_K_RETRIEVE default, the number evals/ablate.py decided
    RUNG_EVENTS = ("vector_search_fallback", "rag_engine_fallback", "vertex_search_fallback", "retrieval_pin_ignored")
    CAUSE = {"the answer cache": "the answer cache", "the store and its rungs": "a fallback rung", "the pool": "a pool too small",
             "the reranker": "a fallback rung", "the version": "a version", "the model": "the model"}
    
    def read_trail(ans, top_k, events, v):
        """The marks, in the order the answer was made: (link, True clean / False off / None not reached, what it says)."""
        s, hit, none = ans["stages"], ans["cache_hit"] != "none", ans["backend"] == "none"
        pool, backend, fell = s.get("pool", 0), s.get("retrieval_backend"), [e for e in events if e in RUNG_EVENTS]
        marks = [("the answer cache", not hit, "served from the answer cache: an earlier answer, retrieval never ran" if hit
                  else "cache_hit none: retrieval ran")]
        if hit:
            marks += [(link, None, "not reached: retrieval never ran") for link in ("the store and its rungs", "the pool", "the reranker")]
        else:
            own = s.get("vector_chunks", 0) if backend == "vector" else pool
            marks.append(("the store and its rungs", not fell and not s.get("policy_fallback") and own == pool,
                          f"{backend}: {own} of the pool's {pool} from its own index; "
                          + (f"fell back: {', '.join(fell)}" if fell else "no fallback event")
                          + ("; the tenant's data_region sent it to the kit's index" if s.get("policy_fallback") else "")))
            why = (f" (TOP_K_RETRIEVE={top_k} on the revision)" if top_k < DECIDED else
                   " (nothing retrieved: a filter, or no such document)" if not pool else " (retired rows or a filter took the rest)")
            marks.append(("the pool", pool >= DECIDED, f"{pool} of the {DECIDED} the ablation decided" + ("" if pool >= DECIDED else why)))
            marks.append(("the reranker", None if not pool else not s.get("rerank_fallback"),
                          "not reached: nothing to order" if not pool else
                          "the Ranking API did not answer: the pool stood in by retrieval score" if s.get("rerank_fallback")
                          else "the Ranking API ordered the pool"))
        if not v:
            marks.append(("the version", None, "no citation to trace"))
        elif v["cited"] != v["ledger"]:
            marks.append(("the version", False, f"cites {v['cited'][:12]}, a version the ledger has retired; its current is {v['ledger'][:12]}"))
        elif not v["bucket_agrees"]:
            marks.append(("the version", False, "the bucket holds a newer object than the ledger: the last upload never landed"))
        elif v["golden"] and v["ledger"] != v["golden"]:
            marks.append(("the version", False, f"{v['source']}: the ledger's current since {v['since'][:16]} is {v['ledger'][:12]}, "
                          f"not the golden set's {v['golden'][:12]}" + (f"; it declares effective_from {v['effective']}" if v["effective"] else "")))
        else:
            marks.append(("the version", True, f"cites {v['cited'][:12]}, the ledger's current and the golden set's"))
        if none or hit:
            marks.append(("the model", None, "not called: " + ("the empty-pool refusal" if none else "a stored answer")))
        elif not ans["answerable"]:
            marks.append(("the model", False, f"refused with {pool} chunks in the pool: read what was packed, then make judge"))
        else:
            n = len(ans["citations"])
            marks.append(("the model", True, f"answered from {n} citation{'s' if n != 1 else ''}; groundedness is make judge's"))
        return marks
    
    def cause(marks):
        off = [(n, link) for n, (link, ok, _) in enumerate(marks, 1) if ok is False]
        if not off:
            return "CAUSE: no link is off - the answer is what the lane holds; if it is still wrong, the golden set or the question is"
        n, link = off[0]
        return f"CAUSE: {CAUSE[link]} (link {n}) - every link before it is clean"
    ans = json.load(open(os.path.expanduser("~/ask131-after.json")))           # the answer that was reported
    ver = api("/version")
    print(f"serving: {ver['git_sha']}, {ver['generator_model']} via {ver['model_backend']}, prompt {ver['prompt']}, "
          f"{ver['embedding']}, current-only {ver['retrieval_current_only']}, answer cache {ver['semantic_cache']}")
    svc = json.loads(gcloud("run", "services", "describe", "documind-api", "--region", R, "--project", P, "--format", "json"))
    env = {e["name"]: e.get("value") for e in svc["spec"]["template"]["spec"]["containers"][0].get("env", [])}
    top_k = int(env.get("TOP_K_RETRIEVE") or 20)                                # config.py's default when the revision sets none
    ors = " OR ".join('jsonPayload.event="%s"' % e for e in RUNG_EVENTS + ("rerank_fallback", "cache_stale"))
    flt = (f'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" '
           f'AND timestamp>="{SINCE}" AND ({ors})')
    events = [e["jsonPayload"]["event"] for e in json.loads(gcloud("logging", "read", flt, "--project", P, "--format", "json") or "[]")]
    print(f"events since the break: {', '.join(events) or 'none'}")
    v = None
    if ans["citations"]:
        c = ans["citations"][0]
        name = c["source_uri"].split("/", 3)[3]                                   # acme/hr_policy_2026.md
        row = firestore.Client(project=P).collection("chunks").document(c["chunk_id"]).get().to_dict() or {}
        led = next(s for s in api("/v1/sources?tenant_id=" + name.split("/")[0])["sources"] if s["name"] == name)
        gen = gcloud("storage", "objects", "describe", c["source_uri"], "--format=value(generation)").strip()
        frozen = "evals/corpus/" + name                                           # the bytes the golden set was written against
        v = {"source": name, "cited": c["chunk_id"].split(":", 1)[1].split("#")[0], "ledger": led["doc_key"].split("_", 1)[1],
             "golden": hashlib.sha256(open(frozen, "rb").read()).hexdigest() if os.path.exists(frozen) else None,
             "since": led["indexed_at"] or "", "effective": row.get("effective_from"), "bucket_agrees": gen == led["generation"]}
    print("the trail of ~/ask131-after.json, in the order the answer was made:")
    marks = read_trail(ans, top_k, events, v)
    for n, (link, ok, said) in enumerate(marks, 1):
        print(f"  {n} {link:24} {'clean' if ok else '-' if ok is None else 'OFF':5}  {said}")
    print(cause(marks))

# Original CLI workflow for step_03_the_versions_view_and_the_two_probes.
COMMANDS_03 = """make sources PROJECT="$PROJECT" TENANT_ONLY=acme | grep -E "^source|hr_policy_2026"
python commands/verify-vector-index.py --deploy-root "$DEMO_ROOT" --project "$PROJECT" --region "$REGION"
GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py

"""

def step_03_the_versions_view_and_the_two_probes(session):
    """Run Do it: the versions view and the two probes at this checkpoint.

    Do it: the versions view and the two probes

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_example),
        ('source_15', step_02_the_trace),
        ('source_17', step_03_the_versions_view_and_the_two_probes),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
