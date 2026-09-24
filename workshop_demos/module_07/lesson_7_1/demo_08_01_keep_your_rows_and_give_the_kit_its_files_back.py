"""Lesson 7.1 / s8: What rows cost, how a golden set rots, and handing the kit back

Summary and purpose:
Your clone now differs from the kit in four files. Lesson 7.2 runs the kit's own set, 65 rows and 15 required ids. The setup block's git pull --ff-only also refuses to run over local edits to a file the kit has changed. So keep your rows as a patch and restore the four files. git -C "$DEMO_ROOT" apply "$HOME/lesson71_rows.patch" brings them back whenever you want them.

HTML instruction: bash — run in the operator shell, in the kit (your rows kept as a patch, the four files given back)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_generated_candidates
Expected observation: evals/build_golden.py   | 2 ++
 evals/golden.jsonl      | 2 ++
 evals/paraphrases.jsonl | 2 ++
 evals/required.json     | 1 +
 4 files changed, 7 insertions(+)
the four files match the kit again
65
7

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L954

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """F="evals/build_golden.py evals/golden.jsonl evals/required.json evals/paraphrases.jsonl"
git diff --stat -- $F
git diff --quiet -- $F || { git diff -- $F > "$HOME/lesson71_rows.patch" && git checkout -- $F; }   # a second run keeps the patch
git diff --quiet -- $F && echo "the four files match the kit again"
wc -l < evals/golden.jsonl; grep -c '^+[^+]' "$HOME/lesson71_rows.patch"
"""


def demonstrate(session):
    """Run Keep your rows, and give the kit its files back at this checkpoint.

    Your clone now differs from the kit in four files. Lesson 7.2 runs the kit's own set, 65 rows and 15 required ids. The setup block's git pull --ff-only also refuses to run over local edits to a file the kit has changed. So keep your rows as a patch and restore the four files. git -C "$DEMO_ROOT" apply "$HOME/lesson71_rows.patch" brings them back whenever you want them.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (your rows kept as a patch, the four files given back).
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
