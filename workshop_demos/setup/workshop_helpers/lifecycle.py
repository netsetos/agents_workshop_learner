"""Small lifecycle operations; demo_03 keeps their order and assertions visible."""
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import time
from .auth import gcloud


@dataclass
class Fixture:
    project: str
    tenant_id: str
    bucket: str
    run_id: str
    name: str
    uri: str
    sha256: str
    doc_key: str
    question: str
    initial_generation: str = ""
    initial_chunks: int = 0
    phase: str = "prepared"

    @property
    def source_id(self):
        return self.name.replace("/", "~")


def create_fixture(context):
    config, run = context.config, context.artifacts.run_id
    name = f"{config.tenant_id}/lesson44_{run}.md"
    text = (f"# Recovery drill {run}\n\nThe violet compass for drill {run} is stored "
            "in locker Q7 in the Jaipur training room.\n")
    data = text.encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    fixture = Fixture(config.project, config.tenant_id, config.uploads_bucket, run, name,
                      f"gs://{config.uploads_bucket}/{name}", sha, f"{config.tenant_id}_{sha}",
                      f"Where is the violet compass for drill {run} stored?")
    if context.storage.bucket(fixture.bucket).get_blob(name, retry=None, timeout=20) or source_row(context, fixture):
        raise RuntimeError("Fixture collision: a new demo run is required.")
    (context.artifacts.directory / "note.md").write_bytes(data)
    save_fixture(context, fixture)
    return fixture


def save_fixture(context, fixture):
    context.artifacts.save("fixture", asdict(fixture))


def assert_fixture_owned(context, fixture, directory=None):
    config = context.config
    if not re.fullmatch(r"[0-9a-f]{16}", fixture.run_id):
        raise RuntimeError("Invalid fixture run ID.")
    expected_name = f"{config.tenant_id}/lesson44_{fixture.run_id}.md"
    if (fixture.project != config.project or fixture.tenant_id != config.tenant_id
            or fixture.bucket != config.uploads_bucket or fixture.name != expected_name
            or fixture.uri != f"gs://{fixture.bucket}/{expected_name}"):
        raise RuntimeError("Fixture identity does not match this project, bucket, tenant, and generated name.")
    note = Path(directory or context.artifacts.directory) / "note.md"
    data = note.read_bytes()
    if hashlib.sha256(data).hexdigest() != fixture.sha256 or fixture.doc_key != f"{fixture.tenant_id}_{fixture.sha256}":
        raise RuntimeError("The local original does not match the recorded hash. Restore requires the exact original bytes.")
    return data


def source_row(context, fixture):
    snap = context.db.collection("sources").document(fixture.source_id).get(retry=None, timeout=20)
    return snap.to_dict() or {} if snap.exists else {}


def upload_original(context, fixture, directory=None):
    data = assert_fixture_owned(context, fixture, directory)
    blob = context.storage.bucket(fixture.bucket).blob(fixture.name)
    blob.metadata = {"workshop_lesson": "4.4", "workshop_run": fixture.run_id, "original_sha256": fixture.sha256}
    blob.upload_from_string(data, content_type="text/markdown", if_generation_match=0, retry=None, timeout=60)
    generation = str(blob.generation)
    if not generation.isdigit():
        raise RuntimeError("Upload returned no generation; inspect the fixture before retrying.")
    return generation


def wait_indexed(context, fixture, generation):
    deadline = time.monotonic() + context.config.ingest_wait_seconds
    last = {}
    while time.monotonic() < deadline:
        last = source_row(context, fixture)
        if (last.get("status") == "indexed" and last.get("doc_key") == fixture.doc_key
                and str(last.get("generation")) == str(generation)
                and last.get("sha256") == fixture.sha256 and int(last.get("chunks") or 0) > 0):
            return last
        if last.get("status") == "withdrawn":
            raise RuntimeError("The fixture was explicitly withdrawn. This demo will not clear that tombstone.")
        print(f"  Waiting for generation {generation}: status={last.get('status', 'not recorded')}", flush=True)
        time.sleep(context.config.poll_seconds)
    context.artifacts.save("ingest_timeout", last)
    raise TimeoutError(f"Generation {generation} did not become indexed. Inspect the ingest worker and saved source row.")


