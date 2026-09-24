"""Lesson 4.4 / s3: Credentials, backend and a clean baseline

Summary and purpose:
Do this before presenting. Stop at an error; do not paste the next stage until its checkpoint passes. Use the same operator shell and virtual environment throughout. Create a chapter directory before changing the backend, save its original pin, and run the offline planner check. These files are local demo state; keep them out of commits.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT; prepare once per demonstration
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_explore_a_different_bucket_and_ledger
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L500

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Credentials, backend and a clean baseline at this checkpoint.

    Do this before presenting. Stop at an error; do not paste the next stage until its checkpoint passes. Use the same operator shell and virtual environment throughout. Create a chapter directory before changing the backend, save its original pin, and run the offline planner check. These files are local demo state; keep them out of commits.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT; prepare once per demonstration.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.state["backend_restore_required"] = True
    session.save()
    session.shell(': "${PROJECT:?run the shell setup first}"\n: "${API:?run the shell setup first}"\nexport RUN_ID="$(python -c \'import uuid; print(uuid.uuid4().hex[:10])\')"\nexport DEMO_DIR="$PWD/.lesson44/$RUN_ID"\nmkdir -p "$DEMO_DIR"\n\nch44_prepare() {\n  GOOGLE_CLOUD_PROJECT="$PROJECT" python - <<\'PY\' > "$DEMO_DIR/backend-before.txt"\nimport warnings\nwarnings.filterwarnings("ignore", category=UserWarning)\nfrom shared.tenancy import backend_for\nprint(backend_for("acme") or "default")\nPY\n  [ "$?" -eq 0 ] && [ -s "$DEMO_DIR/backend-before.txt" ] || return 1\n  make tenant-backend PROJECT="$PROJECT" TENANT=acme RETRIEVAL_BACKEND=vector || return\n  python services/ingest/reconcile.py --selftest || return\n  make reconcile PROJECT="$PROJECT" TENANT_ONLY=acme\n}\nch44_prepare')


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
