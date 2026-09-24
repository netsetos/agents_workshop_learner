"""Lesson 7.3 / s6: The rupee delta, from the usage rows

Summary and purpose:
Every answer of the last hour, grouped by the model that gave it, and the difference per answer. The API priced every answer on its usage row with cost.price(), at the rates of the model that answered. The gate's runs and the judge's collections asked both revisions the same questions, so the two groups are like for like. The cell groups the last hour's rows by model and divides.

HTML instruction: bash — run in the operator shell, in the kit (the last hour of usage rows, by model)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: gemini-3.6-flash          ... answers  Rs ...  Rs ... an answer
  gemini-3.1-flash-lite     ... answers  Rs ...  Rs ... an answer
  the candidate costs Rs ... less an answer: Rs ... per 1,000 answers

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html#L636

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run The rupee delta, from the usage rows at this checkpoint.

    Every answer of the last hour, grouped by the model that gave it, and the difference per answer. The API priced every answer on its usage row with cost.price(), at the rates of the model that answered. The gate's runs and the judge's collections asked both revisions the same questions, so the two groups are like for like. The cell groups the last hour's rows by model and divides.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the last hour of usage rows, by model).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys; sys.path.insert(0, "evals")
    from usage_rows import read_rows, group
    per = {g["model"]: g for g in group(read_rows(os.environ["PROJECT"], 1), ("model",))}
    for m, g in per.items():
        print(f"  {m:24} {g['answers']:4} answers  Rs {g['inr']:7.2f}  Rs {g['inr'] / g['answers']:.4f} an answer")
    live, cand = per.get("gemini-3.6-flash"), per.get("gemini-3.1-flash-lite")
    if live and cand:
        d = live["inr"] / live["answers"] - cand["inr"] / cand["answers"]
        print(f"  the candidate costs Rs {d:.4f} less an answer: Rs {d * 1000:,.0f} per 1,000 answers")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
