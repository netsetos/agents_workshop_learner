"""Lesson 7.1: demo 02 isolation row and live check

Try both isolation markers, fix the required-row set, then ask the new rows live.

Run order inside this file:
1. The first try: the obvious marker (source window 23)
2. The second try: ACME's phrase (source window 25)
3. The third try: listed, and the gate green (source window 27)
4. Do it (source window 31)

Prerequisites: demo_01_lookup_row_and_gate.
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


def step_01_the_first_try_the_obvious_marker(session):
    """Run The first try: the obvious marker at this checkpoint.

    The first try: the obvious marker

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the isolation row, with the obvious marker).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from pathlib import Path
    p = Path("evals/build_golden.py")
    row = '    R("iso-11", "isolation", "How many days of earned leave are encashed on exit?", "zeta", ["20 days"], ["LV-07", "hr_policy_zeta_2026"], True, "Lesson 7.1. The same question, a different answer per tenant: ACME caps encashment at 45 days.", ["45 days"]),'
    lines = [l for l in p.read_text(encoding="utf-8").split("\n") if not l.startswith('    R("iso-11",')]
    lines.insert(lines.index("]", lines.index("GOLDEN = [")), row)            # before the bracket that closes GOLDEN
    p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(sum(l.startswith('    R("') for l in lines), "rows in GOLDEN; the last is iso-11")
    import sys
    from workshop_helpers.gates import expect_failure
    expect_failure(session, [sys.executable, "evals/build_golden.py"], status=1, messages=["iso-11:", "OWN corpus"])
    print("Unchanged golden row count:", len(Path("evals/golden.jsonl").read_text().splitlines()))

def step_02_the_second_try_acme_s_phrase(session):
    """Run The second try: ACME's phrase at this checkpoint.

    The second try: ACME's phrase

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same row with ACME's phrase as the marker, then the build and the gate).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from pathlib import Path
    p = Path("evals/build_golden.py")
    row = '    R("iso-11", "isolation", "How many days of earned leave are encashed on exit?", "zeta", ["20 days"], ["LV-07", "hr_policy_zeta_2026"], True, "Lesson 7.1. ACME caps encashment at 45 days, and 45 days is also in SEC-09 of this handbook, so the marker is the phrase only ACME holds.", ["capped at 45 days"]),'
    lines = [l for l in p.read_text(encoding="utf-8").split("\n") if not l.startswith('    R("iso-11",')]
    lines.insert(lines.index("]", lines.index("GOLDEN = [")), row)            # before the bracket that closes GOLDEN
    p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(sum(l.startswith('    R("') for l in lines), "rows in GOLDEN; the last is iso-11")
    import sys
    from workshop_helpers.gates import expect_failure
    session.command([sys.executable, "evals/build_golden.py"])
    expect_failure(session, [sys.executable, "evals/run_eval.py"], status=1, messages=["iso-11:", "required.json does not list"])

# Original CLI workflow for step_03_the_third_try_listed_and_the_gate_green.
COMMANDS_03 = """python - <<'PY'
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

def step_03_the_third_try_listed_and_the_gate_green(session):
    """Run The third try: listed, and the gate green at this checkpoint.

    The third try: listed, and the gate green

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (iso-11 listed in evals/required.json, then make eval).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

# Original CLI workflow for step_04_example.
COMMANDS_04 = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask, contains, load_golden
api, rows = os.environ["API"], {r["id"]: r for r in load_golden()}
for rid in ("lk-32", "iso-11"):
    r = rows[rid]
    status, body, ms = ask(api, r["question"], r["tenant"], "eval@documind.in", os.environ["TOKEN"])
    answer, cites = body.get("answer", ""), body.get("citations") or []
    print(f"{rid} as {r['tenant']}: HTTP {status}, answerable {body.get('answerable')}, {len(cites)} citation(s), {ms} ms")
    print("   " + answer[:120])
    for w in r["must_contain"]:
        print(f"   must_contain {w!r}: {'found' if contains(answer, w) else 'MISSING'}")
    for w in r.get("must_not_contain", []):
        print(f"   must_not_contain {w!r}: {'LEAKED' if contains(answer, w) else 'absent'}")
    print("   cites " + ", ".join(sorted({c["source_uri"].split("/", 3)[-1] for c in cites})))
status, _, _ = ask(api, rows["iso-11"]["question"], "zeta", "outsider@not-a-tenant.invalid", os.environ["OUTSIDER"])
print(f"iso-11 asked by documind-outsider-sa: HTTP {status} (the isolation gate requires 403)")
PY

"""

def step_04_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three requests to the API; under a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_23', step_01_the_first_try_the_obvious_marker),
        ('source_25', step_02_the_second_try_acme_s_phrase),
        ('source_27', step_03_the_third_try_listed_and_the_gate_green),
        ('source_31', step_04_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
