"""Lesson 4.4 / s2: How reconciliation decides

Summary and purpose:
Reproduce the five default widget documents before exploring its known-bytes and queued variations. The real plan(), decide_bytes() and drift_of() functions make the decisions.

HTML instruction: Python — simulated facts, actual kit planner; no network
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_how_do_we_know_a_pdf_is_queued
Expected observation: ok 1, retire 1, touch 1, reingest 1, withdrawn 1; drift 2

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L431

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Explore a different bucket and ledger at this checkpoint.

    Reproduce the five default widget documents before exploring its known-bytes and queued variations. The real plan(), decide_bytes() and drift_of() functions make the decisions.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Python — simulated facts, actual kit planner; no network.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from copy import deepcopy
    from workshop_helpers.kit import KitAdapter
    from workshop_helpers.reconciliation import evaluate_widget, print_plan
    # These are the exact default rows from the HTML widget; edit a copy for variations.
    rows = [{'name': 'acme/hr_policy_2026.md', 'bucket': 'same', 'ledger': 'indexed', 'bytes': 'same', 'queued': False}, {'name': 'acme/smoke_note_v1.md', 'bucket': 'absent', 'ledger': 'indexed', 'bytes': 'same', 'queued': False}, {'name': 'acme/dpdp_act_2023.pdf', 'bucket': 'newer', 'ledger': 'indexed', 'bytes': 'same', 'queued': False}, {'name': 'acme/new_circular.md', 'bucket': 'same', 'ledger': 'none', 'bytes': 'new', 'queued': False}, {'name': 'acme/old_policy.md', 'bucket': 'same', 'ledger': 'withdrawn', 'bytes': 'same', 'queued': False}]
    kit = KitAdapter(session.config.kit_root)
    report = evaluate_widget(kit, rows)
    print_plan(report)
    assert report["summary"]["drift"] == 2
    assert all(report["summary"][name] == 1 for name in ("ok", "retire", "touch", "reingest", "withdrawn"))
    known = deepcopy(rows)
    known[3]["bytes"] = "known"
    print("\nVariation: the circular's bytes already have an indexed claim.")
    print_plan(evaluate_widget(kit, known))
    queued = deepcopy(rows)
    queued[3]["queued"] = True
    print("\nVariation: a queued claim owns the circular's generation.")
    print_plan(evaluate_widget(kit, queued))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
