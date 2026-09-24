"""Lesson 7.2: demo 03 judge and disagreements

Prepare the judge, run it on lane answers and compare disagreements/trajectory judgments.

Run order inside this file:
1. Do it: the judge's venv and its self-test (source window 31)
2. Do it: the judge on your lane (source window 33)
3. Where the gate and the judge disagree: read the row (source window 35)
4. The judge's other two modes: trajectories now, pairwise in lesson 7.3 (source window 38)

Prerequisites: demo_02_live_gate_and_report.
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


# Original CLI workflow for step_01_the_judge_s_venv_and_its_self_test.
COMMANDS_01 = """python -m venv "$HOME/judge-venv"            # its own venv: the SDK is a major version ahead of the kit's
"$HOME/judge-venv/bin/python" -m pip install -q "google-cloud-aiplatform[evaluation]==2.1.0" pandas google-cloud-firestore
"$HOME/judge-venv/bin/python" evals/judge.py --selftest

"""

def step_01_the_judge_s_venv_and_its_self_test(session):
    """Run Do it: the judge's venv and its self-test at this checkpoint.

    Do it: the judge's venv and its self-test

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_judge_on_your_lane.
COMMANDS_02 = """mkdir -p evals/reports
make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" JUDGE_ARGS="--reuse evals/reports/judge72.json"

"""

def step_02_the_judge_on_your_lane(session):
    """Run Do it: the judge on your lane at this checkpoint.

    --reuse keeps the collected answers in a file. If the Evaluation step stops, the rerun judges the same answers without asking the lane again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_where_the_gate_and_the_judge_disagree_read(session):
    """Run Where the gate and the judge disagree: read the row at this checkpoint.

    Four ways the two can meet, and the gate's misses read against the judge's answers. judge.py prints its summary and writes no per-row ratings, so "read the row" means reading the answers. The cell takes each row the gate failed and prints what the judge's own collection received for it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads both files; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, sys; sys.path.insert(0, "evals")
    from run_eval import contains
    gate = json.load(open("evals/reports/lesson72.json", encoding="utf-8"))["records"]
    judged = {x["id"]: x for x in json.load(open("evals/reports/judge72.json", encoding="utf-8"))}
    missed = [x for x in gate if not x["pass"]]
    print(f"{len(missed)} row(s) cost the gate a point. The judge's own run answered them:")
    for x in missed:
        j = judged.get(x["id"], {})
        figs = [f"{w} {'present' if contains(j.get('response', ''), w) else 'absent'}" for w in j.get("must_contain", [])]
        print(f"  {x['id']:6} gate: {x['why'] or x['outcome']}")
        print(f"         judge's answer: {j.get('response', '')[:80]!r}, {len(j.get('cited') or [])} cited")
        print(f"         {'; '.join(figs) or 'a refusal row: no figure to look for'}")

# Original CLI workflow for step_04_the_judge_s_other_two_modes_trajectories_n.
COMMANDS_04 = """CHAT_URL="$(gcloud run services describe documind-chat --region "$REGION" --project "$PROJECT" --format='value(status.url)' 2>/dev/null)"
if [ -n "$CHAT_URL" ]; then
  make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" CHAT_URL="$CHAT_URL" \\
    JUDGE_ARGS="--reuse evals/reports/judge72.json --no-vertex --trajectory-rows 3" | grep -E "reused|trajectory"
else echo "no documind-chat service on this lane: trajectories need one"; fi

"""

def step_04_the_judge_s_other_two_modes_trajectories_n(session):
    """Run The judge's other two modes: trajectories now, pairwise in lesson 7.3 at this checkpoint.

    The chat service's tool calls against the one grounded path, and why the pairwise judge needs a candidate. With CHAT_URL, the judge sends a few answerable acme rows to each of the chat service's three brains, langchain, langgraph and adk. It compares the tool calls each brain returns with the reference path: one retrieve, then the answer. The three matches are computed in judge.py: exact, in order and any order. A brain that answers without retrieving scores 0 on all three, whatever its answer says. --no-vertex skips the Evaluation service, and --reuse skips asking the API again, so this costs only the chat turns.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_31', step_01_the_judge_s_venv_and_its_self_test),
        ('source_33', step_02_the_judge_on_your_lane),
        ('source_35', step_03_where_the_gate_and_the_judge_disagree_read),
        ('source_38', step_04_the_judge_s_other_two_modes_trajectories_n),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
