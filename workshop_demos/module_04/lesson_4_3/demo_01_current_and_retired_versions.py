"""Lesson 4.3: demo 01 current and retired versions

Inspect version publication and the purge plan without applying deletion.

Run order inside this file:
1. Read the handbook's versions, Rs 0 (source window 9)
2. Do it: the purge plan, Rs 0 (source window 14)

Prerequisites: setup_prepare.
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


def step_01_read_the_handbook_s_versions_rs_0(session):
    """Run Read the handbook's versions, Rs 0 at this checkpoint.

    Read the handbook's versions, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings, collections
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    uri = f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md"
    rows = [r.to_dict() for r in db.collection("chunks").where("tenant_id", "==", "acme").where("source_uri", "==", uri).stream()]
    by = collections.defaultdict(list)
    for r in rows:
        by[r.get("doc_key")].append(r)
    for key, rs in sorted(by.items(), key=lambda kv: -sum(1 for r in kv[1] if r.get("current"))):
        cur, one = sum(1 for r in rs if r.get("current")), rs[0]
        flags = "" if cur else (f"  superseded_by {str(one.get('superseded_by'))[:13]}...  expire_at {one['expire_at'].date() if one.get('expire_at') else None}"
                                f"  effective_to {one.get('effective_to')}")
        print(f"{key[:13]}...  rows {len(rs):>3}  current {cur:>3}  retired {len(rs) - cur:>3}{flags}")
    print("current versions:", sum(1 for rs in by.values() if any(r.get("current") for r in rs)), "| staged rows:", sum(1 for r in rows if r.get("staged")))

# Original CLI workflow for step_02_the_purge_plan_rs_0.
COMMANDS_02 = """make purge PROJECT=$PROJECT TENANT_ONLY=acme

"""

def step_02_the_purge_plan_rs_0(session):
    """Run Do it: the purge plan, Rs 0 at this checkpoint.

    Do it: the purge plan, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only without APPLY=1).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_read_the_handbook_s_versions_rs_0),
        ('source_14', step_02_the_purge_plan_rs_0),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
