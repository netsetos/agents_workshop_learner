"""Lesson 5.1: demo 01 query vector and identity

Search the verified deployment directly, then compare authorized tenant requests.

Run order inside this file:
1. Do it: embed, search, compare (source window 8)
2. Do it: one identity, two tenants, one outsider (source window 13)

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


def step_01_embed_search_compare(session):
    """Run Do it: embed, search, compare at this checkpoint.

    Run the preflight first. This cell uses its verified settings, checks the endpoint and Acme pin again before paying for an embedding, searches with the same tenant/current restricts, then compares candidate IDs with the API citations. Overlap and first-citation order are observations, not pass/fail assertions. Hybrid retrieval, graph candidates, current-version checks and reranking can change the final selection.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, then one question; a paid embedding of a few hundred characters).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, warnings, subprocess
    from pathlib import Path
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    warnings.filterwarnings("ignore", category=UserWarning)
    from google import genai
    from google.cloud import aiplatform, firestore
    from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
    
    PROJECT, REGION, API = os.environ["PROJECT"], os.environ["REGION"], os.environ["API"]
    settings_file = Path("operator-evidence/lesson51/settings.json")
    if not settings_file.exists():
        raise SystemExit("STOP: run this lesson's preflight first.")
    cfg = json.loads(settings_file.read_text())
    if cfg["project"] != PROJECT or cfg["api"].rstrip("/") != API.rstrip("/"):
        raise SystemExit("STOP: saved settings belong to another project or API; rerun preflight.")
    db = firestore.Client(project=PROJECT)
    pin = (db.collection("tenant_settings").document("acme").get().to_dict() or {}).get("retrieval_backend")
    if pin != "vector":
        raise SystemExit("STOP: Acme is not pinned to vector. Run preflight; restore only after the lesson.")
    aiplatform.init(project=PROJECT, location=REGION)
    ep = aiplatform.MatchingEngineIndexEndpoint(cfg["endpoint"])
    if cfg["deployed_id"] not in [d.id for d in ep.deployed_indexes]:
        raise SystemExit("STOP: deployed ID is absent; use the repair note and rerun preflight.")
    restricts = [Namespace(name="tenant_id", allow_tokens=["acme"])]
    if cfg["current_only"] == "on":
        restricts.append(Namespace(name="current", allow_tokens=["true"]))
    print("Direct dense search:", cfg["deployed_id"], "| current_only:", cfg["current_only"],
          "| requested candidates:", cfg["top_k"], "| API mode:", cfg["mode"], "| graph:", cfg["graph"])
    Q = "What is the notice period for a confirmed E3?"
    client = genai.Client(enterprise=True, project=PROJECT, location="us-central1")
    vec = list(client.models.embed_content(model=cfg["embed_model"], contents=[Q],
        config={"output_dimensionality": 768, "task_type": "RETRIEVAL_QUERY"}).embeddings[0].values)
    result = ep.find_neighbors(deployed_index_id=cfg["deployed_id"], queries=[vec],
                              num_neighbors=cfg["top_k"], filter=restricts)
    hits = result[0] if result else []
    pool = [n.id for n in hits]
    print("Direct dense candidates, first five:")
    for n in hits[:5]:
        row = db.collection("chunks").document(n.id).get().to_dict() or {}
        print(n.id, "|", row.get("locator", "?"), "|", row.get("source_uri", ""),
              "| current:", row.get("current"), "| score:", round(n.distance, 4))
    if not hits:
        raise SystemExit("STOP: the valid deployment returned no matching candidates; check ingestion and restricts.")
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
        f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"],
        check=True, capture_output=True, text=True).stdout.strip()
    if not tok:
        raise SystemExit("STOP: no identity token returned.")
    body = json.dumps({"query": Q, "tenant_id": "acme", "stream": False}).encode()
    request = Request(f"{API}/v1/query", data=body, method="POST",
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=180) as response:
            ans = json.load(response)
    except HTTPError as exc:
        raise SystemExit(f"API HTTP {exc.code}: {exc.read().decode()}")
    cited = [c["chunk_id"] for c in ans.get("citations", [])]
    stages = ans.get("stages") or {}
    print("API answerable:", ans.get("answerable"), "|", ans.get("answer", "")[:100])
    print("Citation overlap:", sum(c in pool for c in cited), "of", len(cited),
          "| first matches direct first:", bool(cited) and cited[0] == pool[0])
    print("stages.retrieval_backend:", stages.get("retrieval_backend"), "| pool:", stages.get("pool"),
          "| vector_chunks:", stages.get("vector_chunks"), "| cache_hit:", ans.get("cache_hit"))
    if stages.get("retrieval_backend") != "vector":
        raise SystemExit("STOP: API used another backend. Allow its one-minute pin cache to expire; rerun preflight if it persists.")
    if (stages.get("vector_chunks") or 0) == 0:
        raise SystemExit("STOP: no Vector Search chunks reached the API pool; inspect vector_search_fallback logs and current rows.")
    print("PASS: the direct search worked and Vector Search contributed to the API pool.")

