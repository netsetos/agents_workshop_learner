"""Lesson 7.1 / s5: An isolation row: the marker that cannot work, the list it must join, and the gate green again

Summary and purpose:
The first try: the obvious marker

HTML instruction: bash — run in the operator shell, in the kit (the isolation row, with the obvious marker)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_what_the_gate_catches_and_the_one_mistake_it_can
Expected observation: 67 rows in GOLDEN; the last is iso-11
golden.jsonl
  rows : 67
  shape: isolation=12, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta

  ASSERTIONS THAT DO NOT MATCH THE CORPUS:
   ! iso-11: must_not_contain '45 days' is in zeta's OWN corpus - answering it correctly would fail the row
exit code 1
66

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L675

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
from pathlib import Path
p = Path("evals/build_golden.py")
row = '    R("iso-11", "isolation", "How many days of earned leave are encashed on exit?", "zeta", ["20 days"], ["LV-07", "hr_policy_zeta_2026"], True, "Lesson 7.1. The same question, a different answer per tenant: ACME caps encashment at 45 days.", ["45 days"]),'
lines = [l for l in p.read_text(encoding="utf-8").split("\\n") if not l.startswith('    R("iso-11",')]
lines.insert(lines.index("]", lines.index("GOLDEN = [")), row)            # before the bracket that closes GOLDEN
p.write_text("\\n".join(lines), encoding="utf-8", newline="\\n")
print(sum(l.startswith('    R("') for l in lines), "rows in GOLDEN; the last is iso-11")
PY
python evals/build_golden.py; echo "exit code $?"; wc -l < evals/golden.jsonl
"""


def demonstrate(session):
    """Run The first try: the obvious marker at this checkpoint.

    The first try: the obvious marker

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the isolation row, with the obvious marker).
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
