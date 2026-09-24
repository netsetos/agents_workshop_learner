"""Lesson 7.1 / s5: An isolation row: the marker that cannot work, the list it must join, and the gate green again

Summary and purpose:
The third try: listed, and the gate green

HTML instruction: bash — run in the operator shell, in the kit (iso-11 listed in evals/required.json, then make eval)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_the_second_try_acme_s_phrase
Expected observation: 16 required ids: iso-01 iso-02 iso-03 iso-04 iso-05 iso-06 iso-07 iso-08 iso-09 iso-10 iso-11 mm-01 mm-02 mm-03 mm-04 vr-01
python evals/run_eval.py
== eval gate: OFFLINE (no credentials, no cost) ==
  67 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
exit code 0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L733

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import json
from pathlib import Path
p = Path("evals/required.json")
d = json.loads(p.read_text(encoding="utf-8"))
d["ids"] = sorted(set(d["ids"]) | {"iso-11"})
p.write_text(json.dumps(d, indent=1), encoding="utf-8", newline="\\n")
print(len(d["ids"]), "required ids:", " ".join(d["ids"]))
PY
make eval; echo "exit code $?"
"""


def demonstrate(session):
    """Run The third try: listed, and the gate green at this checkpoint.

    The third try: listed, and the gate green

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (iso-11 listed in evals/required.json, then make eval).
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
