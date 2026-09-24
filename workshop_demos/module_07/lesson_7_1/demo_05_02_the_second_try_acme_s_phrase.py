"""Lesson 7.1 / s5: An isolation row: the marker that cannot work, the list it must join, and the gate green again

Summary and purpose:
The second try: ACME's phrase

HTML instruction: bash — run in the operator shell, in the kit (the same row with ACME's phrase as the marker, then the build and the gate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_the_first_try_the_obvious_marker
Expected observation: 67 rows in GOLDEN; the last is iso-11
golden.jsonl
  rows : 67
  shape: isolation=12, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta
  every must_contain / must_retrieve verified against corpus/  OK
wrote 67 rows -> /home/you/deploy_module_rag/evals/golden.jsonl
== eval gate: OFFLINE (no credentials, no cost) ==
  67 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [FAIL] coverage
         iso-11: a isolation row that required.json does not list

  1 problem(s). The golden set cannot judge the model until it judges itself.
exit code 1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L700

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
from pathlib import Path
p = Path("evals/build_golden.py")
row = '    R("iso-11", "isolation", "How many days of earned leave are encashed on exit?", "zeta", ["20 days"], ["LV-07", "hr_policy_zeta_2026"], True, "Lesson 7.1. ACME caps encashment at 45 days, and 45 days is also in SEC-09 of this handbook, so the marker is the phrase only ACME holds.", ["capped at 45 days"]),'
lines = [l for l in p.read_text(encoding="utf-8").split("\\n") if not l.startswith('    R("iso-11",')]
lines.insert(lines.index("]", lines.index("GOLDEN = [")), row)            # before the bracket that closes GOLDEN
p.write_text("\\n".join(lines), encoding="utf-8", newline="\\n")
print(sum(l.startswith('    R("') for l in lines), "rows in GOLDEN; the last is iso-11")
PY
python evals/build_golden.py | sed -n '1,5p;$p'
python evals/run_eval.py; echo "exit code $?"
"""


def demonstrate(session):
    """Run The second try: ACME's phrase at this checkpoint.

    The second try: ACME's phrase

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same row with ACME's phrase as the marker, then the build and the gate).
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
