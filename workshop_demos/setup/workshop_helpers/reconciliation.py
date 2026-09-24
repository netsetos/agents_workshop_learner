"""Read cloud evidence, then ask the kit's pure planning functions for decisions."""
from collections import Counter
import hashlib

ACTIONS = ("retire", "reingest", "backfill", "touch", "queued", "withdrawn", "ok")


def evaluate(kit, objects, ledger, documents, sha_for):
    actions = kit.planner.plan(objects, ledger, documents)
    for action in actions:
        if action["action"] == "check_bytes":
            sha = sha_for(action)
            row = ledger.get(kit.planner.source_id_for(action["tenant_id"], action["name"]))
            action["action"] = kit.planner.decide_bytes(sha, action["tenant_id"], row, documents)
            action["sha256"] = sha
    counts = Counter(action["action"] for action in actions)
    summary = {name: counts[name] for name in ACTIONS}
    summary.update(event="reconcile_done", applied=False, drift=kit.planner.drift_of(summary))
    return {"actions": actions, "summary": summary}


def print_plan(report):
    for row in report["actions"]:
        print(f"  {row['action']:10} {row['name']:55} {row.get('why', '')}")
    print("Summary:", report["summary"])
    print("Drift = retire + reingest + backfill. Queued and touch do not add drift.")


class ReconcileInspector:
    def __init__(self, context):
        self.context = context

    def inspect(self, fixture=None):
        ctx, config = self.context, self.context.config
        bucket = ctx.storage.bucket(config.uploads_bucket)
        if fixture:
            blob = bucket.get_blob(fixture.name, retry=None, timeout=30)
            blobs = [blob] if blob is not None else []
            source = ctx.db.collection("sources").document(fixture.source_id).get(retry=None, timeout=20)
            ledger = {source.id: source.to_dict()} if source.exists else {}
            claim = ctx.db.collection("documents").document(fixture.doc_key).get(retry=None, timeout=20)
            documents = {claim.id: claim.to_dict()} if claim.exists else {}
        else:
            from google.cloud.firestore_v1.base_query import FieldFilter
            blobs = list(bucket.list_blobs(prefix=f"{config.tenant_id}/", retry=None, timeout=30))
            ledger = {doc.id: doc.to_dict() or {} for doc in ctx.db.collection("sources").where(
                filter=FieldFilter("tenant_id", "==", config.tenant_id)).stream(retry=None, timeout=30)}
            # The kit scans documents/ too: legacy claims can lack tenant_id.
            # Retain only this tenant's object URIs in the evidence we save.
            prefix = f"gs://{config.uploads_bucket}/{config.tenant_id}/"
            documents = {doc.id: doc.to_dict() or {} for doc in ctx.db.collection("documents").stream(retry=None, timeout=30)
                         if (doc.to_dict() or {}).get("gcs_uri", "").startswith(prefix)}
        objects = [{"name": blob.name, "generation": str(blob.generation), "tenant_id": config.tenant_id}
                   for blob in blobs]
        by_name = {blob.name: blob for blob in blobs}

        def sha_for(action):
            blob = by_name[action["name"]]
            if config.max_hash_bytes and int(blob.size or 0) > config.max_hash_bytes:
                raise RuntimeError(f"{blob.name} exceeds max_hash_bytes; adjust the explicit read limit to finish this plan.")
            data = blob.download_as_bytes(if_generation_match=int(action["generation"]), retry=None, timeout=60)
            return hashlib.sha256(data).hexdigest()

        report = evaluate(ctx.kit, objects, ledger, documents, sha_for)
        report.update(scope=fixture.uri if fixture else f"tenant:{config.tenant_id}",
                      evidence={"objects": objects, "sources": ledger, "claims": documents})
        return report


def require_fixture_plan(report, fixture, expected):
    repairs = [row for row in report["actions"] if row["action"] in {"retire", "reingest", "backfill", "touch"}]
    if report["scope"] != fixture.uri:
        raise RuntimeError("This checkpoint requires a fixture-scoped plan.")
    if expected == "clean":
        if repairs or report["summary"]["drift"]:
            raise RuntimeError("The fixture still needs reconciliation. Inspect the saved plan.")
    elif expected == "retire":
        if len(repairs) != 1 or repairs[0]["action"] != "retire" or repairs[0]["name"] != fixture.name:
            raise RuntimeError("Expected exactly one retirement for this fixture.")
    else:
        raise ValueError("Unknown checkpoint.")
