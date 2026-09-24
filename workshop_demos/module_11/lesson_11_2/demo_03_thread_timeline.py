"""Lesson 11.2: demo 03 thread timeline

Follow one thread through its stored steps.

Run order inside this file:
1. Do it (source window 18)

Prerequisites: demo_02_deployed_storage_and_tables.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """~/graph-venv/bin/python - <<'PY'
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
    (thread,) = q("SELECT thread_id FROM checkpoints GROUP BY thread_id ORDER BY max(checkpoint->>'ts') DESC LIMIT 1")[0]
    size = dict(q("SELECT version, length(blob) FROM checkpoint_blobs WHERE thread_id = %s AND channel = 'messages'", thread))
    print(f"the latest thread, session {thread.split(':', 2)[2]}: its checkpoints in order")
    seen = []
    for step, source, version in q("SELECT (metadata->>'step')::int, metadata->>'source', checkpoint->'channel_versions'->>'messages' "
                                   "FROM checkpoints WHERE thread_id = %s ORDER BY checkpoint_id", thread):
        new = version is not None and version not in seen
        seen += [version] if new else []
        print(f"  step {step:>2}  {source:5}  " + (f"messages, version {len(seen)}: {size[version]:>6,} bytes" if new else "messages unchanged"))
    print(f"every version kept: {sum(size.values()):,} bytes; the latest alone: {size[max(size)]:,} bytes")
    db.close()
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the latest thread, step by step).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_18', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
