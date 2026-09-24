"""Lesson 12.2: demo 01 mcp identity and deployment

Read the MCP identity, build/deploy the server and inspect the deployed configuration.

Run order inside this file:
1. Do it (source window 9)
2. Do it: build and deploy (source window 11)
3. Do it: read it back (source window 13)

Prerequisites: setup_prepare.
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
    Operations: bash — run in the operator shell, in the kit (the door as the kit writes it down; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import re, sys
    sys.path[:0] = [".", "commands"]
    from lane import roster_plan
    deploy = open("commands/lesson-7.2.sh").read().split("# ---- DEPLOY ----")[1].split("# ---- SMOKE ----")[0]
    print("documind-mcp, as commands/lesson-7.2.sh deploys it:")
    print("  " + "  ".join("--" + f.replace("@$PROJECT.iam.gserviceaccount.com", "") for f in
          re.findall(r"--(no-allow-unauthenticated|ingress=\S+|service-account=\S+|min-instances=\S+)", deploy)))
    env = dict(kv.split("=", 1) for kv in re.search(r'--set-env-vars="\^\|\^([^"]+)"', deploy).group(1).split("|"))
    for k in ("SELF_URL", "RAG_API_URL", "FASTMCP_STATELESS_HTTP", "RAG_TIMEOUT_S"):
        print(f"  {k}={env[k]}")
    callers = re.search(r"for who in ([\w\- ]+); do", deploy).group(1).split()
    print("who may call it (roles/run.invoker):", ", ".join(callers))
    rosters = {}
    for tenant, email in roster_plan("PROJECT", "acme", [])[0]:
        rosters.setdefault(email.split("@")[0], []).append(tenant)
    print("the tenants each caller may read through it (lane.py's roster_plan):")
    for who in callers:
        print(f"  {who:22} {', '.join(rosters.get(who, [])) or 'none'}")
    print(f"the account rag-api sees for every MCP retrieval: documind-mcp-sa, on {', '.join(rosters['documind-mcp-sa'])}")

# Original CLI workflow for step_02_build_and_deploy.
COMMANDS_02 = """make build deploy-services PROJECT="$PROJECT" REGION="$REGION" SERVICES=mcp SCRIPTS=commands/lesson-7.2.sh ADMIN_EMAILS="$ME"

"""

def step_02_build_and_deploy(session):
    """Run Do it: build and deploy at this checkpoint.

    Do it: build and deploy

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_read_it_back(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_11', step_02_build_and_deploy),
        ('source_13', step_03_read_it_back),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
