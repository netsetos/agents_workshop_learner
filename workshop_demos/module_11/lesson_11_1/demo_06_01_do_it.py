"""Lesson 11.1 / s6: Which checkpointer your lane runs

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the checkpointer your chat service is configured with)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: CHECKPOINT_DSN  from the secret documind-checkpoint-dsn, version latest
  Cloud SQL       documind-ai-YOUR-ID:asia-south1:documind-checkpoint
  the memory warning in 30 days of the service's log: none

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html#L606

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
