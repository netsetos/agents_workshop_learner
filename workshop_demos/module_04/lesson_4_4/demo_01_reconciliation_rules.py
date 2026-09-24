"""Demo 1: simulated facts -> the REAL kit planner -> seven explained decisions.

Run this file. No GCP login, upload or deletion is performed.
"""
from workshop_helpers import DemoContext
from workshop_helpers.reconciliation import evaluate, print_plan


def examples(tenant):
    def name(stem):
        return f"{tenant}/{stem}.md"

    def ledger_row(stem, generation, sha, status="indexed"):
        return {"name": name(stem), "tenant_id": tenant, "gcs_uri": f"gs://example-uploads/{name(stem)}",
                "generation": generation, "sha256": sha, "doc_key": f"{tenant}_{sha}", "status": status}

    objects = [{"name": name(stem), "generation": generation, "tenant_id": tenant} for stem, generation in
               [("new", "1"), ("legacy", "1"), ("metadata_only", "2"),
                ("batch", "4"), ("healthy", "1"), ("withdrawn", "1")]]
    ledger = {name(stem).replace("/", "~"): ledger_row(stem, "1", sha, status) for stem, sha, status in
              [("gone", "gone-sha", "indexed"), ("metadata_only", "same-sha", "indexed"),
               ("healthy", "healthy-sha", "indexed"), ("withdrawn", "withdrawn-sha", "withdrawn")]}
    documents = {
        f"{tenant}_legacy-sha": {"status": "indexed", "gcs_uri": f"gs://example-uploads/{name('legacy')}"},
        f"{tenant}_batch-sha": {"status": "queued", "generation": "4",
                                "gcs_uri": f"gs://example-uploads/{name('batch')}"},
    }
    hashes = {name("new"): "new-sha", name("legacy"): "legacy-sha", name("metadata_only"): "same-sha"}
    return objects, ledger, documents, hashes


def main():
    with DemoContext("01") as demo:
        objects, ledger, documents, hashes = examples(demo.config.tenant_id)
        print("These names, generations and hashes are SIMULATED teaching inputs.")
        report = evaluate(demo.kit, objects, ledger, documents, lambda action: hashes[action["name"]])
        demo.artifacts.save("simulated_inputs", {"objects": objects, "sources": ledger,
                                                 "claims": documents, "simulated_hashes": hashes})
        demo.artifacts.save("plan", report)
        print_plan(report)
        expected = {"retire": 1, "reingest": 1, "backfill": 1, "touch": 1, "queued": 1, "withdrawn": 1, "ok": 1}
        if any(report["summary"][key] != value for key, value in expected.items()) or report["summary"]["drift"] != 3:
            raise RuntimeError("Kit behavior changed. Inspect plan.json before teaching this example.")
        print("\nWhy queued? documents/ has status='queued', the SAME object name and generation 4.")
        print("The planner leaves that work to the batch worker. No filename or size guess is used.")
        print("Touch means the generation changed but the simulated content hash stayed the same.")
        print("Backfill means those bytes were indexed already, but the sources/ ledger row is missing.")
        print("Withdrawn is an explicit tombstone; ordinary reconciliation leaves it alone.")
        print("PASS: seven decisions, three units of drift, zero cloud calls.")


if __name__ == "__main__":
    main()
