"""Lesson 11.3 / s6: The rows behind both

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the rows behind steps 4 and 5)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: lesson113-4242-langchain: 6 checkpoints, 3 before the redeploy and 3 after
  lesson113-4242-adk: no rows - the ADK brain keeps none
  threads of you: 1; the latest is session 3f9c2a1d0b7e, 3 checkpoints
  threads of documind-ui-sa: 2; the latest is session lesson113-4242-langchain, 6 checkpoints

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.3-restart-isolation/Netsetos_GCP_Capstone_11.3_Restart_Isolation_WIX.html#L587

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import json, os, subprocess
from urllib.parse import unquote, urlparse
from google.cloud.sql.connector import Connector
gc = lambda *a: subprocess.run(["gcloud", *a, "--project", os.environ["PROJECT"]], capture_output=True, text=True, check=True).stdout.strip()
dsn = urlparse(gc("secrets", "versions", "access", "latest", "--secret", "documind-checkpoint-dsn"))   # the password stays in memory
instance = gc("sql", "instances", "describe", "documind-checkpoint", "--format", "value(connectionName)")
state = json.load(open(os.path.expanduser("~/lesson113.json")))
with Connector() as connector:
    db = connector.connect(instance, "pg8000", user=dsn.username, password=unquote(dsn.password), db=dsn.path.lstrip("/"))
    cur = db.cursor()
    def q(sql, *args):
        cur.execute(sql, args)                  # a tuple, empty or not: pg8000 takes len() of it, and None has none
        return cur.fetchall()
    for brain in ("langchain", "adk"):
        session = f"{state['session']}-{brain}"
        ts = [t for (t,) in q("SELECT checkpoint->>'ts' FROM checkpoints WHERE thread_id LIKE %s ORDER BY checkpoint_id", "%:" + session)]
        before = sum(t[:19] < state["redeployed_at"] for t in ts)
        print(f"  {session}: " + (f"{len(ts)} checkpoints, {before} before the redeploy and {len(ts) - before} after" if ts
                                  else "no rows - the ADK brain keeps none"))
    for person in (os.environ["ME"], "documind-ui-sa@"):
        rows = q("SELECT thread_id, count(*) FROM checkpoints WHERE thread_id LIKE %s GROUP BY thread_id ORDER BY max(checkpoint->>'ts') DESC",
                 f"%:{person}%")
        print(f"  threads of {person.split('@')[0]}: {len(rows)}" + (f"; the latest is session {rows[0][0].split(':', 2)[2]}, {rows[0][1]} checkpoints" if rows else ""))
    db.close()
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the rows behind steps 4 and 5).
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
