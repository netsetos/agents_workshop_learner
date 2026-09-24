"""Lesson 6.2: demo 03 model settings and failure

Inspect deployed model settings and the candidate failure that is not a refusal.

Run order inside this file:
1. Read the lane, Rs 0 (source window 32)
2. The code (source window 36)

Prerequisites: demo_02_refusals_and_model_call.
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


# Original CLI workflow for step_01_read_the_lane_rs_0.
COMMANDS_01 = """python commands/lane.py tenant-backend acme
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

def step_01_read_the_lane_rs_0(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    Read the lane, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (three reads).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_code.
COMMANDS_02 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars MAX_ANSWER_TOKENS=16 --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
curl -s -o /tmp/cand62.json -w "HTTP %{http_code}\\n" -X POST "$CAND/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}'; cat /tmp/cand62.json; echo
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="generation_truncated" OR jsonPayload.event="generation_unparsed")' \\
  --project "$PROJECT" --freshness 5m --limit 4 --format='value(timestamp,jsonPayload.event,jsonPayload.max_output_tokens,jsonPayload.tokens_out,jsonPayload.finish_reason)'
gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate --remove-env-vars MAX_ANSWER_TOKENS --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
echo "template now: $(svc_env documind-api MAX_ANSWER_TOKENS)"; echo "(empty means unset: the default, 2048)"

"""

def step_02_the_code(session):
    """Run The code at this checkpoint.

    The code

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question that fails on purpose; one log read; the undo).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_32', step_01_read_the_lane_rs_0),
        ('source_36', step_02_the_code),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
