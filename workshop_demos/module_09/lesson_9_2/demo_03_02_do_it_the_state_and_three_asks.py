"""Lesson 9.2 / s3: Both caches, and the corpus they follow

Summary and purpose:
Do it: the state, and three asks

HTML instruction: bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_two_caches
Expected observation: ledger 1ef46119bd89b143 (17 versions, last ingest_ok) | context cache packed from 1ef46119bd89b143: current
  vertex none     in  43109 cached  41259  2480 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2530 ms | A confirmed employee at grade E3 or above serves a
  cache  semantic in      0 cached      0   170 ms | A confirmed employee at grade E3 or above serves a

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L445

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask92() {   # one /v1/query about acme to $1, as documind-ui-sa; $2 = top_k (6), $3 = filters as JSON (none)
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


def demonstrate(session):
    """Run Do it: the state, and three asks at this checkpoint.

    Do it: the state, and three asks

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
