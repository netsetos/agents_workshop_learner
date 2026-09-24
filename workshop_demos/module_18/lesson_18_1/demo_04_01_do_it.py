"""Lesson 18.1 / s4: The token the proxy sends

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it
Expected observation: the SLM, first call       <token 1>   minted so far: 1
the SLM, a minute later   <token 1>   minted so far: 1
the SLM, 55 minutes in    <token 2>   minted so far: 2
the vLLM engine           <token 3>   minted so far: 3
the proxy drops these request headers, then adds its own Authorization: authorization, connection, content-length, host, transfer-encoding

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L538

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """cd services/litellm && python - <<'PY'
import ast, types
import google.oauth2.id_token
minted = []
google.oauth2.id_token.fetch_id_token = lambda request, audience: minted.append(audience) or f"<token {len(minted)}>"   # the metadata server, counted
import gcp_id_token as g
clock = [1_000_000.0]
g.time = types.SimpleNamespace(time=lambda: clock[0])                                  # a clock the cell can move
SLM, VLLM = "https://documind-slm-NUMBER.us-central1.run.app", "https://documind-vllm-NUMBER.us-central1.run.app/v1"
for label, audience, wait in (("the SLM, first call", SLM, 0), ("the SLM, a minute later", SLM, 60),
                              ("the SLM, 55 minutes in", SLM, 55 * 60 - 60), ("the vLLM engine", VLLM, 0)):
    clock[0] += wait
    print(f"{label:25} {g.get_id_token(audience)}   minted so far: {len(minted)}")
hop = ast.literal_eval(next(n.value for n in ast.parse(open("token_proxy.py", encoding="utf-8").read()).body
                            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "HOP"))
print("the proxy drops these request headers, then adds its own Authorization:", ", ".join(sorted(hop)))
PY
cd ../..
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
