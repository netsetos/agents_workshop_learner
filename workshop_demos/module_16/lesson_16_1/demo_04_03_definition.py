"""Lesson 16.1 / s4: The clip built, the transcript withdrawn, the video heard

Summary and purpose:
make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back. Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call:

HTML instruction: bash — run in the operator shell, in the kit (the video uploaded; waits for the worker)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_definition
Expected observation: ...
>> gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4 - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	acme_a85a89590f9a2b8b7ffc8588e11578297c5bc1fe5181482b0ef75d22d00881d3	5	0	5	0	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=townhall_2026_q1.mp4 API=<candidate url>

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html#L589

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/corpus/acme/townhall_2026_q1.mp4
"""


def demonstrate(session):
    """Run Definition at this checkpoint.

    make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back. Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the video uploaded; waits for the worker).
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
