"""Lesson 13.3: demo 01 routing and budget configuration

Read routing/budget/shutdown controls and establish the baseline.

Run order inside this file:
1. Do it (source window 9)
2. Do it (source window 11)

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


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the controls as the kit writes them down; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import pathlib, re, sys
    sys.path.insert(0, "services/rag-api")
    import breakers                                                     # the kit's own table, run below
    router, deploy, mk = (open(p, encoding="utf-8").read() for p in ("services/rag-api/router.py", "commands/lesson-12.2.sh", "Makefile"))
    budget_tf, off_tf = (open(f"terraform/{f}", encoding="utf-8").read() for f in ("budget.tf", "off.tf"))
    classes = re.findall(r"^    (SIMPLE|MEDIUM|COMPLEX) = ", router, re.M)
    print("per answer: ROUTING=" + re.search(r"ROUTING=\$\{ROUTING-(\w+)\}", deploy).group(1) + " on the lane (lesson-12.2.sh). With it on, "
          + re.search(r'CLASSIFIER_MODEL = "([^"]+)"', router).group(1) + " labels each question " + ", ".join(classes)
          + ", and breakers.choose_model() picks the model:")
    print((f"  {'spend':8}" + "".join(f"{c:24}" for c in classes)).rstrip())
    for pct in (0, 79.9, 80, 85, 100, 120):
        print((f"  {str(pct) + '%':8}" + "".join(f"{breakers.choose_model(c, pct):24}" for c in classes)).rstrip())
    cap = re.search(r"BUDGET_USD=\$\{BUDGET_USD-(\d+)\}", deploy).group(1)
    print(f"  the spend: Firestore budget/<month, UTC>, USD added by every answer, over BUDGET_USD ({cap} on the lane); SPEND_PCT replaces it")
    readers = [p.as_posix() for p in pathlib.Path("services").rglob("*.py") if "BUDGET_FLOOR_PCT" in p.read_text(encoding="utf-8") and p.name != "breakers.py"]
    print(f"  BUDGET_FLOOR_PCT = {breakers.BUDGET_FLOOR_PCT} (the comment's min-instances 0): read by " + (", ".join(readers) or "nothing"))
    rules = [float(t) for t in re.findall(r"threshold_percent = ([\d.]+)", budget_tf)]
    print("per month: " + re.search(r'display_name    = "([^"]+)"', budget_tf).group(1) + ", BUDGET_AMOUNT " + re.search(r"BUDGET_AMOUNT\s+\?= (\d+)", mk).group(1)
          + " in the billing account's currency; it emails at " + ", ".join(f"{r:.0%}" for r in rules[:-1]) + f" and at a {rules[-1]:.0%} forecast")
    loop = off_tf.split("for pair in", 1)[1].split("; do", 1)[0]
    print("per hour: documind-off runs " + re.search(r'schedule    = "([^"]+)"', off_tf).group(1) + " " + re.search(r'time_zone   = "([^"]+)"', off_tf).group(1)
          + " and floors " + ", ".join(re.findall(r"(documind-[\w-]+):", loop)) + " to min-instances 0; make off does the same by hand")
    print("  make gpu-cap: the GPU quota in " + re.search(r"SLM_REGION \?= ([\w-]+)", mk).group(1) + " capped at " + re.search(r"CAP \?= (\d+)", mk).group(1)
          + "; alerts.tf's gpu_left_warm pages when one stays up two hours")

# Original CLI workflow for step_02_example.
COMMANDS_02 = """python - <<'PY'
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

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_11', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
