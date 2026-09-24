"""Lesson 12.3: demo 01 peer contract and deployment

Inspect the implemented A2A peer and deploy/read its advertised contract.

Run order inside this file:
1. Do it (source window 10)
2. Do it (source window 12)

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

# Original CLI workflow for step_02_example.
COMMANDS_02 = """export AGENT="https://documind-agent-$NUMBER.$REGION.run.app" SINCE123="$(date -u +%FT%TZ)"
curl -s -o /dev/null -w "the card without a token: HTTP %{http_code}\\n" "$AGENT/.well-known/agent-card.json"
curl -s -H "Authorization: Bearer $(tok "$AGENT")" "$AGENT/.well-known/agent-card.json" > /tmp/card123.json
python - <<'PY'
import json
card = json.load(open("/tmp/card123.json"))
iface = (card.get("supportedInterfaces") or [{}])[0]
print(f"the card with a token: {card['name']}, version {card['version']}")
print(f"  answers at {iface.get('url')} over {iface.get('protocolBinding')}, A2A {iface.get('protocolVersion')}")
print(f"  streaming {card['capabilities'].get('streaming')}, input {card['defaultInputModes']}, output {card['defaultOutputModes']}")
print("  skills:", ", ".join(s["name"] for s in card["skills"]))
PY

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the card, without a token and with one).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_example),
        ('source_12', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
