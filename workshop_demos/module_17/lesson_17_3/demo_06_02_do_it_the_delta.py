"""Lesson 17.3 / s6: The verdict and the delta

Summary and purpose:
The gates and the judge asked both revisions the same questions, so their usage rows are like for like. The cell prints make usage's model table, groups the rows by model, and prices the endpoint's rows at 1.5 times what they log.

HTML instruction: bash — run in the operator shell, in the kit (reads the last two hours of usage rows)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_verdict
Expected observation: by model and backend (what answered, through which door)
model                 model_backend          answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------------------------------
gemini-3.6-flash      vertex                     130    952849    28030    1.6395    139.36    2100   0.00
projects/NUMBER/loca  vertex                     130    970907    17751    0.2694     22.89    1000   0.00

  live        130 answers  Rs 1.0720 an answer
  candidate   130 answers  Rs 0.1761 an answer as logged, Rs 0.2641 as Google bills it
the rupee delta: the tuned endpoint costs Rs 0.8079 less an answer, Rs 808 per 1,000 answers
  (the usage rows alone say Rs 0.8959: they log the endpoint at its base's rate)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L726

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make usage PROJECT="$PROJECT" HOURS=2 | sed -n '/^by model and backend/,/^$/p'
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


def demonstrate(session):
    """Run Do it: the delta at this checkpoint.

    The gates and the judge asked both revisions the same questions, so their usage rows are like for like. The cell prints make usage's model table, groups the rows by model, and prices the endpoint's rows at 1.5 times what they log.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the last two hours of usage rows).
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