def step_02_one_identity_two_tenants_one_outsider(session):
    """Run Do it: one identity, two tenants, one outsider at this checkpoint.

    The UI's service account, which your tok() impersonates, sits on all three rosters. The first two calls send it the same question against acme and zeta; the third sends the outsider's token; the fourth sends the UI's token with a header that claims to be someone else. Each line shows the HTTP status. A request turned away for a reason that passes, a model quota hit, a Cloud Run scale-up or a dropped connection, is asked once more after five seconds; anything else prints the reason the service gave instead of a traceback.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, time, subprocess, urllib.request, urllib.error
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = "What is the per-trip cap on travel reimbursement?"
    def tok(sa):                                                     # the setup block's tok() and otok(), one per service account
        return subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                               f"--impersonate-service-account={sa}@{PROJECT}.iam.gserviceaccount.com"],
                              capture_output=True, text=True, check=True).stdout.strip()
    def ask(token, tenant, extra=None):
        """(status, reply): the JSON the API sent, or the start of whatever else came back; one retry on a status that passes."""
        body = json.dumps({"query": Q, "tenant_id": tenant, "stream": False}).encode()
        for attempt in (1, 2):
            req = urllib.request.Request(f"{API}/v1/query", data=body, method="POST",
                                         headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", **(extra or {})})
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    code, raw = r.status, r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                code, raw = e.code, e.read().decode("utf-8", "replace")
            except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
                code, raw = 0, f"{type(e).__name__}: {e}"
            if code in (0, 429, 500, 502, 503, 504) and attempt == 1:
                print(f"   ({tenant}: HTTP {code or 'none'}, {' '.join(raw.split())[:60]!r}; asking once more in five seconds)")
                time.sleep(5)
                continue
            try:
                return code, json.loads(raw)
            except ValueError:
                return code, {"detail": " ".join(raw.split())[:100]}
    ui = tok("documind-ui-sa")
    for t in ("acme", "zeta"):
        st, j = ask(ui, t)
        print(f"{t}: HTTP {st} |", str(j.get("answer") or j.get("detail", ""))[:70], "|", [c["source_uri"].split("/")[-1] for c in j.get("citations", [])[:1]])
    st, j = ask(tok("documind-outsider-sa"), "acme")
    print(f"outsider on acme: HTTP {st} | {j.get('detail', '')}")
    st, j = ask(ui, "zeta", {"x-user-email": "ceo@zeta.example"})
    print(f"ui-sa with a false header on zeta: HTTP {st} |", str(j.get("answer") or j.get("detail", ""))[:50], "| the header changed nothing" if st == 200 else "")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_embed_search_compare),
        ('source_13', step_02_one_identity_two_tenants_one_outsider),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
