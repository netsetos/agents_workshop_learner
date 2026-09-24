"""Lesson 5.1 / s9: Finish: restore the saved tenant pin

Summary and purpose:
Run only after steps 3–9. Restore the value saved before the demo, which may be rag_engine, another backend or default. The last option removes the explicit pin. Do not assume every lane originally used RAG Engine, and do not place this command beside the setup command.

HTML instruction: bash — end of lesson only; restore the original Acme pin
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_the_question_the_revisions_answered_differ
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L947

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Finish: restore the saved tenant pin at this checkpoint.

    Run only after steps 3–9. Restore the value saved before the demo, which may be rag_engine, another backend or default. The last option removes the explicit pin. Do not assume every lane originally used RAG Engine, and do not place this command beside the setup command.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — end of lesson only; restore the original Acme pin.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, warnings
    from pathlib import Path
    warnings.filterwarnings("ignore", category=UserWarning)
    from shared.tenancy import backend_for, set_backend
    project = os.environ["PROJECT"]
    os.environ["GOOGLE_CLOUD_PROJECT"] = project
    path = Path("operator-evidence/lesson51/pin-before.json")
    if not path.exists():
        raise SystemExit("STOP: no saved pin; inspect the current tenant setting before changing it.")
    before = json.loads(path.read_text())
    if before["project"] != project:
        raise SystemExit("STOP: saved pin belongs to another project.")
    current = backend_for("acme") or "default"
    if current not in ("vector", before["backend"]):
        raise SystemExit("STOP: the pin changed independently; do not overwrite it.")
    print("Acme restored:", set_backend("acme", before["backend"]))
    print("Allow up to 60 seconds for the API's tenant-setting cache.")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
