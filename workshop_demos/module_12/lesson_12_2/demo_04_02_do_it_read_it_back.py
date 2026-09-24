"""Lesson 12.2 / s4: Deploy, and read it back

Summary and purpose:
Do it: read it back

HTML instruction: bash — run in the operator shell, in the kit (the service as deployed, against the script)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_build_and_deploy
Expected observation: serving     documind-mcp-00004-k7w at https://documind-mcp-NUMBER.asia-south1.run.app
  runs as     documind-mcp-sa
  ingress     all
  SELF_URL    https://documind-mcp-NUMBER.asia-south1.run.app
  invokers    documind-agent-sa, documind-outsider-sa, documind-ui-sa
  the script  documind-agent-sa, documind-outsider-sa, documind-ui-sa - the same

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L476

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: read it back at this checkpoint.

    Do it: read it back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the service as deployed, against the script).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gc(*a):
        return json.loads(subprocess.run(["gcloud", "run", "services", *a, "documind-mcp", "--region", os.environ["REGION"],
                                          "--project", os.environ["PROJECT"], "--format", "json"], capture_output=True, text=True, check=True).stdout)
    svc, policy = gc("describe"), gc("get-iam-policy")
    spec, meta = svc["spec"]["template"]["spec"], svc["spec"]["template"]["metadata"]
    env = {e["name"]: e.get("value") for e in spec["containers"][0].get("env", [])}
    print(f"  serving     {svc['status']['latestReadyRevisionName']} at {svc['status']['url']}")
    print(f"  runs as     {spec['serviceAccountName'].split('@')[0]}")
    print(f"  ingress     {svc['metadata']['annotations'].get('run.googleapis.com/ingress')}")
    print(f"  SELF_URL    {env.get('SELF_URL')}")
    invokers = sorted(m.split(":", 1)[1].split("@")[0] for b in policy.get("bindings", []) if b["role"] == "roles/run.invoker" for m in b["members"])
    print(f"  invokers    {', '.join(invokers)}")
    print(f"  the script  {', '.join(sorted(['documind-agent-sa', 'documind-outsider-sa', 'documind-ui-sa']))} - "
          + ("the same" if invokers == sorted(["documind-agent-sa", "documind-outsider-sa", "documind-ui-sa"]) else "DIFFERENT: someone bound more, or less"))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
