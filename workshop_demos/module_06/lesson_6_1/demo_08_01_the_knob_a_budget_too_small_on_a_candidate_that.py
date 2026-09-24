"""Lesson 6.1 / s8: What the budget costs, the knob on a candidate, and the lines this lesson leaves empty

Summary and purpose:
max_context_tokens is a setting, so the way to see the drop on the live corpus without touching the live service is a candidate revision, as in lessons 5.2 to 5.4: a budget of 600 tokens leaves room for about three handbook sections after the fixed prompt, so the same question at top_k 5 packs three, drops two, logs the drop, and answers from what it packed. The variable is not set on the live service, so the undo removes it and the default returns.

HTML instruction: bash — run in the operator shell (one new revision, no traffic; one question; one log read; then the undo)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_the_day_s_tokens_and_the_retries_there_wer
Expected observation: candidate: tokens_in 6xx | citations 2 | answerable True | pool 20
2026-09-2xT1x:xx:xx.xxxxxxZ	3	2
template now:
(empty means unset: the default, 8000)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L797

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars MAX_CONTEXT_TOKENS=600 --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
curl -s -X POST "$CAND/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":5}' \\
  | python -c "import sys, json; j = json.load(sys.stdin); print('candidate: tokens_in', j['tokens_in'], '| citations', len(j['citations']), '| answerable', j['answerable'], '| pool', j['stages']['pool'])"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="context_budget_drop"' \\
  --project "$PROJECT" --freshness 5m --limit 2 --format='value(timestamp,jsonPayload.packed,jsonPayload.dropped)'
gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate --remove-env-vars MAX_CONTEXT_TOKENS --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
echo "template now: ${MAX_CONTEXT_TOKENS:-$(svc_env documind-api MAX_CONTEXT_TOKENS)}"; echo "(empty means unset: the default, 8000)"
"""


def demonstrate(session):
    """Run The knob: a budget too small, on a candidate that takes no traffic at this checkpoint.

    max_context_tokens is a setting, so the way to see the drop on the live corpus without touching the live service is a candidate revision, as in lessons 5.2 to 5.4: a budget of 600 tokens leaves room for about three handbook sections after the fixed prompt, so the same question at top_k 5 packs three, drops two, logs the drop, and answers from what it packed. The variable is not set on the live service, so the undo removes it and the default returns.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question; one log read; then the undo).
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
