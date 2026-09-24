"""Lesson 3.2 / s4: Count pages first: slices, and the 250-page line

Summary and purpose:
The amendment Act is four pages and globex does not hold it, so ingesting it there is a fresh source, one Document AI request, and a few paise. Then read the worker's line for it, which carries the page count as pages.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (costs about four pages of Document AI)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_count_the_corpus_rs_0
Expected observation: globex_e7a1c0...    4    5    5

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L510

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make ingest-one PROJECT=$PROJECT TENANT=globex FILE=evals/corpus/acme/maternity_benefit_amendment_act_2017.pdf

gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" AND jsonPayload.event="ingest_ok" AND jsonPayload.tenant="globex"' \\
  --project "$PROJECT" --limit 1 --format='value(jsonPayload.doc_key,jsonPayload.pages,jsonPayload.chunks,jsonPayload.embedded)'
"""


def demonstrate(session):
    """Run Prove it on the lane: one small PDF, four pages at this checkpoint.

    The amendment Act is four pages and globex does not hold it, so ingesting it there is a fresh source, one Document AI request, and a few paise. Then read the worker's line for it, which carries the page count as pages.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (costs about four pages of Document AI).
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
