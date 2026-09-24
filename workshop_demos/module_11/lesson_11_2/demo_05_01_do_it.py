"""Lesson 11.2 / s5: The tables, and one row per thread

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the tables, their rows, and one row per thread)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: documind-ai-YOUR-ID:asia-south1:documind-checkpoint, database documind, as chat: 4 tables
  checkpoint_blobs           35 rows
  checkpoint_migrations      10 rows
  checkpoint_writes          37 rows
  checkpoints                29 rows
setup() has applied migrations 0 to 9
one row per thread, the latest first:
  acme  documind-ui-sa  lesson111-4242-b     8 checkpoints  step  6  2026-09-23T10:03
  acme  documind-ui-sa  lesson111-4242       6 checkpoints  step  4  2026-09-23T10:02
  acme  documind-ui-sa  smoke-langgraph      5 checkpoints  step  3  2026-09-23T09:16
  acme  documind-ui-sa  smoke-langchain      5 checkpoints  step  3  2026-09-23T09:15
  acme  documind-ui-sa  lesson103            5 checkpoints  step  3  2026-09-23T08:41
no ADK tables: the ADK brain's sessions are not in this database

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.2-durable-storage/Netsetos_GCP_Capstone_11.2_Durable_Storage_WIX.html#L581

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """~/graph-venv/bin/python - <<'PY'
import os, subprocess
from urllib.parse import unquote, urlparse
from google.cloud.sql.connector import Connector
gc = lambda *a: subprocess.run(["gcloud", *a, "--project", os.environ["PROJECT"]], capture_output=True, text=True, check=True).stdout.strip()
dsn = urlparse(gc("secrets", "versions", "access", "latest", "--secret", "documind-checkpoint-dsn"))   # the password stays in memory
instance = gc("sql", "instances", "describe", "documind-checkpoint", "--format", "value(connectionName)")
with Connector() as connector:
    db = connector.connect(instance, "pg8000", user=dsn.username, password=unquote(dsn.password), db=dsn.path.lstrip("/"))
    cur = db.cursor()
    def q(sql, *args):
        cur.execute(sql, args)                  # a tuple, empty or not: pg8000 takes len() of it, and None has none
        return cur.fetchall()
    tables = [t for (t,) in q("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")]
    print(f"{instance}, database {dsn.path.lstrip('/')}, as {dsn.username}: {len(tables)} tables")
    for t in tables:
        print(f"  {t:22} {q(f'SELECT count(*) FROM {t}')[0][0]:>6,} rows")
    print(f"setup() has applied migrations 0 to {q('SELECT max(v) FROM checkpoint_migrations')[0][0]}")
    print("one row per thread, the latest first:")
    for thread, n, step, ts in q("SELECT thread_id, count(*), max((metadata->>'step')::int), max(checkpoint->>'ts') "
                                 "FROM checkpoints GROUP BY thread_id ORDER BY 4 DESC LIMIT 12"):
        tenant, person, session = thread.split(":", 2)
        print(f"  {tenant:5} {person.split('@')[0][:15]:15} {session[:18]:18} {n:>3} checkpoints  step {step:>2}  {ts[:16]}")
    if "sessions" not in tables:
        print("no ADK tables: the ADK brain's sessions are not in this database")
    db.close()
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the tables, their rows, and one row per thread).
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
