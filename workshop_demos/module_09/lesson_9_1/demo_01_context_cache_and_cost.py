"""Lesson 9.1: demo 01 context cache and cost

Ask uncached, create a context cache, repeat the ask and inspect the bill.

Run order inside this file:
1. Do it: the question, uncached (source window 10)
2. Do it: the cache (source window 12)
3. Do it: the same question, with the cache (source window 14)
4. Do it (source window 17)

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


# Original CLI workflow for step_01_the_question_uncached.
COMMANDS_01 = """ask91() {   # one /v1/query to $1 about acme, as documind-ui-sa; prints the answer's cache fields
TOKEN="$(tok "$API")" URL="$1" Q="$2" python - <<'PY'
import json, os, urllib.error, urllib.request
body = json.dumps({"query": os.environ["Q"], "tenant_id": "acme", "top_k": 6}).encode()
req = urllib.request.Request(os.environ["URL"] + "/v1/query", data=body, method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["TOKEN"]})
try:
    a = json.load(urllib.request.urlopen(req, timeout=120))
    print(f"  backend {a['backend']:6} cache_hit {a['cache_hit']:8} tokens_in {a['tokens_in']:>6}  cached_tokens {a['cached_tokens']:>6}  {a['latency_ms']:>5} ms  | {a['answer'][:44]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}  {e.read().decode(errors='replace')[:90]}")
PY
}
export SINCE91="$(date -u +%FT%TZ)" Q91="How many days a month can I work remotely?"
ask91 "$API" "$Q91"

"""

def step_01_the_question_uncached(session):
    """Run Do it: the question, uncached at this checkpoint.

    Do it: the question, uncached

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a small ask function, a start time for the rows, and one question to the live API).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_cache.
COMMANDS_02 = """make cache PROJECT="$PROJECT" TENANT=acme

"""

def step_02_the_cache(session):
    """Run Do it: the cache at this checkpoint.

    Do it: the cache

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acme's context cache: its pack, on Gemini, for an hour).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_the_same_question_with_the_cache.
COMMANDS_03 = """ask91 "$API" "$Q91"

"""

def step_03_the_same_question_with_the_cache(session):
    """Run Do it: the same question, with the cache at this checkpoint.

    Do it: the same question, with the cache

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same question again, to the live API).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def step_04_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every acme usage row since the first ask; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
         f'AND jsonPayload.tenant="acme" AND timestamp>="{os.environ["SINCE91"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    for e in json.loads(out or "[]"):
        j, rev = e["jsonPayload"], e["resource"]["labels"]["revision_name"]
        print(f"  {rev[-9:]}  {j['model_backend']:6}  in {j['tokens_in']:>6}  cached {j['cached_tokens']:>6}  Rs {j['cost_usd'] * 85:.4f}  {j['latency_ms']:>5} ms")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_the_question_uncached),
        ('source_12', step_02_the_cache),
        ('source_14', step_03_the_same_question_with_the_cache),
        ('source_17', step_04_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
