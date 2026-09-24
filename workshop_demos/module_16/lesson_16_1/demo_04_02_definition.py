"""Lesson 16.1 / s4: The clip built, the transcript withdrawn, the video heard

Summary and purpose:
Next, the transcript goes. upload.sh keeps a transcript home once its video exists, as it keeps a PDF's text mirror home, but it removes nothing already sent: make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back.

HTML instruction: bash — run in the operator shell, in the kit (the transcript withdrawn from acme)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_definition
Expected observation: {"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.md", "fingerprint": "1a19e8a7d490616d", "retired_doc_keys": ["acme_b0d7702de2bf5a7d0770de433916af821b4a83f13ca321e074293ef99f4d75c1"], "retired_ids": ["acme:b0d7702de2bf5a7d0770de433916af821b4a83f13ca321e074293ef99f4d75c1#0"], "retired_chunks": 1, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html#L561

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make retire PROJECT="$PROJECT" SOURCE=acme/townhall_2026_q1.md
"""


def demonstrate(session):
    """Run Definition at this checkpoint.

    Next, the transcript goes. upload.sh keeps a transcript home once its video exists, as it keeps a PDF's text mirror home, but it removes nothing already sent: make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the transcript withdrawn from acme).
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
