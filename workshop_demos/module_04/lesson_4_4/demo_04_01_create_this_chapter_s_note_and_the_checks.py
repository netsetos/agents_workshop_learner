"""Lesson 4.4 / s4: Create this chapter's note and the checks

Summary and purpose:
A fresh name, a new fact and an unchanged local copy remove the dependencies on earlier lessons. This chapter does not use ~/lesson34_note.md or the smoke-lantern question. Another smoke note may still answer that question even after one copy is retired. Our primary checks are the exact source name, its object generation and its citation; a bare answerable True is insufficient.

HTML instruction: bash — run once; keep the note and its checksum unchanged
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_credentials_backend_and_a_clean_baseline
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L522

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export NOTE="$DEMO_DIR/note.md"
export SOURCE="acme/lesson44_${RUN_ID}.md"
export OBJECT="gs://${PROJECT}-uploads/$SOURCE"
export QUESTION="Where is the violet compass for drill $RUN_ID stored?"
cat > "$NOTE" <<EOF
# Recovery drill $RUN_ID

The violet compass for drill $RUN_ID is stored in locker Q7
in the Jaipur training room.
EOF
sha256sum "$NOTE" > "$DEMO_DIR/note.sha256"
export DOC_KEY="acme_$(sha256sum "$NOTE" | cut -d ' ' -f1)"
python - <<'PY'
import json, os
from pathlib import Path
Path(os.environ["DEMO_DIR"], "query.json").write_text(json.dumps({
    "query": os.environ["QUESTION"], "tenant_id": "acme", "stream": False
}), encoding="utf-8")
PY
declare -p RUN_ID DEMO_DIR NOTE SOURCE OBJECT QUESTION DOC_KEY > "$DEMO_DIR/session.env"
printf 'Keep this directory for the whole demo: %s\\n' "$DEMO_DIR"
"""


def demonstrate(session):
    """Run Create this chapter's note and the checks at this checkpoint.

    A fresh name, a new fact and an unchanged local copy remove the dependencies on earlier lessons. This chapter does not use ~/lesson34_note.md or the smoke-lantern question. Another smoke note may still answer that question even after one copy is retired. Our primary checks are the exact source name, its object generation and its citation; a bare answerable True is insufficient.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run once; keep the note and its checksum unchanged.
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
