"""Lesson 7.1 / s4: A lookup row: written into build_golden.py, built, and judged

Summary and purpose:
The cell removes any earlier lk-32 line and inserts the row before the bracket that closes GOLDEN, so running it twice is harmless. The builder prints its first five lines and its last. make eval runs exactly the gate's line; calling it directly puts the exit code on a line of its own.

HTML instruction: bash — run in the operator shell, in the kit (one line into evals/build_golden.py, then the build and the gate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_the_gate_the_rows_that_cite_the_handbook_a
Expected observation: 66 rows in GOLDEN; the last is lk-32
golden.jsonl
  rows : 66
  shape: isolation=11, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta
  every must_contain / must_retrieve verified against corpus/  OK
wrote 66 rows -> /home/you/deploy_module_rag/evals/golden.jsonl
== eval gate: OFFLINE (no credentials, no cost) ==
  66 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
exit code 0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L546

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
from pathlib import Path
p = Path("evals/build_golden.py")
row = '    R("lk-32", "lookup", "How long can an account go unused before it is disabled?", "acme", ["45 days"], ["SEC-09", "hr_policy_2026"], True, "Lesson 7.1. SEC-09 was the one clause of the handbook no row asked about. Zeta holds the same clause, so the row is a lookup and never an isolation row."),'
lines = [l for l in p.read_text(encoding="utf-8").split("\\n") if not l.startswith('    R("lk-32",')]
lines.insert(lines.index("]", lines.index("GOLDEN = [")), row)            # before the bracket that closes GOLDEN
p.write_text("\\n".join(lines), encoding="utf-8", newline="\\n")
print(sum(l.startswith('    R("') for l in lines), "rows in GOLDEN; the last is lk-32")
PY
python evals/build_golden.py | sed -n '1,5p;$p'
python evals/run_eval.py; echo "exit code $?"
"""


def demonstrate(session):
    """Run Do it: add the row, build, gate at this checkpoint.

    The cell removes any earlier lk-32 line and inserts the row before the bracket that closes GOLDEN, so running it twice is harmless. The builder prints its first five lines and its last. make eval runs exactly the gate's line; calling it directly puts the exit code on a line of its own.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one line into evals/build_golden.py, then the build and the gate).
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
