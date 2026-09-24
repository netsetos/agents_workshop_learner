"""Lesson 6.1 / s7: The answer's reserve, the retry, and the tokens on the rows

Summary and purpose:
Do it: the day's tokens, and the retries there were not

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: two log reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_dated_revision_in_the_stream_read_revi
Expected observation: by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
acme                        NN     xxxxx     xxxx    0.0xxx      x.xx    4xxx   0.0x
2026-09-2xT1x:xx:xx.xxxxxxZ	context_budget_drop		1x	x

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L768

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make usage PROJECT=$PROJECT HOURS=24 | sed -n '/^by tenant/,/^$/p'
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="generation_truncated" OR jsonPayload.event="context_budget_drop")' \\
  --project "$PROJECT" --freshness 24h --limit 5 --format='value(timestamp,jsonPayload.event,jsonPayload.tokens_out,jsonPayload.packed,jsonPayload.dropped)'
"""


def demonstrate(session):
    """Run Do it: the day's tokens, and the retries there were not at this checkpoint.

    Do it: the day's tokens, and the retries there were not

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: two log reads).
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
