"""Lesson 9.2: demo 01 cache state and scope

Inspect both caches and vary request scope while keeping question words fixed.

Run order inside this file:
1. Do it: the two caches (source window 8)
2. Do it: the state, and three asks (source window 10)
3. Do it (source window 13)

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


# Original CLI workflow for step_01_the_two_caches.
COMMANDS_01 = """make cache PROJECT="$PROJECT" TENANT=acme
make candidate PROJECT="$PROJECT" SEMANTIC_CACHE=on
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"

"""

def step_01_the_two_caches(session):
    """Run Do it: the two caches at this checkpoint.

    Do it: the two caches

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_state_and_three_asks.
COMMANDS_02 = """ask92() {   # one /v1/query about acme to $1, as documind-ui-sa; $2 = top_k (6), $3 = filters as JSON (none)
TOKEN="$(tok "$API")" URL="$1" K="${2:-6}" F="${3:-null}" Q="$Q92" python - <<'PY'
import json, os, urllib.error, urllib.request
body = json.dumps({"query": os.environ["Q"], "tenant_id": "acme", "top_k": int(os.environ["K"]), "filters": json.loads(os.environ["F"])}).encode()
req = urllib.request.Request(os.environ["URL"] + "/v1/query", data=body, method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["TOKEN"]})
try:
    a = json.load(urllib.request.urlopen(req, timeout=120))
    print(f"  {a['backend']:6} {a['cache_hit']:8} in {a['tokens_in']:>6} cached {a['cached_tokens']:>6} {a['latency_ms']:>5} ms | {a['answer'][:50]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}  {e.read().decode(errors='replace')[:90]}")
PY
}
state92() {   # the ledger's fingerprint beside the one the context cache was packed from
python - <<'PY'
import os
from google.cloud import firestore
db = firestore.Client(project=os.environ["PROJECT"])
l, c = (db.document(p).get().to_dict() or {} for p in ("ledger/acme", "tenant_caches/acme"))
state = "none" if not c else "current" if c.get("corpus_fingerprint") == l.get("fingerprint") else "STALE"
print(f"  ledger {l.get('fingerprint')} ({l.get('versions')} versions, last {l.get('last_event')}) | context cache packed from {c.get('corpus_fingerprint')}: {state}")
PY
}
export SINCE92="$(date -u +%FT%TZ)" Q92="What is the notice period for a confirmed E3?"
state92
ask92 "$API"            # the live revision: the context cache, no answer cache
ask92 "$CAND"           # the candidate: a miss, stored
ask92 "$CAND"           # the same words: the exact rung

"""

def step_02_the_state_and_three_asks(session):
    """Run Do it: the state, and three asks at this checkpoint.

    Do it: the state, and three asks

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_example.
COMMANDS_03 = """ask92 "$CAND" 8                     # top_k 8: another scope
ask92 "$CAND" 6 '{"kind": "text"}'   # a filter: another scope
python - <<'PY'
import sys
sys.path.insert(0, "services/rag-api")
from semantic_cache import scope_of
for label, f, k, p in [("as asked", None, 6, "v3"), ("top_k 8", None, 8, "v3"), ("kind: text", {"kind": "text"}, 6, "v3"), ("prompt v4", None, 6, "v4")]:
    print(f"  scope {label:10} {scope_of(f, k, p)}")
PY

"""

def step_03_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_the_two_caches),
        ('source_10', step_02_the_state_and_three_asks),
        ('source_13', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
