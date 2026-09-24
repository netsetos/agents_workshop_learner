"""Lesson 6.2 / s8: What an answer costs, and the failure that is not a refusal

Summary and purpose:
The code

HTML instruction: bash — run in the operator shell (one new revision, no traffic; one question that fails on purpose; one log read; the undo)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_read_the_lane_rs_0
Expected observation: HTTP 502
{"detail":"generation produced no parseable answer (MAX_TOKENS)"}
2026-09-2xT1x:xx:xx.xxxxxxZ	generation_unparsed			MAX_TOKENS
2026-09-2xT1x:xx:xx.xxxxxxZ	generation_truncated	16	1x
template now:
(empty means unset: the default, 2048)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L869

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
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


def demonstrate(session):
    """Run The code at this checkpoint.

    The code

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question that fails on purpose; one log read; the undo).
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
