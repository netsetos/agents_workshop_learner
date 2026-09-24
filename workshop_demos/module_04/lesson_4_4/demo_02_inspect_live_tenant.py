"""Demo 2: inspect live bucket, ledger and claims; save the plan without applying it."""
from workshop_helpers import DemoContext
from workshop_helpers.reconciliation import ReconcileInspector, print_plan


def main():
    with DemoContext("02", live=True) as demo:
        report = ReconcileInspector(demo).inspect()
        demo.artifacts.save("live_plan", report)
        print_plan(report)
        claims = report["evidence"]["claims"]
        for action in report["actions"]:
            if action["action"] != "queued":
                continue
            print("\nQueued evidence for", action["name"])
            matched = []
            for doc_key, claim in claims.items():
                by_object = claim.get("gcs_uri") == f"gs://{demo.config.uploads_bucket}/{action['name']}"
                generation = str(claim.get("generation") or "")
                by_generation = not generation or generation == str(action.get("generation"))
                by_hash = action.get("sha256") and doc_key == f"{demo.config.tenant_id}_{action['sha256']}"
                if claim.get("status") == "queued" and ((by_object and by_generation) or by_hash):
                    matched.append({"doc_key": doc_key, "status": claim["status"],
                                    "gcs_uri": claim.get("gcs_uri"), "generation": generation or "legacy: absent"})
            for proof in matched:
                print(" ", proof)
        print("\nRead-only inspection complete. No plan actions were applied.")
        print("This is a snapshot while ingestion may be running; repeat after workers settle if needed.")


if __name__ == "__main__":
    main()
