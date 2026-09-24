"""Lesson 13.2 / s6: The alert the dead-letter queue never had

Summary and purpose:
A drill proves the alert end to end without waiting an hour for a poison upload. The cell publishes one message straight to the dead-letter topic, labelled drill=13.2. After five minutes it reads the gauge the policy reads, a sample a minute, and the policy itself.

HTML instruction: bash — run in the operator shell, in the kit (one drill message into the dead-letter queue, then the gauge)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it_plan_and_apply
Expected observation: messageIds:
- '17405836920431227'
ingest-dlq-sub, undelivered messages - the gauge the policy reads, a sample a minute:
  11:30 0  11:31 0  11:32 0  11:33 1  11:34 1  11:35 1  11:36 1  11:37 1
policy: Ingest dead-letter queue holds messages - above 0 for 60s, 1 notification channel(s)
above zero since 11:33 IST: the condition holds - Monitoring > Alerting shows the incident

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.2-usage-reconcile/Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html#L776

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud pubsub topics publish documind-ingest-dlq --project "$PROJECT" --message="drill 13.2: not an upload" --attribute=drill=13.2
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


def demonstrate(session):
    """Run Do it: the drill at this checkpoint.

    A drill proves the alert end to end without waiting an hour for a poison upload. The cell publishes one message straight to the dead-letter topic, labelled drill=13.2. After five minutes it reads the gauge the policy reads, a sample a minute, and the policy itself.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one drill message into the dead-letter queue, then the gauge).
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
