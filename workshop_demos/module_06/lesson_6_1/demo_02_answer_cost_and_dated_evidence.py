"""Lesson 6.1: demo 02 answer cost and dated evidence

Inspect an answer's tokens/price and follow a dated document through a stream.

Run order inside this file:
1. Do it: one question, its tokens, its price, and the estimate beside it (source window 21)
2. Do it: the dated revision in, the stream read, revision 1 back (source window 27)

Prerequisites: demo_01_packing_and_token_counts.
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


def step_01_one_question_its_tokens_its_price_and_the(session):
    """Run Do it: one question, its tokens, its price, and the estimate beside it at this checkpoint.

    Do it: one question, its tokens, its price, and the estimate beside it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question, a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, json, subprocess, urllib.request
    sys.path[:0] = [".", "services/rag-api"]
    from context_budget import estimate_tokens, pack_chunks
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = "What is the notice period for a confirmed E3?"
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"], capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(f"{API}/v1/query", method="POST", data=json.dumps({"query": Q, "tenant_id": "acme", "stream": False, "top_k": 5}).encode(),
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=180))
    print(f"the answer: tokens_in {j['tokens_in']} | cached_tokens {j.get('cached_tokens', 0)} | tokens_out {j['tokens_out']} | cost_usd {j['cost_usd']} | citations {len(j['citations'])} | model {j['model']}")
    try:
        from cost import price                                                     # the API's own arithmetic; offline the price table falls back to the file's rates
        p = price(j["model"], j["tokens_in"], j["tokens_out"], j.get("cached_tokens", 0))
        print(f"cost.price(): ${p['usd']} = Rs {p['inr']} at {p['usd_inr_rate']} | in {p['tokens_in']} out {p['tokens_out']} cached {p['cached_tokens']}")
    except ImportError as e:
        print("cost.price() needs google-cloud-bigquery in the venv:", e)
    try:
        d = json.load(open("/tmp/pool53.json"))                                   # lesson 5.3's ranked pool for this question
        ranked = [dict(d["pool"][i], source_uri="gs://uploads/acme/" + d["pool"][i]["source"]) for i, _ in d["ranked"]][:5]
        context, packed, dropped = pack_chunks(ranked, 7832, estimate_tokens)
        est = 168 + estimate_tokens(context)
        print(f"the estimate for the same packed set: fixed 168 + context {estimate_tokens(context)} = {est} | the model counted {j['tokens_in']} | ratio {j['tokens_in'] / est:.2f}")
    except FileNotFoundError:
        print("no /tmp/pool53.json here: run lesson 5.3's step 4 first to put the estimate beside tokens_in")

# Original CLI workflow for step_02_the_dated_revision_in_the_stream_read_revi.
COMMANDS_02 = """worker_line() { for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND (jsonPayload.event=\\"ingest_ok\\" OR jsonPayload.event=\\"ingest_reactivated\\") AND (jsonPayload.tenant=\\"acme\\" OR jsonPayload.doc_key:\\"acme_\\") AND timestamp>=\\"$1\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.event,jsonPayload.chunks,jsonPayload.embedded,jsonPayload.effective_from)')"
  [ -n "$LINE" ] && { echo ">> event chunks embedded effective_from: $LINE"; return; }; done; echo ">> no worker line in five minutes"; }
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; gcloud storage cp evals/demo/smoke_note_v2.md "gs://$PROJECT-uploads/acme/smoke_note.md"; worker_line "$SINCE"
curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"Where is the smoke lantern kept, and from when?","tenant_id":"acme"}' \\
  | python -c "
import sys, json
ev, text = None, []
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: '): ev = line[7:]
    elif line.startswith('data: ') and ev == 'citation':
        d = json.loads(line[6:]); print('citation', d['n'], d['source'].split('/')[-1], '| effective_from', d.get('effective_from'), '| quote', repr(d['quote'][:50]))
    elif line.startswith('data: ') and ev == 'token': text.append(json.loads(line[6:])['t'])
    elif line.startswith('data: ') and ev == 'done':
        d = json.loads(line[6:]); print('done: tokens_in', d.get('tokens_in'), '| tokens_out', d.get('tokens_out'), '| latency_ms', d.get('latency_ms'), '| the price is on the row, not in the event')
print('answer:', ''.join(text)[:160])"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; gcloud storage cp evals/demo/smoke_note_v1.md "gs://$PROJECT-uploads/acme/smoke_note.md"; worker_line "$SINCE"

"""

def step_02_the_dated_revision_in_the_stream_read_revi(session):
    """Run Do it: the dated revision in, the stream read, revision 1 back at this checkpoint.

    Do it: the dated revision in, the stream read, revision 1 back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one upload, one streamed question, one upload; paise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_one_question_its_tokens_its_price_and_the),
        ('source_27', step_02_the_dated_revision_in_the_stream_read_revi),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
