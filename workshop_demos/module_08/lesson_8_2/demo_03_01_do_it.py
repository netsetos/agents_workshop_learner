"""Lesson 8.2 / s3: The refusal ladder: the door, a 401 and a 403 side by side

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (four requests to /v1/query; one is answered)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: no token                   403  (Cloud Run's own page: the request never reached the API)
  a token without its email  401  {"detail":"the bearer token carries no verified email"}
  the outsider's token       403  {"detail":"not a member of this tenant"}
  documind-ui-sa's token     200  {"answer":"A confirmed employee at grade E3 or above serves a noti

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html#L427

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" BARE="$(gcloud auth print-identity-token --audiences="$API" --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com")" \\
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four requests to /v1/query; one is answered).
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
