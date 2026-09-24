"""Lesson 7.2: demo 02 live gate and report

Run the live gate, retain its actual exit code and inspect the row-level report.

Run order inside this file:
1. Do it: the live gate, with a report (source window 18)
2. Do it: the live gate, with a report (source window 20)
3. Do it: the live gate, with a report (source window 22)

Prerequisites: demo_01_offline_gate_and_ci.
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


def step_01_the_live_gate_with_a_report(session):
    """Run Do it: the live gate, with a report at this checkpoint.

    Do it: the live gate, with a report

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every row as the member, every isolation row as the outsider: about ten minutes).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.gates import live_gate
    live_gate(session, report="evals/reports/lesson72.json")

def step_02_the_live_gate_with_a_report(session):
    """Run Do it: the live gate, with a report at this checkpoint.

    Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the report; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json
    r = json.load(open("evals/reports/lesson72.json", encoding="utf-8"))
    gold = {g["id"]: g for g in map(json.loads, open("evals/golden.jsonl", encoding="utf-8"))}
    rec = r["records"]
    A = [x for x in rec if gold[x["id"]]["answerable"]]
    answered = [x for x in A if x["outcome"] == "ok" and x["answerable"]]
    contained = [x for x in answered if not x["why"].startswith("answered without")]
    U = [x for x in rec if not gold[x["id"]]["answerable"]]
    refused = [x for x in U if x["outcome"] == "ok" and not x["answerable"]]
    print(f"  answerable_rate    {len(answered):2} answered          of {len(A)} answerable rows")
    print(f"  must_contain_rate  {len(contained):2} with the figure   of {len(answered)} ANSWERED")
    print(f"  correct_rate       {sum(x['pass'] for x in A):2} right             of {len(A)} ANSWERABLE")
    print(f"  refusal_rate       {len(refused):2} refused           of {len(U)} unanswerable rows")
    for k, v in r["scores"].items():
        verdict = "FAIL" if k in r["failed"] else "pass" if k in r["judged"] else " -- "
        print(f"  {verdict}  {k:21} {v:6.1%}  (needs {r['thresholds'][k]:.0%})")
    print("  cost a point:", ", ".join(f"{x['id']} ({x['why'] or x['outcome']})" for x in rec if not x["pass"]) or "nothing")

# Original CLI workflow for step_03_the_live_gate_with_a_report.
COMMANDS_03 = """make usage PROJECT="$PROJECT" HOURS=1 | sed -n '1,8p'

"""

def step_03_the_live_gate_with_a_report(session):
    """Run Do it: the live gate, with a report at this checkpoint.

    Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point. Last, what the run cost. The API priced every answer on its usage row; make usage groups the last hour of those rows. Run it straight after the gate, before step 5 asks the lane again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the usage rows of the last hour, priced).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_18', step_01_the_live_gate_with_a_report),
        ('source_20', step_02_the_live_gate_with_a_report),
        ('source_22', step_03_the_live_gate_with_a_report),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
