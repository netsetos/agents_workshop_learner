"""Lesson 13.3 / s6: Off at night, and the ceiling under it

Summary and purpose:
A floor of zero lets the service scale to zero, but an idle instance can stay up for up to fifteen minutes after its last request. The cell waits, then reads the UI's instance count from Cloud Monitoring for the last half hour, a sample a minute.

HTML instruction: bash — run in the operator shell, in the kit (after 15 minutes; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_floor_then_the_switch
Expected observation: documind-ui, container instances (active and idle), a sample a minute, last 30 minutes:
  11:52 1  11:53 1  11:54 1  11:55 1  11:56 1  11:57 1  11:58 1  11:59 1  12:00 1  12:01 1
  12:02 1  12:03 1  12:04 1  12:05 1  12:06 1  12:07 1  12:08 1  12:09 0  12:10 0  12:11 0
  12:12 0  12:13 0  12:14 0  12:15 0  12:16 0  12:17 0  12:18 0  12:19 0  12:20 0  12:21 0
zero instances since 12:09 IST

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L684

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sleep 900     # Cloud Run keeps an idle instance up to 15 minutes
python - <<'PY'
import datetime as dt, json, os, subprocess, urllib.parse, urllib.request
P = os.environ["PROJECT"]
tok = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
stamp = lambda t: t.isoformat().replace("+00:00", "Z")
query = {"filter": 'metric.type="run.googleapis.com/container/instance_count" AND resource.labels.service_name="documind-ui"',
         "interval.startTime": stamp(end - dt.timedelta(minutes=30)), "interval.endTime": stamp(end)}
url = f"https://monitoring.googleapis.com/v3/projects/{P}/timeSeries?" + urllib.parse.urlencode(query)
series = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + tok}), timeout=60))
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
count = {}
for s in series.get("timeSeries", []):                          # one series per state: active, idle
    for p in s["points"]:
        t = dt.datetime.fromisoformat(p["interval"]["endTime"].replace("Z", "+00:00")).astimezone(IST)
        count[t] = count.get(t, 0) + int(p["value"]["int64Value"])
points = sorted(count.items())
print("documind-ui, container instances (active and idle), a sample a minute, last 30 minutes:")
for i in range(0, len(points), 10):
    print("  " + "  ".join(f"{t:%H:%M} {n}" for t, n in points[i:i + 10]))
zero = next((t for i, (t, n) in enumerate(points) if all(m == 0 for _, m in points[i:])), None)
print(f"zero instances since {zero:%H:%M} IST" if zero and points[-1][1] == 0
      else "not zero yet: an idle instance can stay up to 15 minutes after its last request; run this again")
PY
"""


def demonstrate(session):
    """Run Do it: the instances, after fifteen minutes at this checkpoint.

    A floor of zero lets the service scale to zero, but an idle instance can stay up for up to fifteen minutes after its last request. The cell waits, then reads the UI's instance count from Cloud Monitoring for the last half hour, a sample a minute.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (after 15 minutes; reads only).
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
