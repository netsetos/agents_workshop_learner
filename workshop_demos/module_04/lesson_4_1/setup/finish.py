"""Lesson 4.1: finish

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

Run order inside this file:
1. Decide, then clean up (source window 36)
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


def step_01_decide_then_clean_up(session):
    """Run Decide, then clean up at this checkpoint.

    This dead letter deserves the second choice: the object was never meant to be indexed. Acknowledge the message to remove it from the queue, and delete the empty object from the bucket, because an object with no ledger row is exactly what the nightly walk of lesson 4.4 looks for, and it would rewrite the object onto itself and send the same poison round again every night. Both commands change your lane; both act only on the drill's own artefacts.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (removes the dead letter and the empty object; nothing else).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.poison import finish_drill
    finish_drill(session)

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
        ('source_36', step_01_decide_then_clean_up),
        ('source_5', step_02_which_store_answers_acme_pin_it_to_the_kit),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=True)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
