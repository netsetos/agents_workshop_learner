"""Lesson 13.2 / s4: Four questions, four rows

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (four questions, then make usage)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: acme  answered   839 in  46 out  cost_usd None  What is the per-trip cap on domestic travel reimbursement?
  acme  answered   399 in  44 out  cost_usd None  What is the notice period for a confirmed E3?
  acme  refused    915 in  39 out  cost_usd None  What is ACME's sabbatical policy?
  zeta  answered   843 in  46 out  cost_usd None  What is the per-trip cap on travel reimbursement?
python evals/usage_rows.py --project documind-ai-YOUR-ID --hours ${HOURS:-24}
4 answers from documind-api in the last 1 h; USD_INR=85

by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
acme                         3      2153      129    0.0042      0.36    2348   0.33
zeta                         1       843       46    0.0016      0.14    2506   0.00

by model and backend (what 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.2-usage-reconcile/Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html#L525

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import json, os, subprocess, urllib.request
P, API = os.environ["PROJECT"], os.environ["API"]
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
ASKS = [('acme', 'What is the per-trip cap on domestic travel reimbursement?'), ('acme', 'What is the notice period for a confirmed E3?'), ('acme', "What is ACME's sabbatical policy?"), ('zeta', 'What is the per-trip cap on travel reimbursement?')]
for tenant, question in ASKS:
    body = json.dumps({"query": question, "tenant_id": tenant}).encode()
    req = urllib.request.Request(API + "/v1/query", data=body, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    a = json.load(urllib.request.urlopen(req, timeout=120))
    print(f"  {tenant:5} {'answered' if a['answerable'] else 'refused':8} {a['tokens_in']:>5} in {a['tokens_out']:>3} out  "
          f"cost_usd {a['cost_usd']}  {question}")
PY
sleep 20      # Cloud Logging needs a moment to show the rows
make usage PROJECT="$PROJECT" HOURS=1
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four questions, then make usage).
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
