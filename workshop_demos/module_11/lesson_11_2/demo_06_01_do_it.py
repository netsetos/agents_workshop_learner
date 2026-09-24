"""Lesson 11.2 / s6: One thread, step by step

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the latest thread, step by step)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: the latest thread, session lesson111-4242-b: its checkpoints in order
  step -1  input  messages unchanged
  step  0  loop   messages, version 1:    175 bytes
  step  1  loop   messages, version 2:    412 bytes
  step  2  input  messages unchanged
  step  3  loop   messages, version 3:    586 bytes
  step  4  loop   messages, version 4:    866 bytes
  step  5  loop   messages, version 5:  2,285 bytes
  step  6  loop   messages, version 6:  2,522 bytes
every version kept: 6,846 bytes; the latest alone: 2,522 bytes

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.2-durable-storage/Netsetos_GCP_Capstone_11.2_Durable_Storage_WIX.html#L635

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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the latest thread, step by step).
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
