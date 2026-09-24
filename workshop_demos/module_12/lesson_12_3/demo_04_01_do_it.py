"""Lesson 12.3 / s4: The card: refused without a token, read with one

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the card, without a token and with one)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: the card without a token: HTTP 403
the card with a token: documind_peer, version 0.0.1
  answers at https://documind-agent-NUMBER.asia-south1.run.app over JSONRPC, A2A 1.0
  streaming False, input ['text/plain'], output ['text/plain']
  skills: model

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html#L469

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export AGENT="https://documind-agent-$NUMBER.$REGION.run.app" SINCE123="$(date -u +%FT%TZ)"
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the card, without a token and with one).
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
