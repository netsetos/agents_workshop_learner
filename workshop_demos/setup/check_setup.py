"""Read-only preflight, separate from the teaching examples."""
from dataclasses import asdict
from workshop_helpers import DemoContext
from workshop_helpers.discovery import read_serving


def main():
    with DemoContext("00", live=True) as demo:
        print("Kit:", demo.kit.provenance["path"])
        snapshot = demo.db.document(f"tenant_settings/{demo.config.tenant_id}").get(retry=None, timeout=15)
        print("Firestore read: OK | tenant settings exist:", snapshot.exists)
        # Check object listing, the permission the read-only inspection actually needs.
        list(demo.storage.bucket(demo.config.uploads_bucket).list_blobs(
            prefix=f"{demo.config.tenant_id}/", max_results=1, retry=None, timeout=15))
        print("Uploads bucket listing: OK")
        worker = read_serving(demo.config, demo.config.ingest_service, demo.config.ingest_revision)
        demo.artifacts.save("ingest_configuration", asdict(worker))
        demo.kit.prepare_retirement(demo, worker.environment)
        print("Ingest revision:", worker.revision, "| mirror:", worker.environment.get("MANAGED_MIRROR", "off"))
        health = demo.api.request("/health", timeout=30)
        version = demo.api.request("/version", timeout=30)
        demo.artifacts.save("api_health", health)
        demo.artifacts.save("api_version", version)
        print("API health:", health)
        print("API:", demo.api.url)
        print("Answer cache:", version.get("semantic_cache", "not reported"))
        if version.get("semantic_cache") != "off":
            print("Demo 03: use VERIFY_API=False for ledger-only proof, or configure a serving demo API with cache off.")
        print("Read preflight passed. Upload, deletion and mirror write permissions are exercised only by demo 03.")


if __name__ == "__main__":
    main()
