"""Lesson 4.3 / s3: Publish: the swap, and the reader's guard

Summary and purpose:
Read the handbook's versions, Rs 0

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: acme_497809ff...  rows 283  current 283  retired   0
acme_55603088...  rows 283  current   0  retired 283  superseded_by acme_497809ff...  expire_at 2026-10-22  effective_to None
acme_54337b4b...  rows 283  current   0  retired 283  superseded_by acme_497809ff...  expire_at 2026-10-22  effective_to None
current versions: 1 | staged rows: 0

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L454

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