def delete_live_object(context, fixture):
    data = assert_fixture_owned(context, fixture)
    blob = context.storage.bucket(fixture.bucket).get_blob(fixture.name, retry=None, timeout=20)
    if blob is None:
        raise RuntimeError("The fixture is already absent; a fresh run is needed to demonstrate deletion.")
    if str(blob.generation) != fixture.initial_generation:
        raise RuntimeError("The live generation changed; refusing to delete it.")
    if (blob.metadata or {}).get("workshop_run") != fixture.run_id:
        raise RuntimeError("Live object ownership metadata does not match this demo.")
    live_data = blob.download_as_bytes(if_generation_match=int(fixture.initial_generation), retry=None, timeout=30)
    if live_data != data:
        raise RuntimeError("Live bytes changed; refusing to delete this object.")
    blob.delete(if_generation_match=int(fixture.initial_generation), retry=None, timeout=30)
    fixture.phase = "object_deleted"
    save_fixture(context, fixture)


def require_complete_retirement(context, fixture):
    from google.cloud.firestore_v1.base_query import FieldFilter
    source = source_row(context, fixture)
    if source.get("status") != "retired" or source.get("doc_key") != fixture.doc_key:
        raise RuntimeError("The exact source is not retired.")
    rows = [row.to_dict() or {} for row in context.db.collection("chunks").where(
        filter=FieldFilter("doc_key", "==", fixture.doc_key)).stream(retry=None, timeout=30)]
    if len(rows) != fixture.initial_chunks or not all(
        row.get("current") is False and row.get("source_uri") == fixture.uri
        and row.get("tenant_id") == fixture.tenant_id for row in rows
    ):
        raise RuntimeError("Retained chunks are incomplete or not all retired; same-byte reuse cannot be claimed.")
    return source


def prove_reuse(fixture, generation, row):
    if str(generation) == fixture.initial_generation:
        raise RuntimeError("Restoration must have a new object generation.")
    expected = fixture.initial_chunks
    if not (row.get("status") == "indexed" and row.get("doc_key") == fixture.doc_key
            and row.get("sha256") == fixture.sha256 and str(row.get("generation")) == str(generation)
            and int(row.get("chunks", -1)) == expected and int(row.get("reused", -1)) == expected
            and int(row.get("embedded", -1)) == 0 and expected > 0):
        raise RuntimeError("The upload returned, but complete reuse (N reused, zero embedded) was not proved. Inspect the worker events.")


def check_answer(context, fixture, present, artifact):
    deadline = time.monotonic() + context.config.answer_wait_seconds
    last = None
    while time.monotonic() < deadline:
        last = context.api.query(fixture.question)
        context.artifacts.save(artifact, {"question": fixture.question, "source": fixture.uri, "response": last})
        cited = any(c.get("source_uri") == fixture.uri for c in last.get("citations", []))
        valid = (last.get("answerable") and cited and "Q7" in last.get("answer", "")
                 and "Jaipur" in last.get("answer", "")) if present else not cited
        print("  Answer:", "fixture cited" if cited else "fixture not cited",
              "| backend:", last.get("stages", {}).get("retrieval_backend"), flush=True)
        if valid:
            return last
        time.sleep(context.config.poll_seconds)
    raise TimeoutError(f"The API did not confirm fixture {'presence' if present else 'absence'}; inspect {artifact}.json.")


def worker_events(context, fixture, generation):
    query = (f'resource.type="cloud_run_revision" AND resource.labels.service_name={json.dumps(context.config.ingest_service)} '
             f'AND jsonPayload.doc_key={json.dumps(fixture.doc_key)} AND jsonPayload.generation={json.dumps(str(generation))}')
    try:
        records = json.loads(gcloud("logging", "read", query, f"--project={context.config.project}",
                                    "--freshness=1h", "--limit=20", "--format=json"))
        events = [{"timestamp": r.get("timestamp"), "payload": r.get("jsonPayload", {})} for r in records]
        context.artifacts.save("worker_events", events)
        print("Worker events:", [r["payload"].get("event") for r in events] or "not visible yet")
        return events
    except Exception as exc:
        context.artifacts.save("worker_events_unavailable", {"error": str(exc)})
        print("Worker logs could not be read; source generation and counts remain the recorded evidence:", exc)
        return []


def ensure_original_present(context, fixture, directory=None):
    """Recovery preserves an existing identical object and never overwrites another generation."""
    data = assert_fixture_owned(context, fixture, directory)
    blob = context.storage.bucket(fixture.bucket).get_blob(fixture.name, retry=None, timeout=20)
    if blob is not None:
        if (blob.metadata or {}).get("workshop_run") != fixture.run_id:
            raise RuntimeError("Recovery found different ownership metadata; inspect the object manually.")
        if blob.download_as_bytes(if_generation_match=int(blob.generation), retry=None, timeout=30) != data:
            raise RuntimeError("Recovery found different bytes; it will not overwrite them.")
        generation = str(blob.generation)
    else:
        generation = upload_original(context, fixture, directory)
    return wait_indexed(context, fixture, generation)
