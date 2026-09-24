"""Lesson 13.3 / s4: The month so far

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: documind-api: ROUTING=off, BUDGET_USD=100, SPEND_PCT=unset
the counter, budget/2026-09: USD 7.8412 of 100 = 7.84% - the breaker would read 'normal'
the billing budget: 5000 INR a month on the whole project; emails at 50%, 80%, 100%, 120% forecast
python services/slm/gpu_quota.py --project documind-ai-YOUR-ID --region us-central1

Total NVIDIA L4 GPU allocation without zonal redundancy
  run.googleapis.com/nvidia_l4_gpu_allocation_no_zonal_redundancy
  1/{project}/{region}         us-central1  effective 3 (default 3)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L523

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import datetime as dt, json, os, subprocess
from google.cloud import firestore
P, R = os.environ["PROJECT"], os.environ["REGION"]
def gcloud(*a):
    return subprocess.run(["gcloud", *a], capture_output=True, text=True)
svc = json.loads(gcloud("run", "services", "describe", "documind-api", "--region", R, "--project", P, "--format", "json").stdout)
env = {e["name"]: e.get("value") for e in svc["spec"]["template"]["spec"]["containers"][0].get("env", [])}
month = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m")
snap = firestore.Client(project=P).collection("budget").document(month).get()
usd = float((snap.to_dict() or {}).get("usd", 0.0)) if snap.exists else 0.0
cap = float(env.get("BUDGET_USD") or 100)
pct = float(env["SPEND_PCT"]) if env.get("SPEND_PCT") else 100 * usd / cap
print(f"documind-api: ROUTING={env.get('ROUTING', 'off')}, BUDGET_USD={cap:g}, SPEND_PCT={env.get('SPEND_PCT') or 'unset'}")
print(f"the counter, budget/{month}: USD {usd:.4f} of {cap:g} = {pct:.2f}% - the breaker would read '{'strict' if pct >= 80 else 'normal'}'")
account = gcloud("billing", "projects", "describe", P, "--format=value(billingAccountName)").stdout.strip().rsplit("/", 1)[-1]
b = gcloud("billing", "budgets", "list", f"--billing-account={account}", "--format=json")
if b.returncode != 0:
    print("the billing budget: not readable as you (the Budgets API needs billing.budgets.list on the billing account)")
for budget in json.loads(b.stdout or "[]") if b.returncode == 0 else []:
    if budget.get("displayName") == "DocuMind monthly budget":
        amount = budget["amount"]["specifiedAmount"]
        rules = ", ".join(f"{float(t['thresholdPercent']):.0%}" + (" forecast" if t.get("spendBasis") == "FORECASTED_SPEND" else "")
                          for t in budget.get("thresholdRules", []))
        print(f"the billing budget: {amount.get('units')} {amount.get('currencyCode')} a month on the whole project; emails at {rules}")
PY
make gpu-quota PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
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
