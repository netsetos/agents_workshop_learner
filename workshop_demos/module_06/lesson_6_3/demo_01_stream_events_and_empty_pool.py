"""Lesson 6.3: demo 01 stream events and empty pool

Time the event sequence and inspect citations plus the one-token empty-pool stream.

Run order inside this file:
1. Do it: one stream, timed, then the query's citations beside it (source window 12)
2. Do it: the empty pool as one token, then the stream rows (source window 16)

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


def step_01_one_stream_timed_then_the_query_s_citation(session):
    """Run Do it: one stream, timed, then the query's citations beside it at this checkpoint.

    Do it: one stream, timed, then the query's citations beside it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; one stream and one query, two rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, time, subprocess, urllib.request
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = os.environ.get("Q", "What is the notice period for a confirmed E3?")
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"], capture_output=True, text=True, check=True).stdout.strip()
    H = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    req = urllib.request.Request(f"{API}/v1/stream", method="POST", headers=H, data=json.dumps({"query": Q, "tenant_id": "acme", "top_k": 5}).encode())
    t0 = time.perf_counter(); ev = None; first = {}; cits, tokens, done, raw = [], [], {}, []
    with urllib.request.urlopen(req, timeout=180) as r:
        for line in r:
            line = line.decode("utf-8").rstrip("\n"); raw.append(line)
            if line.startswith("event: "):
                ev = line[7:]; first.setdefault(ev, round((time.perf_counter() - t0) * 1000))
            elif line.startswith("data: "):
                d = json.loads(line[6:])
                if ev == "citation": cits.append(d)
                elif ev == "token": tokens.append(d["t"])
                elif ev == "done": done = d
    open("/tmp/stream63.txt", "w", encoding="utf-8").write("\n".join(raw) + "\n")
    print(f"first citation at {first.get('citation')} ms | first token at {first.get('token')} ms | done at {first.get('done')} ms | the API's own latency_ms {done.get('latency_ms')}")
    print(f"{len(cits)} citation events, then {len(tokens)} token events, then done")
    for c in cits:
        print(f"   citation {c['n']} #{str(c['chunk_id']).rsplit('#', 1)[-1]:>3} {c['source'].split('/')[-1][:22]:22} kind {c['kind']} effective_from {c.get('effective_from')} quote {c['quote'][:34]!r}")
    print("the answer:", " ".join("".join(tokens).split())[:120], "...")
    print("done:", {k: done.get(k) for k in ("tokens_in", "tokens_out", "cached_tokens", "model", "backend", "cache_hit", "prompt")})
    print("stages:", done.get("stages"))
    req = urllib.request.Request(f"{API}/v1/query", method="POST", headers=H, data=json.dumps({"query": Q, "tenant_id": "acme", "stream": False, "top_k": 5}).encode())
    j = json.load(urllib.request.urlopen(req, timeout=180))
    print(f"the query's answer to the same question: {len(j['citations'])} citations, the ones the model used; the stream's {len(cits)} were the packed set")
    print("saved /tmp/stream63.txt: paste it into the reader in step 1")

# Original CLI workflow for step_02_the_empty_pool_as_one_token_then_the_strea.
COMMANDS_02 = """curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","filters":{"doc_type":"policy"}}' \\
  | python -c "
import sys, json
ev, n = None, {}
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: '): ev = line[7:]; n[ev] = n.get(ev, 0) + 1
    elif line.startswith('data: ') and ev == 'token': print('the one token:', json.loads(line[6:])['t'][:88], '...')
    elif line.startswith('data: ') and ev == 'done': d = json.loads(line[6:]); print('done: backend', d['backend'], '| tokens_in', d['tokens_in'], '| pool', d['stages']['pool'], '| rerank_ms', d['stages']['rerank_ms'], '| generate_ms', d['stages']['generate_ms'])
print('events:', n)"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="stream"' \\
  --project "$PROJECT" --freshness 15m --limit 3 --format='value(jsonPayload.answerable,jsonPayload.model_backend,jsonPayload.tokens_in,jsonPayload.tokens_out,jsonPayload.pool,jsonPayload.guard,jsonPayload.brain)'

"""

def step_02_the_empty_pool_as_one_token_then_the_strea(session):
    """Run Do it: the empty pool as one token, then the stream rows at this checkpoint.

    Do it: the empty pool as one token, then the stream rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one stream that costs nothing; one log read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_12', step_01_one_stream_timed_then_the_query_s_citation),
        ('source_16', step_02_the_empty_pool_as_one_token_then_the_strea),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
