"""Lesson 11.2: demo 02 deployed storage and tables

Read the deployed storage configuration and inspect the checkpoint tables.

Run order inside this file:
1. Do it (source window 14)
2. Do it (source window 16)

Prerequisites: demo_01_turns_and_writes.
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
    Operations: bash — run in the operator shell, in the kit (what holds the conversations on your lane).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gc(*args):
        r = subprocess.run(["gcloud", *args, "--project", os.environ["PROJECT"], "--format", "json"], capture_output=True, text=True)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    i = gc("sql", "instances", "describe", "documind-checkpoint")
    s, ip = i["settings"], i["settings"].get("ipConfiguration", {})
    print(f"  instance      {i['name']}: {i['databaseVersion']}, {s['tier']}, {s['availabilityType'].lower()}, {s['dataDiskSizeGb']} GB")
    print(f"  backups       {'on' if s.get('backupConfiguration', {}).get('enabled') else 'off'}")
    print(f"  network       public IP {'on' if ip.get('ipv4Enabled') else 'off'}, {len(ip.get('authorizedNetworks', []))} authorized networks")
    print(f"  databases     {', '.join(d['name'] for d in gc('sql', 'databases', 'list', '--instance', i['name']))}")
    print(f"  users         {', '.join(u['name'] for u in gc('sql', 'users', 'list', '--instance', i['name']))}")
    v = gc("secrets", "versions", "list", "documind-checkpoint-dsn") or []
    print(f"  the DSN       secret documind-checkpoint-dsn, {len(v)} version(s), the latest {v[0]['state'].lower() if v else 'missing'}")
    tag = lambda image: image.rsplit(":", 1)[-1][:12]
    job = gc("run", "jobs", "describe", "documind-checkpoint-setup", "--region", os.environ["REGION"])
    svc = gc("run", "services", "describe", "documind-chat", "--region", os.environ["REGION"])
    if job and svc:
        ran = (gc("run", "jobs", "executions", "list", "--job", "documind-checkpoint-setup", "--region", os.environ["REGION"], "--limit", "1") or [{}])[0]
        ji, si = job["spec"]["template"]["spec"]["template"]["spec"]["containers"][0]["image"], svc["spec"]["template"]["spec"]["containers"][0]["image"]
        print(f"  setup job     last run {ran.get('metadata', {}).get('creationTimestamp', 'never')[:16]}, succeeded {ran.get('status', {}).get('succeededCount', 0)}")
        print(f"  images        job chat:{tag(ji)}, service chat:{tag(si)} - {'the same' if ji == si else 'DIFFERENT'}")
    else:
        print(f"  setup job     not found beside documind-chat in {os.environ['REGION']}")
    adk = subprocess.run(["gcloud", "logging", "read", 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-chat" '
                          'AND textPayload:"DatabaseSessionService unavailable"', "--project", os.environ["PROJECT"], "--freshness", "30d",
                          "--limit", "1", "--format", "value(textPayload)"], capture_output=True, text=True).stdout.strip()
    print("  ADK sessions  " + ("in memory: " + adk[:62] if adk else "no fallback warning in 30 days of the log"))

# Original CLI workflow for step_02_example.
COMMANDS_02 = """~/graph-venv/bin/python - <<'PY'
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

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the tables, their rows, and one row per thread).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_14', step_01_example),
        ('source_16', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
