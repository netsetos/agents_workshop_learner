"""Lesson 7.1: demo 01 lookup row and gate

Inspect the golden set, add a lookup row and test the real falsifiability gate.

Run order inside this file:
1. Do it: the gate, the rows that cite the handbook, and the handbook's clauses (source window 10)
2. Do it: the gate, the rows that cite the handbook, and the handbook's clauses (source window 12)
3. Do it: add the row, build, gate (source window 16)
4. What the gate catches, and the one mistake it cannot see (source window 18)

Prerequisites: setup_prepare.
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


def step_01_the_gate_the_rows_that_cite_the_handbook_a(session):
    """Run Do it: the gate, the rows that cite the handbook, and the handbook's clauses at this checkpoint.

    The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the offline gate, then the rows that cite the handbook).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.steps import backup_files
    backup_files(session, ["evals/build_golden.py", "evals/golden.jsonl", "evals/required.json", "evals/paraphrases.jsonl"])
    session.shell("make eval\npython evals/run_eval.py --source hr_policy_2026.md | sed -n '/rows citing/,$p'")

def step_02_the_gate_the_rows_that_cite_the_handbook_a(session):
    """Run Do it: the gate, the rows that cite the handbook, and the handbook's clauses at this checkpoint.

    The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3. Ten rows cite the handbook, by --source. Now count by clause. The cell reads the handbook's sections and lists, for each clause that is not filler, the ACME rows that anchor on it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the handbook and golden.jsonl; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, re
    text = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    heads = re.findall(r"(?m)^## (\S+) \S (.+)$", text)
    rows = [json.loads(l) for l in open("evals/golden.jsonl", encoding="utf-8") if l.strip()]
    real = [(code, name) for code, name in heads if not code.startswith("GEN-")]
    print(f"hr_policy_2026.md: {len(heads)} sections, {len(heads) - len(real)} of them GEN- filler")
    for code, name in real:
        ids = [r["id"] for r in rows if r["tenant"] == "acme" and code in r["must_retrieve"]]
        print(f"  {code:10} {name:24} {' '.join(ids) or '<- no golden row asks about this clause'}")

# Original CLI workflow for step_03_add_the_row_build_gate.
COMMANDS_03 = """python - <<'PY'
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

def step_03_add_the_row_build_gate(session):
    """Run Do it: add the row, build, gate at this checkpoint.

    The cell removes any earlier lk-32 line and inserts the row before the bracket that closes GOLDEN, so running it twice is harmless. The builder prints its first five lines and its last. make eval runs exactly the gate's line; calling it directly puts the exit code on a line of its own.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one line into evals/build_golden.py, then the build and the gate).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def step_04_what_the_gate_catches_and_the_one_mistake(session):
    """Run What the gate catches, and the one mistake it cannot see at this checkpoint.

    The next cell judges six versions of the row in memory, with the gate's own two functions. It writes nothing.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (six versions of the row, judged in memory; writes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys; sys.path.insert(0, "evals")
    from run_eval import load_corpus, check_falsifiable, check_anchors
    corpus = load_corpus()
    row = {"id": "lk-32", "shape": "lookup", "tenant": "acme", "must_contain": ["45 days"],
           "must_retrieve": ["SEC-09", "hr_policy_2026"], "answerable": True}
    for name, change in [("as written", {}),
                         ("a figure the clause never gives", {"must_contain": ["45 working days"]}),
                         ("words the file breaks across two lines", {"must_contain": ["disabled automatically"]}),
                         ("a clause code with a typo", {"must_retrieve": ["SEC-9", "hr_policy_2026"]}),
                         ("nothing the answer must contain", {"must_contain": []}),
                         ("another clause's figure", {"must_contain": ["60 days"]})]:
        found = check_falsifiable([{**row, **change}], corpus) + check_anchors([{**row, **change}], corpus)
        print(f"{name:40} {'REFUSED' if found else 'accepted'}")
        for f in found:
            print("   ", f)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_10', step_01_the_gate_the_rows_that_cite_the_handbook_a),
        ('source_12', step_02_the_gate_the_rows_that_cite_the_handbook_a),
        ('source_16', step_03_add_the_row_build_gate),
        ('source_18', step_04_what_the_gate_catches_and_the_one_mistake),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
