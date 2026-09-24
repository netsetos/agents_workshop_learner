"""Lesson 4.4 / s2: How reconciliation decides

Summary and purpose:
Explain the page's two-PDF illustration. Reconciliation leaves the matching queued generation to the batch lane; only the new Act contributes to drift.

HTML instruction: Python — simulated facts, actual kit planner; no network
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: reingest 1, queued 1, drift 1; applied false

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L335

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run How do we know a PDF is queued? at this checkpoint.

    Explain the page's two-PDF illustration. Reconciliation leaves the matching queued generation to the batch lane; only the new Act contributes to drift.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Python — simulated facts, actual kit planner; no network.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.kit import KitAdapter
    from workshop_helpers.reconciliation import evaluate, print_plan
    kit = KitAdapter(session.config.kit_root)
    objects = [dict(name="acme/cgst_act_2017.pdf", generation="1", tenant_id="acme"),
               dict(name="acme/cgst_it_bundle.pdf", generation="4", tenant_id="acme")]
    claims = {"acme_bundle": {"status": "queued", "generation": "4",
                              "gcs_uri": "gs://example-uploads/acme/cgst_it_bundle.pdf"}}
    report = evaluate(kit, objects, {}, claims, lambda action: "new-act-bytes")
    print_plan(report)
    assert report["summary"]["reingest"] == report["summary"]["queued"] == 1
    assert report["summary"]["drift"] == 1
    print("The queued claim names this object AND generation. It does not prove the batch job finished.")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
