"""Lesson 18.2 / s5: The stand-in, deployed and smoke-tested

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit, right after the deploy
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: DocuMind SLM - live smoke test
  target: https://documind-slm-NUMBER.us-central1.run.app
  --------------------------------------------------------
  [PASS] /api/tags lists documind-slm  HTTP 200 in 0.1s (cold start included): ['documind-slm:latest']
  [PASS] /api/generate answers  'OK' in 12.0s
  [PASS] /v1/chat/completions answers (the OpenAI-compatible door)  'OK' in 0.6s
  [PASS] through the gateway's documind-slm route  HTTP 200, served by 'ollama_chat/documind-slm' in 0.6s
  [PASS] what the service serves  stock	us-central1-docker.pkg.dev/documind-ai-YOUR-ID/cloud-run-source-deploy/documind-slm@sha256:DIGEST
  --------------------------------------------------------
  5 passed, 0 failed

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L597

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make smoke-slm PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit, right after the deploy.
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
