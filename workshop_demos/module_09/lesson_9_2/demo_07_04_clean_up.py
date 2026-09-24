"""Lesson 9.2 / s7: The corpus comes back: version 1, and the old answer with it

Summary and purpose:
Clean up

HTML instruction: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_03_every_row_of_the_walk
Expected observation: Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-00041-kqz      (the live revision, as before; no candidate tag)
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \\
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  deleted acme's cache

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html#L666

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate
rm -f .candidate-revision      # make promote would otherwise flip traffic to the recorded revision
make cache PROJECT="$PROJECT" TENANT=acme CACHE_OP=delete
"""


def demonstrate(session):
    """Run Clean up at this checkpoint.

    Clean up

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted).
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
