"""Lesson 12.3 / s3: The peer's permissions, as the kit writes them

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the peer's permissions, as the kit writes them; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: documind-agent, as commands/lesson-8.4.sh deploys it:
  runs as documind-agent-sa  model gemini-3.6-flash  knows one URL: MCP_URL
  who may call it: documind-ui-sa, documind-chat-sa
  documind-agent-sa may call documind-mcp: True
  its project roles: aiplatform.user, logging.logWriter, cloudtrace.agent
  the rosters it is on: acme
  agent.py imports: __future__, google, logging, os, starlette, urllib, uvicorn
  the image copies: services/agent/requirements.txt, services/agent/

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html#L427

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the peer's permissions, as the kit writes them; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, re, sys
    sys.path[:0] = [".", "commands"]
    from lane import roster_plan
    deploy = open("commands/lesson-8.4.sh").read().split("# ---- DEPLOY ----")[1].split("# ---- SMOKE ----")[0]
    env = dict(kv.split("=", 1) for kv in re.search(r'--set-env-vars="\^\|\^([^"]+)"', deploy).group(1).split("|"))
    print("documind-agent, as commands/lesson-8.4.sh deploys it:")
    print("  runs as", re.search(r"--service-account=([\w-]+)@", deploy).group(1), " model", env["AGENT_MODEL"], " knows one URL: MCP_URL")
    print("  who may call it:", ", ".join(re.search(r"for sa in ([\w\- ]+); do", deploy).group(1).split()))
    mcp = open("commands/lesson-7.2.sh").read()
    print("  documind-agent-sa may call documind-mcp:", "documind-agent-sa" in re.search(r"for who in ([\w\- ]+); do", mcp).group(1))
    roles = re.search(r"agent_roles = \[(.*?)\]", open("terraform/sa.tf").read(), re.S).group(1)
    print("  its project roles:", ", ".join(re.findall(r'"roles/([\w.]+)"', roles)))
    tenants = [t for t, e in roster_plan("PROJECT", "acme", [])[0] if e.startswith("documind-agent-sa@")]
    print("  the rosters it is on:", ", ".join(tenants))
    tree = ast.parse(open("services/agent/agent.py").read())
    mods = sorted({(n.module or "").split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
                  | {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
    print("  agent.py imports:", ", ".join(m for m in mods if m))
    print("  the image copies:", ", ".join(l.split()[-2] for l in open("services/agent/Dockerfile") if l.startswith("COPY")))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
