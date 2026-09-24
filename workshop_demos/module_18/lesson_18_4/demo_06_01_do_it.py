"""Lesson 18.4 / s6: Zero GPU instances

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, at least 10 minutes after make off (reads Cloud Monitoring; changes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: instance_count per service, 09:40 to 10:25 UTC, one point a minute (Cloud Monitoring):
  documind-slm      last instance at 10:13 UTC    a GPU service
  documind-vllm     no instance in the window     a GPU service
  documind-gateway  last instance at 10:09 UTC
  documind-ui       no instance in the window
GPU services with an instance in the last 3 minutes: none - zero GPU instances

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.4-compare-shutdown/Netsetos_GCP_Capstone_18.4_Compare_Shutdown_WIX.html#L647

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, at least 10 minutes after make off (reads Cloud Monitoring; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess, time, urllib.parse, urllib.request
    from datetime import datetime, timedelta, timezone
    P = os.environ["PROJECT"]
    tok = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
    now = datetime.fromtimestamp(time.time(), timezone.utc).replace(second=0, microsecond=0)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    q = urllib.parse.urlencode({"filter": 'metric.type="run.googleapis.com/container/instance_count" AND resource.type="cloud_run_revision"',
                                "interval.startTime": iso(now - timedelta(minutes=45)), "interval.endTime": iso(now),
                                "aggregation.alignmentPeriod": "60s", "aggregation.perSeriesAligner": "ALIGN_MAX",
                                "aggregation.crossSeriesReducer": "REDUCE_SUM", "aggregation.groupByFields": "resource.label.service_name"})
    req = urllib.request.Request(f"https://monitoring.googleapis.com/v3/projects/{P}/timeSeries?{q}", headers={"Authorization": f"Bearer {tok}"})
    last = {}
    for s in json.load(urllib.request.urlopen(req, timeout=60)).get("timeSeries", []):
        up = [p["interval"]["endTime"] for p in s.get("points", []) if int(p["value"].get("int64Value", 0)) > 0]
        last[s["resource"]["labels"]["service_name"]] = max(up) if up else None
    GPU = ("documind-slm", "documind-vllm")
    print(f"instance_count per service, {iso(now - timedelta(minutes=45))[11:16]} to {iso(now)[11:16]} UTC, one point a minute (Cloud Monitoring):")
    for name in GPU + ("documind-gateway", "documind-ui"):
        t = last.get(name)
        what = f"last instance at {t[11:16]} UTC" if t else "no instance in the window"
        print(f"  {name:17} " + (f"{what:28}  a GPU service" if name in GPU else what))
    fresh = iso(now - timedelta(minutes=3))           # a sample shows up to 120 s after it is taken
    still = [n for n in GPU if last.get(n) and last[n] >= fresh]
    print("GPU services with an instance in the last 3 minutes: " + (", ".join(still) if still else "none - zero GPU instances"))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
