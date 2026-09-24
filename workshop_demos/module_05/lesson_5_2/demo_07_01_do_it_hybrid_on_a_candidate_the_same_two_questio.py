"""Lesson 5.2 / s7: The knob: hybrid on a candidate that takes no traffic, compared, then removed

Summary and purpose:
Do it: hybrid on a candidate, the same two questions to both revisions, then undo

HTML instruction: bash — run in the operator shell (one new revision, no traffic; two version reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_a_wiring_check_then_acme_s_rows_with_a_led
Expected observation: documind-api-NUMBER                  mode dense | backend vector
candidate---documind-api-NUMBER      mode hybrid | backend vector

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L794

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RETRIEVAL_MODE=hybrid --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
for U in "$API" "$CAND"; do
  curl -s "$U/version" -H "Authorization: Bearer $(tok "$API")" \\
    | python -c "import sys, json; j = json.load(sys.stdin); print('$U'.split('//')[1].split('.')[0].ljust(36), 'mode', j['retrieval_mode'], '| backend', j['retrieval_backend'])"
done
"""


def demonstrate(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; two version reads).
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
