"""Lesson 4.4 / s12: Verify the story and restore the original backend

Summary and purpose:
Use the state transition and the exact evidence, then return the tenant to its saved configuration. Before reporting the chapter complete, check the final source and plan. If the optional incomplete-undo variation was run, record its fresh ingestion separately from the successful reuse in step 8. Leave the verified fixture and local original available for the audience to inspect.

HTML instruction: bash — finish the demo, then restore the pin saved before it began
Category: cleanup. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L1007

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Verify the story and restore the original backend at this checkpoint.

    Use the state transition and the exact evidence, then return the tenant to its saved configuration. Before reporting the chapter complete, check the final source and plan. If the optional incomplete-undo variation was run, record its fresh ingestion separately from the successful reuse in step 8. Leave the verified fixture and local original available for the audience to inspect.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — finish the demo, then restore the pin saved before it began.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    try:
        session.shell("ch44_source && ch44_plan clean")
    finally:
        session.shell('ch44_restore_backend() {\n  local previous\n  previous="$(cat "$DEMO_DIR/backend-before.txt")" || return\n  case "$previous" in\n    vector|firestore|rag_engine|vertex_search|default) ;;\n    *) echo "STOP: saved backend is missing or invalid."; return 1 ;;\n  esac\n  make tenant-backend PROJECT="$PROJECT" TENANT=acme RETRIEVAL_BACKEND="$previous"\n}\nch44_restore_backend')
        session.state["backend_restore_required"] = False
        session.save()


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
