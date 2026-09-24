"""Lesson 17.3: demo 02 paired evaluation

Run the same questions on the baseline/candidate and inspect row-level results.

Run order inside this file:
1. Do it (source window 16)
2. Do it (source window 18)

Prerequisites: demo_01_clean_baseline_and_candidate.
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
COMMANDS_01 = """make eval-live PROJECT="$PROJECT" REPORT="$HOME/base173.json" | tail -3
make eval-live PROJECT="$PROJECT" API="$CAND" REPORT="$HOME/cand173.json"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every golden row, on each revision: about twenty minutes).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the two reports).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    base, cand = (json.load(open(os.path.expanduser(f"~/{n}173.json"), encoding="utf-8")) for n in ("base", "cand"))
    print(f"  {'':21} {'live':>7} {'candidate':>10}  {'needs':>5}")
    for k in base["scores"]:
        if k in base["judged"] or k in cand["judged"]:
            flag = "  FAIL" if k in cand["failed"] else ""
            print(f"  {k:21} {base['scores'][k]:7.1%} {cand['scores'][k]:10.1%}  {base['thresholds'][k]:5.0%}{flag}")
    was = {r["id"]: r["pass"] for r in base["records"]}
    moved = [r for r in cand["records"] if was.get(r["id"]) != r["pass"]]
    for r in moved:
        print(f"  {r['id']}: {'pass' if was.get(r['id']) else 'fail'} on live, {'pass' if r['pass'] else 'fail'} on the candidate ({r['why'] or r['outcome']})")
    med = lambda rep: sorted(x["latency_ms"] for x in rep["records"])[len(rep["records"]) // 2]
    print(f"  {len(moved)} row(s) changed verdict; median round trip {med(base)} ms live, {med(cand)} ms candidate")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_16', step_01_example),
        ('source_18', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
