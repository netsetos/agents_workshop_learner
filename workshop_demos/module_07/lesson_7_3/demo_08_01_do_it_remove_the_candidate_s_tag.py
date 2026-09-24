"""Lesson 7.3 / s8: Deciding, the confounds that fake a result, and removing the candidate

Summary and purpose:
This ends the experiment. The candidate revision stays in the service's history with no traffic and no URL. Removing the tag is not enough on its own: make promote refuses only when the tag points at another revision, and otherwise flips traffic to the revision named in .candidate-revision. Deleting that file makes make promote stop with an error instead.

HTML instruction: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed; the live revision is untouched)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_the_rupee_delta_from_the_usage_rows
Expected observation: ...
the candidate URL now: HTTP 404

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html#L688

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate
rm -f .candidate-revision      # make promote flips to the revision this file names, tag or no tag
curl -s -o /dev/null -w "the candidate URL now: HTTP %{http_code}\\n" -H "Authorization: Bearer $(tok "$API")" "$CAND/health"
"""


def demonstrate(session):
    """Run Do it: remove the candidate's tag at this checkpoint.

    This ends the experiment. The candidate revision stays in the service's history with no traffic and no URL. Removing the tag is not enough on its own: make promote refuses only when the tag points at another revision, and otherwise flips traffic to the revision named in .candidate-revision. Deleting that file makes make promote stop with an error instead.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed; the live revision is untouched).
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
