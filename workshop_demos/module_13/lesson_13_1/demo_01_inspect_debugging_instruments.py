"""Lesson 13.1: demo 01 inspect debugging instruments

Read the available trace instruments and establish the question's baseline.

Run order inside this file:
1. Do it (source window 9)
2. Do it (source window 11)

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
    Operations: bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, re
    root = "services/rag-api/"
    main, ret = (open(root + f, encoding="utf-8").read() for f in ("main.py", "retriever.py"))
    tree = ast.parse(open(root + "schemas.py", encoding="utf-8").read())
    env = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "RAGResponse")
    print("the envelope on every answer, beyond the contract (schemas.py, RAGResponse):")
    print("  " + ", ".join(n.target.id for n in env.body if isinstance(n, ast.AnnAssign)))
    q = main[main.index("def query("):main.index("def _record(")]
    keys = set(re.findall(r'stages\["(\w+)"\]', q)) | {n + "_ms" for n in re.findall(r'stage\(stages, "(\w+)"\)', q)}
    print("stages, as query() fills them (main.py):")
    print("  " + ", ".join(sorted(keys)))
    print("found_by, the rung that put a chunk in the pool (retriever.py):")
    print("  " + ", ".join(sorted(set(re.findall(r'found_by"\]? ?[:=] ?"(\w+)"', ret)))))
    v = main[main.index("def version():"):main.index('@app.get("/v1/sources")')]
    print("GET /version, what is serving (main.py):")
    print("  " + ", ".join(re.findall(r'"(\w+)":', v)))
    print("the events a degraded answer leaves in documind-api's log:")
    for f in ("main.py", "retriever.py", "generator.py", "cache_manager.py"):
        for i, line in enumerate(open(root + f, encoding="utf-8"), 1):
            for ev in re.findall(r'"event": "(\w+(?:fallback|stale|ignored|exhausted|truncated))"', line):
                print(f"  {ev:24} {f}:{i}")

# Original CLI workflow for step_02_example.
COMMANDS_02 = """ask131() {   # ask131 LABEL: acme's E3 notice-period question as documind-ui-sa - the answer and its trail, kept in ~/ask131-LABEL.json
LABEL="$1" python - <<'PY'
import json, os, subprocess, urllib.request
label, P, API = os.environ["LABEL"], os.environ["PROJECT"], os.environ["API"]
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
body = json.dumps({"query": "What is the notice period for a confirmed E3?", "tenant_id": "acme"}).encode()
req = urllib.request.Request(API + "/v1/query", data=body, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
ans = json.load(urllib.request.urlopen(req, timeout=120))
json.dump(ans, open(os.path.expanduser(f"~/ask131-{label}.json"), "w"), indent=1)
s = ans["stages"]
print(ans["answer"])
for n, c in enumerate(ans["citations"], 1):
    version, chunk = c["chunk_id"].split(":", 1)[1].split("#")
    print(f"  [{n}] {c['source_uri'].rsplit('/', 1)[-1]}  version {version[:12]}  chunk {chunk}  {c['quote']!r}")
print(f"  cache_hit {ans['cache_hit']} | backend {ans['backend']} | answerable {ans['answerable']}")
print(f"  store {s.get('retrieval_backend')} | vector_chunks {s.get('vector_chunks')} | pool {s.get('pool')} | "
      f"rerank_fallback {s.get('rerank_fallback', 0)} | policy_fallback {s.get('policy_fallback')}")
print(f"  kept in ~/ask131-{label}.json")
PY
}
ask131 before

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the question, the answer and its trail).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_11', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
