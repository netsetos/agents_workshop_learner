"""Lesson 10.1: demo 02 retrieval and direct brain

Call the shared retrieval tool and trace the direct brain's single retrieval.

Run order inside this file:
1. Do it (source window 15)
2. Do it (source window 19)

Prerequisites: demo_01_deploy_and_read_tool_contracts.
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
COMMANDS_01 = """export SINCE101="$(date -u +%FT%TZ)"
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" RAG_API_URL="$API" python - <<'PY'
import time
from shared.documind_tools import retrieve
t = time.time()
r = retrieve("After how many years of continuous service does gratuity become payable?", tenant_id="acme", top_k=5)
print(f"  {len(r['citations'])} citations | answerable {r['answerable']} | confidence {r['confidence']} | {time.time() - t:.1f} s")
if r["citations"]:
    print("  first:", {k: r["citations"][0].get(k) for k in ("chunk_id", "page", "score")})
print("  rag-api's own answer:", (r.get("answer") or r.get("error") or "")[:90])
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the one retrieve(), called from your shell as a roster member).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """chat10() {   # one /v1/chat turn as documind-ui-sa: $1 = the brain, $2 = the question
TOKEN="$(tok "$CHAT")" B="$1" Q="$2" python - <<'PY'
import json, os, urllib.error, urllib.request
def text(answer):   # a chat service built before 24 September 2026 can send Gemini's content blocks instead of a string
    return answer if isinstance(answer, str) else "".join(p if isinstance(p, str) else p.get("text", "") for p in answer
                                                          if isinstance(p, str) or p.get("type") == "text")
body = json.dumps({"question": os.environ["Q"], "session_id": "lesson101-" + os.environ["B"], "brain": os.environ["B"]}).encode()
req = urllib.request.Request(os.environ["CHAT"] + "/v1/chat", data=body, method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["TOKEN"]})
try:
    a = json.load(urllib.request.urlopen(req, timeout=300))
    print(f"  {a['brain']:9} tool_calls {a['tool_calls']}  refusals {a['refusals']}  citations {len(a.get('citations', []))}  {a['latency_ms']} ms")
    print(f"      {text(a['answer'])[:96]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}  {e.read().decode(errors='replace')[:100]}")
PY
}
chat10 direct "After how many years of continuous service does gratuity become payable?"

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a small chat function, and the direct brain).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_15', step_01_example),
        ('source_19', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
