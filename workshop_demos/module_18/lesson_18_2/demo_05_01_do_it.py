"""Lesson 18.2 / s5: The stand-in, deployed and smoke-tested

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a GPU service: it bills while an instance lives)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: >> stand-in: gemma3:4b will be served as documind-slm
gcloud run deploy documind-slm \\
  --source services/slm --region us-central1 --project documind-ai-YOUR-ID \\
  --gpu 1 --gpu-type nvidia-l4 --no-gpu-zonal-redundancy \\
  --cpu 8 --memory 32Gi \\
  --max-instances 1 --min-instances 0 --timeout 600 --concurrency 4 \\
  --no-allow-unauthenticated --labels slm-source=stock \\
  --startup-probe httpGet.path=/api/tags,httpGet.port=8080,initialDelaySeconds=10,periodSeconds=5,failureThreshold=30 --quiet
...
>> slm: https://documind-slm-NUMBER.us-central1.run.app (min-instances 0; make slm-off after every session anyway)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L584

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make deploy-slm PROJECT="$PROJECT" SLM_STOCK=gemma3:4b      # the first build pulls 3.3 GB into the image: minutes
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a GPU service: it bills while an instance lives).
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
