"""Lesson 13.3 / s5: The tier at 85 percent

Summary and purpose:
Do it: routing on, the month as it is

HTML instruction: bash — run in the operator shell, in the kit (a candidate revision, no traffic, ROUTING on; three questions)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: gemini-3.1-flash-lite    What is the notice period for a confirmed E3?
                           A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  gemini-3.6-flash         Explain what happens when a trip costs more than the per-trip travel cap.
                           Travel is capped at Rs 40,000 per trip [1]; a trip above the cap needs the function head's written approval before travel [1].
  gemini-3.1-pro-preview   Work out, step by step, the total reimbursed for three domestic trips costing Rs 38,000, Rs 45,000 and Rs 22,000.
                           Each trip is reimbursed up to the cap of Rs 40,000 [1]: Rs 38,000 + Rs 40,000 + Rs 22,000 = Rs 1,00,000; the Rs 5,000 above the cap ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L580

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars ROUTING=on --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
ask133() {   # ask133 URL: three acme questions (a lookup, an explanation, a worked sum) as documind-ui-sa - the model that answered each
URL="$1" python - <<'PY'
import json, os, subprocess, urllib.request
P, API, URL = os.environ["PROJECT"], os.environ["API"], os.environ["URL"]
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
for q in ['What is the notice period for a confirmed E3?', 'Explain what happens when a trip costs more than the per-trip travel cap.', 'Work out, step by step, the total reimbursed for three domestic trips costing Rs 38,000, Rs 45,000 and Rs 22,000.']:
    body = json.dumps({"query": q, "tenant_id": "acme"}).encode()
    req = urllib.request.Request(URL + "/v1/query", data=body, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    a = json.load(urllib.request.urlopen(req, timeout=180))
    print(f"  {a['model']:24} {q}")
    print(f"  {'':24} {a['answer'][:132] + ('...' if len(a['answer']) > 132 else '')}")
PY
}
ask133 "$CAND"
"""


def demonstrate(session):
    """Run Do it: routing on, the month as it is at this checkpoint.

    Do it: routing on, the month as it is

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a candidate revision, no traffic, ROUTING on; three questions).
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
