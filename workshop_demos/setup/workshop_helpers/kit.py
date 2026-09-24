"""Reuse the installed learner kit; do not copy its reconciliation rules.

The scoped retirement below performs the SAME retirement operations as the
kit's reconcile.py, but only after validating the pilot's one generated fixture.
It never calls the tenant-wide --apply command.
"""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import logging
import os
from pathlib import Path
import sys


class KitAdapter:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.ingest = self.root / "services" / "ingest"
        self.planner = self._load("reconcile")
        for name in ("plan", "decide_bytes", "drift_of"):
            if not callable(getattr(self.planner, name, None)):
                raise RuntimeError(f"Installed kit reconcile.py has no {name}(). Update the kit explicitly.")
        self.provenance = {
            "path": str(self.ingest / "reconcile.py"),
            "sha256": hashlib.sha256((self.ingest / "reconcile.py").read_bytes()).hexdigest(),
            "implementation": "actual local kit, loaded at runtime",
        }

    def _load(self, name):
        path = self.ingest / f"{name}.py"
        if not path.is_file():
            raise FileNotFoundError(f"Required kit module is missing: {path}")
        module_name = f"_workshop_kit_{name}_{hashlib.sha256(str(path).encode()).hexdigest()[:12]}"
        if module_name in sys.modules:
            return sys.modules[module_name]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(module_name, None)
            raise
        return module

    @contextmanager
    def environment(self, project, worker_env):
        # Legacy kit modules expect deploy/ on sys.path and these explicit env vars.
        # The bridge is centralized here, never pasted into individual demos.
        allowed = {"MANAGED_MIRROR", "RAG_LOCATION", "SEARCH_LOCATION", "AUDIT_BUCKET",
                   "RETENTION_DAYS", "EMBEDDING_MODEL"}
        values = {key: value for key, value in worker_env.items() if key in allowed}
        values["GOOGLE_CLOUD_PROJECT"] = project
        values.setdefault("MANAGED_MIRROR", "off")
        values.setdefault("RAG_LOCATION", "us-central1")
        values.setdefault("SEARCH_LOCATION", "global")
        values.setdefault("EMBEDDING_MODEL", "text-embedding-005")
        values.setdefault("RETENTION_DAYS", "30")
        values.setdefault("AUDIT_BUCKET", f"{project}-audit")
        previous = {key: os.environ.get(key) for key in values}
        old_path = list(sys.path)
        sys.path.insert(0, str(self.root))
        os.environ.update(values)
        try:
            yield
        finally:
            sys.path[:] = old_path
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def prepare_retirement(self, context, worker_env):
        """Check imports/configuration before the fixture is uploaded or deleted."""
        with self.environment(context.config.project, worker_env):
            if int(os.environ["RETENTION_DAYS"]) <= 0:
                raise RuntimeError("The same-byte undo demo needs a positive retention window.")
            idem = self._load("idempotency")
            managed = self._load("managed")
            for name in ("retire_previous", "refresh_fingerprint"):
                if not callable(getattr(idem, name, None)):
                    raise RuntimeError(f"Installed kit lacks {name}().")
            managed.Mirror.from_env(context.db)

    def apply_fixture_retirement(self, context, fixture, worker_env):
        from google.cloud import firestore
        from google.cloud.firestore_v1.base_query import FieldFilter
        from .lifecycle import assert_fixture_owned, source_row
        assert_fixture_owned(context, fixture)
        if context.storage.bucket(context.config.uploads_bucket).get_blob(fixture.name, retry=None, timeout=20):
            raise RuntimeError("The live object exists again. Refusing to retire it.")
        row = source_row(context, fixture)
        if row.get("status") != "indexed" or row.get("doc_key") != fixture.doc_key:
            raise RuntimeError("The source changed since planning; expected this fixture's indexed version.")
        if str(row.get("generation")) != str(fixture.initial_generation):
            raise RuntimeError("The source generation changed since this run's upload.")
        actions = self.planner.plan([], {fixture.source_id: row}, {})
        if len(actions) != 1 or actions[0]["action"] != "retire" or actions[0]["name"] != fixture.name:
            raise RuntimeError("The kit planner did not select exactly this fixture for retirement.")
        current = [snap.to_dict() or {} for snap in context.db.collection("chunks").where(
            filter=FieldFilter("tenant_id", "==", fixture.tenant_id)).where(
            filter=FieldFilter("source_uri", "==", fixture.uri)).stream(retry=None, timeout=30)
            if (snap.to_dict() or {}).get("current") is not False]
        if len(current) != fixture.initial_chunks or not all(row.get("doc_key") == fixture.doc_key for row in current):
            raise RuntimeError("The fixture's current chunks changed or are incomplete. Refusing retirement.")

        class Capture(logging.Handler):
            def __init__(self):
                super().__init__()
                self.lines = []
            def emit(self, record):
                self.lines.append(record.getMessage())

        capture = Capture()
        logger = logging.getLogger("documind.ingest")
        old_level = logger.level
        logger.setLevel(logging.INFO)
        logger.addHandler(capture)
        try:
            with self.environment(context.config.project, worker_env):
                idem = self._load("idempotency")
                managed = self._load("managed")
                mirror = managed.Mirror.from_env(context.db)
                expires = datetime.now(timezone.utc) + timedelta(days=int(os.environ["RETENTION_DAYS"]))
                gone = idem.retire_previous(context.db, fixture.tenant_id, fixture.uri, None, expire_at=expires)
                mirror.retired(fixture.tenant_id, gone.get("retired_doc_keys", []), "retired")
                context.db.collection("sources").document(fixture.source_id).set(
                    {"status": "retired", "retired_at": firestore.SERVER_TIMESTAMP}, merge=True)
                fingerprint = idem.refresh_fingerprint(context.db, fixture.tenant_id, "reconcile")
            result = {"scope": fixture.uri, "operations": "kit retirement functions",
                      "fingerprint": fingerprint, **gone, "mirror_logs": capture.lines}
            context.artifacts.save("retirement", result)
            if any('"mirror_failed"' in line or '"mirror_audit_failed"' in line for line in capture.lines):
                raise RuntimeError("A managed mirror or audit operation failed. See retirement.json. The demo will attempt to restore its original object.")
            return result
        finally:
            logger.removeHandler(capture)
            logger.setLevel(old_level)
