"""Demo 3: create ONE unique note, delete it, reconcile its retirement, restore it.

This file writes to GCP. It leaves the restored note indexed for inspection.
It never applies the rest of the tenant's reconciliation plan.
"""
from dataclasses import asdict
from workshop_helpers import DemoContext
from workshop_helpers.discovery import read_serving
from workshop_helpers.lifecycle import (
    create_fixture, save_fixture, upload_original, wait_indexed, source_row,
    delete_live_object, require_complete_retirement, prove_reuse,
    check_answer, ensure_original_present, worker_events,
)
from workshop_helpers.reconciliation import ReconcileInspector, print_plan, require_fixture_plan

VERIFY_API = True  # False: storage + ledger + reuse proof only; no answer/citation claims.


def run_round_trip(demo, verify_api=VERIFY_API):
    worker = read_serving(demo.config, demo.config.ingest_service, demo.config.ingest_revision)
    demo.artifacts.save("ingest_configuration", asdict(worker))
    demo.kit.prepare_retirement(demo, worker.environment)
    if verify_api:
        demo.artifacts.save("api_version", demo.api.check_fresh_answers())
    else:
        print("API verification disabled. This run proves the storage and ledger lifecycle only.")
    fixture = create_fixture(demo)
    inspector = ReconcileInspector(demo)
    print("Fixture:", fixture.uri)
    recovery_needed = False
    try:
        print("\n1. Upload the original bytes and wait for this exact generation.")
        fixture.initial_generation = upload_original(demo, fixture)
        save_fixture(demo, fixture)
        initial = wait_indexed(demo, fixture, fixture.initial_generation)
        fixture.initial_chunks = int(initial["chunks"])
        fixture.phase = "indexed"
        save_fixture(demo, fixture)
        demo.artifacts.save("source_before", initial)
        plan = inspector.inspect(fixture)
        demo.artifacts.save("plan_before", plan)
        require_fixture_plan(plan, fixture, "clean")
        if verify_api:
            check_answer(demo, fixture, present=True, artifact="answer_before")

        print("\n2. Delete only this live object. Its original bytes remain in this run's note.md.")
        recovery_needed = True  # Also recover if the delete response is lost after the server committed it.
        delete_live_object(demo, fixture)
        after_delete = source_row(demo, fixture)
        demo.artifacts.save("source_after_delete", after_delete)
        plan = inspector.inspect(fixture)
        demo.artifacts.save("plan_after_delete", plan)
        print_plan(plan)

        print("\n3. Apply retirement ONLY for this fixture, using the kit's functions.")
        if after_delete.get("status") == "retired":
            print("A concurrent reconciler already retired this fixture; this run did not perform that retirement.")
        else:
            require_fixture_plan(plan, fixture, "retire")
            demo.kit.apply_fixture_retirement(demo, fixture, worker.environment)
        demo.artifacts.save("source_retired", require_complete_retirement(demo, fixture))
        fixture.phase = "retired"
        save_fixture(demo, fixture)
        plan = inspector.inspect(fixture)
        demo.artifacts.save("plan_retired", plan)
        require_fixture_plan(plan, fixture, "clean")
        if verify_api:
            check_answer(demo, fixture, present=False, artifact="answer_retired")

        print("\n4. Restore the exact original bytes under the same name.")
        generation = upload_original(demo, fixture)
        demo.artifacts.save("restored_generation", {"generation": generation})
        restored = wait_indexed(demo, fixture, generation)
        demo.artifacts.save("source_restored", restored)
        prove_reuse(fixture, generation, restored)
        if verify_api:
            check_answer(demo, fixture, present=True, artifact="answer_restored")
        plan = inspector.inspect(fixture)
        demo.artifacts.save("plan_restored", plan)
        require_fixture_plan(plan, fixture, "clean")
        fixture.phase = "restored"
        save_fixture(demo, fixture)
        recovery_needed = False
        worker_events(demo, fixture, generation)
        print(f"PASS: same doc_key; generation {fixture.initial_generation} -> {generation}; "
              f"chunks={fixture.initial_chunks}, reused={restored['reused']}, embedded={restored['embedded']}.")
        print("This fixture has zero drift and remains indexed. Inspect the saved evidence before the next run.")
        return restored
    finally:
        if recovery_needed:
            print("A step failed or was interrupted. Attempting to leave the original document present.", flush=True)
            try:
                recovered = ensure_original_present(demo, fixture)
                fixture.phase = "recovered_after_incomplete_demo"
                save_fixture(demo, fixture)
                demo.artifacts.save("recovery", recovered)
                print("Original is indexed again. The demo still FAILED; recovery is not proof of its assertions.")
            except Exception as recovery_error:
                demo.artifacts.save("recovery_failed", {"error": str(recovery_error)})
                print("Recovery incomplete:", recovery_error)
                print("Keep this results directory. Set RUN_DIRECTORY in recover_fixture.py and run it.")


def main():
    with DemoContext("03", live=True) as demo:
        run_round_trip(demo)


if __name__ == "__main__":
    main()
