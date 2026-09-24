"""Lesson 4.4 / s8: Restore the exact bytes and prove reuse

Summary and purpose:
A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

HTML instruction: bash — upload only if the original checksum still passes; wait for the new generation
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L712

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ch44_upload &&
python - <<'PY'
import json, os
from pathlib import Path
d=Path(os.environ["DEMO_DIR"])
r=json.loads((d/"source.json").read_text())
n=int((d/"initial-chunks.txt").read_text())
assert r["status"]=="indexed" and r["doc_key"]==os.environ["DOC_KEY"]
assert str(r["generation"])==os.environ["CH44_GENERATION"]
assert r["chunks"]==n and r["reused"]==n and r["embedded"]==0, \\
    "This was not a complete reuse. Inspect this version's worker events."
print("Restored:", n, "chunks reused; 0 embedded")
PY
"""


def demonstrate(session):
    """Run Restore the exact bytes and prove reuse at this checkpoint.

    A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — upload only if the original checksum still passes; wait for the new generation.
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
