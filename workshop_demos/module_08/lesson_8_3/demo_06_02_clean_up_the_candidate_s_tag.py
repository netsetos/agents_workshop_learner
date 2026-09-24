"""Lesson 8.3 / s6: Four questions to the candidate: plain, two injections, a PAN

Summary and purpose:
Clean up: the candidate's tag

HTML instruction: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_four_questions_to_the_candidate_plain_two_inject
Expected observation: Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-000MM-xxx      (the live revision, as before; no candidate tag)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html#L614

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate
rm -f .candidate-revision      # make promote would otherwise flip traffic to the recorded revision
"""


def demonstrate(session):
    """Run Clean up: the candidate's tag at this checkpoint.

    Clean up: the candidate's tag

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed).
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
