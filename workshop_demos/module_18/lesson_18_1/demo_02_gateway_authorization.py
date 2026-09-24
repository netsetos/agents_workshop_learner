"""Lesson 18.1: demo 02 gateway authorization

Exercise the authenticated route and deployment checks.

Run order inside this file:
1. Do it (source window 14)
2. Do it (source window 17)
3. Do it (source window 19)

Prerequisites: demo_01_gateway_routes.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """cd services/litellm && python - <<'PY'
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

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """make deploy-gateway PROJECT="$PROJECT"            # builds the image from services/litellm: the first build takes a while

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_example.
COMMANDS_03 = """make smoke-gateway PROJECT="$PROJECT"

"""

def step_03_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_14', step_01_example),
        ('source_17', step_02_example),
        ('source_19', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
