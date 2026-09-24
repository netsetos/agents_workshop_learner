"""Lesson 6.2 / s7: The model as a setting: the global client, a tuned endpoint, a pin and a router

Summary and purpose:
Read the lane, Rs 0

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (three reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_same_call_from_the_shell
Expected observation: acme: retrieval_backend=vector
acme's tenant_settings: {'generator_model': None, 'model_backend': None, 'retrieval_backend': 'vector', 'data_region': 'any'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L811

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python commands/lane.py tenant-backend acme
python - <<'PY'
import os, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
ts = firestore.Client(project=os.environ["PROJECT"]).collection("tenant_settings").document("acme").get().to_dict() or {}
print("acme's tenant_settings:", {k: ts.get(k) for k in ("generator_model", "model_backend", "retrieval_backend", "data_region")})
PY
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="tier_exhausted" OR jsonPayload.event="routing_fallback")' \\
  --project "$PROJECT" --freshness 7d --limit 3 --format='value(timestamp,jsonPayload.event,jsonPayload.model,jsonPayload.fallback)'
"""


def demonstrate(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    Read the lane, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (three reads).
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
