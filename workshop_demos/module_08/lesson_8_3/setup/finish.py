"""Lesson 8.3: finish

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

Run order inside this file:
1. Clean up: withdraw the note (source window 31)
2. Which store answers acme? Pin it to the kit's own index for this lesson (source window 5)

Prerequisites: workshop setup; see this lesson README.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_clean_up_withdraw_the_note.
COMMANDS_01 = """make retire PROJECT="$PROJECT" SOURCE=acme/lesson83_vendor_note.md

"""

def step_01_clean_up_withdraw_the_note(session):
    """Run Clean up: withdraw the note at this checkpoint.

    The note came from you, and it should not stay in acme's corpus. make retire flags its chunks, which leave retrieval, and marks its ledger row WITHDRAWN; the object stays in the uploads bucket. Look at what stays. The findings record stays in dlp_findings until someone deletes it. The two audit events stay for five years, whatever anyone wants, which is what retention means. The withdrawal writes no audit event of its own: doc.delete is a registered action, and nothing in the kit emits it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the note withdrawn from the index).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_which_store_answers_acme_pin_it_to_the_kit(session):
    """Run Which store answers acme? Pin it to the kit's own index for this lesson at this checkpoint.

    DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell when you finish the lesson, not now.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.restore_backend()

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_31', step_01_clean_up_withdraw_the_note),
        ('source_5', step_02_which_store_answers_acme_pin_it_to_the_kit),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=True)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
