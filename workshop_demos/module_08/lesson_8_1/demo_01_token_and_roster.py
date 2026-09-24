"""Lesson 8.1: demo 01 token and roster

Inspect audiences, token claims and both membership lookup directions.

Run order inside this file:
1. Do it: the API's audiences, and who may invoke it (source window 10)
2. Do it: what your token says about itself (source window 12)
3. Do it: the three rosters, as Firestore holds them (source window 17)
4. Do it: the plan make roster would write for you (source window 19)

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


def step_01_the_api_s_audiences_and_who_may_invoke_it(session):
    """Run Do it: the API's audiences, and who may invoke it at this checkpoint.

    Do it: the API's audiences, and who may invoke it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gcloud(*a):
        cmd = ["gcloud", *a, "--region", os.environ["REGION"], "--project", os.environ["PROJECT"], "--format=json"]
        return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    env = {e["name"]: e.get("value", "") for e in gcloud("run", "services", "describe", "documind-api")["spec"]["template"]["spec"]["containers"][0].get("env", [])}
    for k in ("IAP_AUDIENCE", "SELF_URL"):
        print(f"{k:13}", "\n              ".join(env.get(k, "(unset)").split(",")))
    for b in gcloud("run", "services", "get-iam-policy", "documind-api").get("bindings", []):
        if b["role"] == "roles/run.invoker":
            print("run.invoker  ", "\n              ".join(sorted(b["members"])))

# Original CLI workflow for step_02_what_your_token_says_about_itself.
COMMANDS_02 = """TOKEN="$(tok "$API")" BARE="$(gcloud auth print-identity-token --audiences="$API" \\
  --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com")" python - <<'PY'
import base64, json, os, time
for name in ("TOKEN", "BARE"):
    part = os.environ[name].split(".")[1]
    c = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))      # read, not verified: the API verifies
    print(f"{name}: aud {c.get('aud')}")
    print(f"       email {c.get('email', '(none)')}, email_verified {c.get('email_verified', '(none)')}, "
          f"iss {c.get('iss')}, {int((c['exp'] - time.time()) / 60)} minutes left")
PY

"""

def step_02_what_your_token_says_about_itself(session):
    """Run Do it: what your token says about itself at this checkpoint.

    The cell mints two tokens for the API as documind-ui-sa: one the way tok does, and one without --include-email. It reads their claims without verifying them; the API does the verifying. Nothing is sent.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_the_three_rosters_as_firestore_holds_them(session):
    """Run Do it: the three rosters, as Firestore holds them at this checkpoint.

    Do it: the three rosters, as Firestore holds them

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    for t in ("acme", "zeta", "globex"):
        members = sorted(d.id for d in db.collection("tenants").document(t).collection("members").stream())
        print(f"{t:7} {len(members)} member(s)")
        for m in members:
            print("   ", m)

# Original CLI workflow for step_04_the_plan_make_roster_would_write_for_you.
COMMANDS_04 = """python commands/lane.py --project "$PROJECT" roster --tenant acme --members "$ME" --dry-run

"""

def step_04_the_plan_make_roster_would_write_for_you(session):
    """Run Do it: the plan make roster would write for you at this checkpoint.

    make roster runs this command without --dry-run. The dry run prints the memberships and the data-region policies it would set, and writes nothing.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (make roster's plan; --dry-run writes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_the_api_s_audiences_and_who_may_invoke_it),
        ('source_12', step_02_what_your_token_says_about_itself),
        ('source_17', step_03_the_three_rosters_as_firestore_holds_them),
        ('source_19', step_04_the_plan_make_roster_would_write_for_you),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
