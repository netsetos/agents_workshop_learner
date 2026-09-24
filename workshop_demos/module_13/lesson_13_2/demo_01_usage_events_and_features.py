"""Lesson 13.2: demo 01 usage events and features

Inspect emitted usage events and the feature/report inputs built from them.

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
    Operations: bash — run in the operator shell, in the kit (the readers as the kit writes them down; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import re
    def between(text, start, end):
        return text.split(start, 1)[1].split(end, 1)[0]
    sink = between(open("terraform/sink.tf", encoding="utf-8").read(), "filter", "EOT\n  unique")
    view = open("terraform/sql/tenant_daily.sql", encoding="utf-8").read()
    tool = open("evals/usage_rows.py", encoding="utf-8").read()
    alerts = open("terraform/alerts.tf", encoding="utf-8").read()
    queries = between(alerts, 'name    = "documind/queries"', "EOT\n  metric")
    readers = [
        ("the sink, into BigQuery", re.findall(r'service_name = "([\w-]+)"', sink), re.findall(r'event = "(\w+)"', sink),
         "every row, as it is written"),
        ("tenant_daily, the view", ["what the sink copied"], re.findall(r'"(\w+)"', between(view, "WHERE jsonPayload.event IN (", ")")),
         "one row per India day and " + str(len(between(view, "GROUP BY day,", ";").split(","))) + " dimensions"),
        ("make usage", [re.search(r'"--service", default="([\w-]+)"', tool).group(1)], re.findall(r'event="(\w+)"', between(tool, "def read_rows", "def p95")),
         "the last N hours (default " + re.search(r'"--hours", type=int, default=(\d+)', tool).group(1) + "), at most "
         + re.search(r"limit: int = (\d+)", tool).group(1) + " rows"),
        ("documind/queries, for alerts", re.findall(r'service_name="([\w-]+)"', queries), re.findall(r'event="(\w+)"', queries), "counted as written"),
    ]
    print(f"{'reader':30} {'services':28} {'events':21} window")
    for name, services, events, when in readers:
        print(f"{name:30} {', '.join(services):28} {', '.join(events):21} {when}")
    inr = re.search(r"\* (\d+), 2\) AS cost_inr", view).group(1)
    print(f"rupees: tenant_daily's cost_inr is cost_usd x {inr}; make usage's USD_INR is {re.search(r'USD_INR = (\d+)', tool).group(1)}")
    events = {name: set(e) for name, _, e, _ in readers}
    for ev in sorted(set().union(*events.values())):
        print(f"  {ev:7} read by: " + ", ".join(n for n, _, e, _ in readers if ev in e))
    policies = re.findall(r'resource "google_monitoring_alert_policy" "(\w+)"', alerts)
    print(f"alert policies in terraform/alerts.tf: {len(policies)} - " + ", ".join(policies))
    print("the one that reads the dead-letter queue: " + ", ".join(p for p in policies
          if "ingest_dlq_sub" in between(alerts, f'"google_monitoring_alert_policy" "{p}"', "\n}\n")))

# Original CLI workflow for step_02_example.
COMMANDS_02 = """python - <<'PY'
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

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four questions, then make usage).
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
