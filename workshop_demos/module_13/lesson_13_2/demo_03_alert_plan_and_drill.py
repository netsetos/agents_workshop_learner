"""Lesson 13.2: demo 03 alert plan and drill

Plan/apply the reviewed alert configuration, exercise the drill and inspect its message.

Run order inside this file:
1. Do it: plan and apply (source window 18)
2. Do it: the drill (source window 20)
3. Do it: drain the drill message (source window 22)

Prerequisites: demo_02_reports_and_alert_policy.
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


# Original CLI workflow for step_01_plan_and_apply.
COMMANDS_01 = """make plan PROJECT="$PROJECT" REGION="$REGION" ADMIN_EMAILS="$ME"   # the flags you gave make up; the plan refuses to delete
python commands/infrastructure.py apply --project "$PROJECT" --region "$REGION" --terraform-dir terraform   # make up's first line, alone

"""

def step_01_plan_and_apply(session):
    """Run Do it: plan and apply at this checkpoint.

    Do it: plan and apply

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the checkout where make up ran (Terraform's state).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_drill.
COMMANDS_02 = """gcloud pubsub topics publish documind-ingest-dlq --project "$PROJECT" --message="drill 13.2: not an upload" --attribute=drill=13.2
sleep 300     # a sample a minute, shown up to two minutes late, and the policy wants a minute above zero
python - <<'PY'
import datetime as dt, json, os, subprocess, urllib.parse, urllib.request
P = os.environ["PROJECT"]
tok = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
def monitoring(path, **query):
    url = f"https://monitoring.googleapis.com/v3/projects/{P}/{path}" + ("?" + urllib.parse.urlencode(query) if query else "")
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + tok}), timeout=60))
end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
stamp = lambda t: t.isoformat().replace("+00:00", "Z")
series = monitoring("timeSeries", filter='metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages" '
                                          'AND resource.labels.subscription_id="ingest-dlq-sub"',
                    **{"interval.startTime": stamp(end - dt.timedelta(minutes=10)), "interval.endTime": stamp(end)})
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
points = sorted((dt.datetime.fromisoformat(p["interval"]["endTime"].replace("Z", "+00:00")).astimezone(IST), int(p["value"]["int64Value"]))
                for s in series.get("timeSeries", []) for p in s["points"])
print("ingest-dlq-sub, undelivered messages - the gauge the policy reads, a sample a minute:")
print("  " + "  ".join(f"{t:%H:%M} {n}" for t, n in points))
for p in monitoring("alertPolicies").get("alertPolicies", []):
    th = p["conditions"][0].get("conditionThreshold", {})
    if "ingest-dlq-sub" in th.get("filter", ""):
        print(f"policy: {p['displayName']} - above {th.get('thresholdValue', 0)} for {th['duration']}, "
              f"{len(p.get('notificationChannels', []))} notification channel(s)")
above = [t for t, n in points if n > 0]
print(f"above zero since {above[0]:%H:%M} IST: the condition holds - Monitoring > Alerting shows the incident" if above
      else "not above zero yet: Pub/Sub's sample can take two minutes to appear; run this again")
PY

"""

def step_02_the_drill(session):
    """Run Do it: the drill at this checkpoint.

    A drill proves the alert end to end without waiting an hour for a poison upload. The cell publishes one message straight to the dead-letter topic, labelled drill=13.2. After five minutes it reads the gauge the policy reads, a sample a minute, and the policy itself.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one drill message into the dead-letter queue, then the gauge).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_drain_the_drill_message(session):
    """Run Do it: drain the drill message at this checkpoint.

    The drill message must not stay in the queue, and a real message must not be thrown away with it. The cell pulls without acknowledging, acknowledges only the messages labelled drill=13.2, and leaves anything else for make dlq.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acknowledges the drill message only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    P = os.environ["PROJECT"]
    def gcloud(*a):
        return subprocess.run(["gcloud", *a], capture_output=True, text=True, check=True).stdout
    pulled = json.loads(gcloud("pubsub", "subscriptions", "pull", "ingest-dlq-sub", "--project", P, "--limit", "10", "--format=json") or "[]")
    drill = [m["ackId"] for m in pulled if (m["message"].get("attributes") or {}).get("drill") == "13.2"]
    if drill:
        gcloud("pubsub", "subscriptions", "ack", "ingest-dlq-sub", "--project", P, "--ack-ids=" + ",".join(drill))
    print(f"pulled {len(pulled)}; acknowledged {len(drill)} drill message(s); {len(pulled) - len(drill)} other(s) left for make dlq")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_18', step_01_plan_and_apply),
        ('source_20', step_02_the_drill),
        ('source_22', step_03_drain_the_drill_message),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
