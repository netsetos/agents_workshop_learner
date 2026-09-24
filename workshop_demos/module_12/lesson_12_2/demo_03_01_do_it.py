"""Lesson 12.2 / s3: The door, as the kit writes it down

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the door as the kit writes it down; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: documind-mcp, as commands/lesson-7.2.sh deploys it:
  --no-allow-unauthenticated  --ingress=all  --min-instances=${MIN_INSTANCES:-0}  --service-account=documind-mcp-sa
  SELF_URL=https://documind-mcp-$PROJECT_NUMBER.${REGION:-us-central1}.run.app
  RAG_API_URL=https://documind-api-$PROJECT_NUMBER.${REGION:-us-central1}.run.app
  FASTMCP_STATELESS_HTTP=true
  RAG_TIMEOUT_S=90
who may call it (roles/run.invoker): documind-ui-sa, documind-agent-sa, documind-outsider-sa
the tenants each caller may read through it (lane.py's roster_plan):
  documind-ui-sa         acme, zeta, globex
  documind-agent-sa      acme
  documind-outsider-sa   none
the account rag-api sees for every MCP retrieval: documind-mcp-sa, on acme, zeta, globex

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L413

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
