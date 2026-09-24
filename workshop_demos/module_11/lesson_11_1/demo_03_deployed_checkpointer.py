"""Lesson 11.1: demo 03 deployed checkpointer

Read which checkpointer the deployed lane actually uses.

Run order inside this file:
1. Do it (source window 18)

Prerequisites: demo_02_history_across_brains.
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
    Operations: bash — run in the operator shell, in the kit (the checkpointer your chat service is configured with).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gc(*args):
        return subprocess.run(["gcloud", *args, "--project", os.environ["PROJECT"]], capture_output=True, text=True, check=True).stdout
    tpl = json.loads(gc("run", "services", "describe", "documind-chat", "--region", os.environ["REGION"], "--format", "json"))["spec"]["template"]
    env = {e["name"]: e for e in tpl["spec"]["containers"][0].get("env", [])}
    dsn = env.get("CHECKPOINT_DSN", {})
    ref = dsn.get("valueFrom", {}).get("secretKeyRef")
    print("  CHECKPOINT_DSN  " + (f"from the secret {ref['name']}, version {ref['key']}" if ref else f"= {dsn.get('value')!r}"))
    print("  Cloud SQL       " + tpl["metadata"].get("annotations", {}).get("run.googleapis.com/cloudsql-instances", "none"))
    seen = gc("logging", "read", 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-chat" '
              'AND textPayload:"CHECKPOINT_DSN=memory"', "--freshness", "30d", "--limit", "1", "--format", "value(timestamp)").strip()
    print("  the memory warning in 30 days of the service's log: " + (seen or "none"))

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
