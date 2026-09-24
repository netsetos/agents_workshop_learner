"""Lesson 17.3: demo 03 verdict and cost delta

Read the quality verdict and measured cost delta before removing the candidate.

Run order inside this file:
1. Do it: the verdict (source window 21)
2. Do it: the delta (source window 23)

Prerequisites: demo_02_paired_evaluation.
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


# Original CLI workflow for step_01_the_verdict.
COMMANDS_01 = """make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" API_B="$CAND"

"""

def step_01_the_verdict(session):
    """Run Do it: the verdict at this checkpoint.

    Do it: the verdict

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the judge's venv from lesson 7.2: 65 answers from each revision, then Vertex AI Evaluation).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_delta.
COMMANDS_02 = """make usage PROJECT="$PROJECT" HOURS=2 | sed -n '/^by model and backend/,/^$/p'
python - <<'PY'
import os, sys
sys.path.insert(0, "evals")
from usage_rows import group, read_rows
EP, TUNED = os.environ["ENDPOINT"], 1.5      # Google's pricing page: a tuned Gemini 3 endpoint answers at 1.5 x its base
per = {g["model"]: g for g in group(read_rows(os.environ["PROJECT"], 2), ("model",))}
live, cand = per["gemini-3.6-flash"], per[EP]
a, logged = live["inr"] / live["answers"], cand["inr"] / cand["answers"]
print(f"  live       {live['answers']:4} answers  Rs {a:.4f} an answer")
print(f"  candidate  {cand['answers']:4} answers  Rs {logged:.4f} an answer as logged, Rs {logged * TUNED:.4f} as Google bills it")
d = a - logged * TUNED
print(f"the rupee delta: the tuned endpoint costs Rs {d:.4f} less an answer, Rs {d * 1000:,.0f} per 1,000 answers")
print(f"  (the usage rows alone say Rs {a - logged:.4f}: they log the endpoint at its base's rate)")
PY

"""

def step_02_the_delta(session):
    """Run Do it: the delta at this checkpoint.

    The gates and the judge asked both revisions the same questions, so their usage rows are like for like. The cell prints make usage's model table, groups the rows by model, and prices the endpoint's rows at 1.5 times what they log.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the last two hours of usage rows).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_the_verdict),
        ('source_23', step_02_the_delta),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
