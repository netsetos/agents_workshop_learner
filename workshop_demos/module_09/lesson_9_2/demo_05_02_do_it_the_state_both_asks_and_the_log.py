"""Lesson 9.2 / s5: The corpus moves: revision 2, and both caches react

Summary and purpose:
Do it: the state, both asks, and the log

HTML instruction: bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_the_release
Expected observation: ledger 1441fb4775d21e13 (17 versions, last ingest_reactivated) | context cache packed from 1ef46119bd89b143: STALE
  vertex none     in   1880 cached      0  2390 ms | From 1 October 2026 the notice period for a confir
  vertex none     in   1880 cached      0  2455 ms | From 1 October 2026 the notice period for a confir
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L564

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """state92
ask92 "$API"            # the live revision
ask92 "$CAND"           # the candidate
python - <<'PY'
import json, os, subprocess
f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="cache_stale" '
     f'AND timestamp>="{os.environ["SINCE92"]}"')
out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "5",
                      "--format", "json"], capture_output=True, text=True, check=True).stdout
for e in json.loads(out or "[]"):
    j = e["jsonPayload"]
    print(f"  cache_stale {j['tenant']}: packed from {j['cache_fingerprint']}, ledger now {j['ledger_fingerprint']}")
PY
"""


def demonstrate(session):
    """Run Do it: the state, both asks, and the log at this checkpoint.

    Do it: the state, both asks, and the log

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines).
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
