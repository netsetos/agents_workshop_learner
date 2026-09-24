"""Lesson 8.2: demo 01 refusal ladder and isolation

Compare admission/authentication/authorization refusals and cross-tenant golden rows.

Run order inside this file:
1. Do it (source window 8)
2. Do it (source window 12)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" BARE="$(gcloud auth print-identity-token --audiences="$API" --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com")" \\
  python - <<'PY'
import json, os, urllib.error, urllib.request
body = json.dumps({"query": "What is the notice period for a confirmed E3?", "tenant_id": "acme", "top_k": 6}).encode()
for label, token in [("no token", None), ("a token without its email", os.environ["BARE"]),
                     ("the outsider's token", os.environ["OUTSIDER"]), ("documind-ui-sa's token", os.environ["TOKEN"])]:
    req = urllib.request.Request(os.environ["API"] + "/v1/query", data=body, method="POST", headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            status, text = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, text = e.code, e.read().decode(errors="replace")
    shown = text[:66] if text.startswith("{") else "(Cloud Run's own page: the request never reached the API)"
    print(f"  {label:26} {status}  {shown}")
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four requests to /v1/query; one is answered).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask, check_isolation, contains, load_golden
api, token = os.environ["API"], os.environ["TOKEN"]
iso = [r for r in load_golden() if r["shape"] == "isolation"]
rate, bad = check_isolation(api, iso, token, os.environ["OUTSIDER"])
print(f"the outsider, on {len(iso)} isolation rows: 403 on {rate:.0%}", *bad, sep="\\n  ")
for r in iso:
    status, body, _ = ask(api, r["question"], r["tenant"], "eval@documind.in", token)
    leaked = [w for w in r["must_not_contain"] if contains(body.get("answer", ""), w)]
    print(f"  {r['id']:6} as {r['tenant']:6} HTTP {status}  answerable {str(body.get('answerable')):5}  "
          + (f"LEAKED {', '.join(leaked)}" if leaked else f"no {r['must_not_contain'][0]!r}"))
PY

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (11 outsider requests, then 11 member questions).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_example),
        ('source_12', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
