"""Lesson 15.2: repair graph baseline

Explicit recovery: repair graph baseline

Run order inside this file:
1. Do it (source window 25)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars GRAPH_SEED_DISTANCE=0.45 --quiet     # your number from step 5, not this one
ask152 "$CAND"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Notice what the first answer says, too. Dense retrieval found FIN-02 without any graph, because the handbook is small and the clause says "purchase". The Spanner walk made sure FIN-02 was in the pool whatever the dense ranking did. On a corpus where the answer's words are far from the question's, that is the difference. Set the threshold on the candidate alone, from your own numbers, and ask again. make candidate cannot pass it (step 7 says why), so this is a gcloud line:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run only if step 5 seeded nothing (the threshold, on the candidate alone).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_25', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
