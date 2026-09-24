"""Lesson 9.3: finish

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

Run order inside this file:
1. Choosing the threshold, and the clean-up (source window 22)
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


# Original CLI workflow for step_01_choosing_the_threshold_and_the_clean_up.
COMMANDS_01 = """gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate
rm -f .candidate-revision      # make promote would otherwise flip traffic to the recorded revision

"""

def step_01_choosing_the_threshold_and_the_clean_up(session):
    """Run Choosing the threshold, and the clean-up at this checkpoint.

    What the numbers allow, where the threshold lives, and the candidate put away. The kit's rule is the lowest candidate with no false hit on the set, and your curve names it. Before moving the switch, weigh three things. First, the rule of three: 18 different pairs with no false hit still allow a true rate of about 17%. The honest next step is more different pairs, written from real questions one word away, not a lower threshold. Second, the saving at that threshold: if it hits only a few same-fact pairs, the exact rung (the same words, no threshold at all) may be most of what the cache is worth. Third, the replay's hit from lines, which the curve cannot see. The threshold is an environment variable, SEMANTIC_CACHE_THRESHOLD, read once when a revision starts. No make target passes it, so trying 0.97 on a candidate takes gcloud run services update documind-api --no-traffic --tag candidate --update-env-vars SEMANTIC_CACHE_THRESHOLD=0.97, with your region and project, and then the replay again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed).
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
        ('source_22', step_01_choosing_the_threshold_and_the_clean_up),
        ('source_5', step_02_which_store_answers_acme_pin_it_to_the_kit),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=True)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
