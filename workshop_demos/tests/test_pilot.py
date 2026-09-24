"""Offline contracts and failure-path checks. These do not test a deployed service."""
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from workshop_helpers.api import ApiClient
from workshop_helpers.artifacts import ArtifactStore
from workshop_helpers.config import load_config
from workshop_helpers.discovery import select_revision
from workshop_helpers.kit import KitAdapter
from workshop_helpers.lifecycle import (
    Fixture, assert_fixture_owned, delete_live_object, ensure_original_present,
    prove_reuse, upload_original, wait_indexed,
)
from workshop_helpers.reconciliation import evaluate, require_fixture_plan

WORKSHOP = Path(__file__).resolve().parents[1]


def demo_module(filename):
    spec = importlib.util.spec_from_file_location(filename[:-3], WORKSHOP / "module_04" / "lesson_4_4" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = replace(load_config(), project="test-project", uploads_bucket="test-project-uploads",
                              results_dir=Path(self.temp.name), ingest_wait_seconds=1, poll_seconds=0.001)
        self.ctx = SimpleNamespace(config=self.config, artifacts=ArtifactStore(self.config, "03"),
                                   storage=Mock(), db=Mock(), kit=Mock(), api=Mock())
        data = b"unique fixture bytes\n"
        (self.ctx.artifacts.directory / "note.md").write_bytes(data)
        sha = hashlib.sha256(data).hexdigest()
        run = self.ctx.artifacts.run_id
        name = f"{self.config.tenant_id}/lesson44_{run}.md"
        self.fixture = Fixture(self.config.project, self.config.tenant_id, self.config.uploads_bucket,
                               run, name, f"gs://{self.config.uploads_bucket}/{name}", sha,
                               f"{self.config.tenant_id}_{sha}", "Where is the test compass?", "101", 3)

    def test_actual_kit_seven_decisions_and_drift(self):
        kit = KitAdapter(self.config.kit_root)
        objects, ledger, documents, hashes = demo_module("demo_01_reconciliation_rules.py").examples(self.config.tenant_id)
        report = evaluate(kit, objects, ledger, documents, lambda action: hashes[action["name"]])
        for action in ("retire", "reingest", "backfill", "touch", "queued", "withdrawn", "ok"):
            self.assertEqual(report["summary"][action], 1)
        self.assertEqual(report["summary"]["drift"], 3)
        self.assertFalse(report["summary"]["applied"])

    def test_queued_claim_cannot_hide_newer_generation(self):
        kit = KitAdapter(self.config.kit_root)
        obj = {"name": "acme/batch.pdf", "generation": "5", "tenant_id": "acme"}
        claims = {"acme_hash": {"gcs_uri": "gs://bucket/acme/batch.pdf", "generation": "4", "status": "queued"}}
        self.assertEqual(kit.planner.plan([obj], {}, claims)[0]["action"], "check_bytes")
        obj["generation"] = "4"
        self.assertEqual(kit.planner.plan([obj], {}, claims)[0]["action"], "queued")

    def test_legacy_queued_claim_is_preserved(self):
        kit = KitAdapter(self.config.kit_root)
        claims = {"acme_hash": {"gcs_uri": "gs://bucket/acme/batch.pdf", "status": "queued"}}
        self.assertEqual(kit.planner.plan([{"name": "acme/batch.pdf", "generation": "5", "tenant_id": "acme"}],
                                         {}, claims)[0]["action"], "queued")

    def test_serving_revision_not_latest_candidate(self):
        service = {"status": {"latestReadyRevisionName": "api-new", "traffic": [
            {"revisionName": "api-old", "percent": 100}, {"revisionName": "api-new", "percent": 0}]}}
        self.assertEqual(select_revision(service), "api-old")
        with self.assertRaises(RuntimeError):
            select_revision(service, "api-new")
        service["status"]["traffic"][1]["percent"] = 10
        with self.assertRaises(RuntimeError):
            select_revision(service)

    def test_ownership_and_exact_bytes_required(self):
        self.assertEqual(assert_fixture_owned(self.ctx, self.fixture), b"unique fixture bytes\n")
        with self.assertRaises(RuntimeError):
            assert_fixture_owned(self.ctx, replace(self.fixture, name="acme/real_policy.md"))
        with self.assertRaises(RuntimeError):
            assert_fixture_owned(self.ctx, replace(self.fixture, project="another-project"))
        (self.ctx.artifacts.directory / "note.md").write_bytes(b"changed")
        with self.assertRaises(RuntimeError):
            assert_fixture_owned(self.ctx, self.fixture)

    def test_upload_never_overwrites_an_object(self):
        blob = self.ctx.storage.bucket.return_value.blob.return_value
        blob.generation = 202
        self.assertEqual(upload_original(self.ctx, self.fixture), "202")
        self.assertEqual(blob.upload_from_string.call_args.kwargs["if_generation_match"], 0)

    def test_delete_generation_and_ownership_guards(self):
        blob = self.ctx.storage.bucket.return_value.get_blob.return_value
        blob.generation = 999
        with self.assertRaises(RuntimeError):
            delete_live_object(self.ctx, self.fixture)
        blob.delete.assert_not_called()
        blob.generation = 101
        blob.metadata = {"workshop_run": self.fixture.run_id}
        blob.download_as_bytes.return_value = b"unique fixture bytes\n"
        delete_live_object(self.ctx, self.fixture)
        self.assertEqual(blob.delete.call_args.kwargs["if_generation_match"], 101)

    def test_restore_preserves_existing_identical_generation(self):
        blob = self.ctx.storage.bucket.return_value.get_blob.return_value
        blob.metadata = {"workshop_run": self.fixture.run_id}
        blob.generation = 202
        blob.download_as_bytes.return_value = b"unique fixture bytes\n"
        with patch("workshop_helpers.lifecycle.wait_indexed", return_value={"status": "indexed"}) as wait:
            ensure_original_present(self.ctx, self.fixture)
            wait.assert_called_once_with(self.ctx, self.fixture, "202")
        self.ctx.storage.bucket.return_value.blob.assert_not_called()

    def test_restore_refuses_existing_changed_bytes(self):
        blob = self.ctx.storage.bucket.return_value.get_blob.return_value
        blob.metadata = {"workshop_run": self.fixture.run_id}
        blob.generation = 202
        blob.download_as_bytes.return_value = b"not the saved original"
        with self.assertRaises(RuntimeError):
            ensure_original_present(self.ctx, self.fixture)
        self.ctx.storage.bucket.return_value.blob.assert_not_called()

    def test_reuse_proof_requires_all_counts_and_new_generation(self):
        row = {"status": "indexed", "doc_key": self.fixture.doc_key, "sha256": self.fixture.sha256,
               "generation": "202", "chunks": 3, "reused": 3, "embedded": 0}
        prove_reuse(self.fixture, "202", row)
        for changes in ({"reused": 2}, {"embedded": 1}, {"doc_key": "different"}, {"generation": "101"}):
            with self.assertRaises(RuntimeError):
                prove_reuse(self.fixture, "202", {**row, **changes})
        with self.assertRaises(RuntimeError):
            prove_reuse(self.fixture, "101", {**row, "generation": "101"})

    def test_wait_ignores_old_ledger_generation(self):
        old = {"status": "indexed", "doc_key": self.fixture.doc_key, "sha256": self.fixture.sha256,
               "generation": "101", "chunks": 3}
        new = {**old, "generation": "202"}
        with patch("workshop_helpers.lifecycle.source_row", side_effect=[old, new]), patch("workshop_helpers.lifecycle.time.sleep"):
            self.assertEqual(wait_indexed(self.ctx, self.fixture, "202"), new)

    def test_fixture_plan_rejects_tenant_scope_and_other_names(self):
        report = {"scope": "tenant:acme", "actions": [], "summary": {"drift": 0}}
        with self.assertRaises(RuntimeError):
            require_fixture_plan(report, self.fixture, "clean")
        report.update(scope=self.fixture.uri, actions=[{"action": "retire", "name": "acme/other.md"}])
        with self.assertRaises(RuntimeError):
            require_fixture_plan(report, self.fixture, "retire")

    def test_api_requires_uncached_answer(self):
        api = object.__new__(ApiClient)
        api.config = self.config
        api.request = Mock(return_value={"cache_hit": "semantic"})
        with self.assertRaises(RuntimeError):
            api.query("question")
        api.request.return_value = {"cache_hit": "none"}
        self.assertEqual(api.query("question"), {"cache_hit": "none"})
        api.request.return_value = {"semantic_cache": "on"}
        with self.assertRaises(RuntimeError):
            api.check_fresh_answers()

    def test_helpers_import_without_google_or_gcloud_from_other_cwd(self):
        code = "import sys; import workshop_helpers; assert not any(x == 'google' or x.startswith('google.') for x in sys.modules)"
        subprocess.run([sys.executable, "-c", code], cwd=self.temp.name, check=True)

    def test_configuration_paths_independent_of_working_directory(self):
        original = Path.cwd()
        try:
            os.chdir(self.temp.name)
            self.assertEqual(load_config().kit_root, self.config.kit_root)
        finally:
            os.chdir(original)

    def test_round_trip_recovers_after_retirement_failure(self):
        module = demo_module("demo_03_restore_round_trip.py")
        worker = SimpleNamespace()  # patched asdict below avoids needing a real GCP serving config.
        initial = {"chunks": 3, "status": "indexed"}
        inspector = Mock()
        inspector.inspect.return_value = {"actions": [], "summary": {"drift": 0}}
        self.ctx.kit.apply_fixture_retirement.side_effect = RuntimeError("mirror failed")
        with patch.multiple(module, read_serving=Mock(return_value=worker), asdict=Mock(return_value={}),
                            create_fixture=Mock(return_value=self.fixture), save_fixture=Mock(),
                            upload_original=Mock(return_value="101"), wait_indexed=Mock(return_value=initial),
                            ReconcileInspector=Mock(return_value=inspector), require_fixture_plan=Mock(),
                            delete_live_object=Mock(), source_row=Mock(return_value=initial),
                            print_plan=Mock(), ensure_original_present=Mock(return_value={"status": "indexed"})) as unused:
            worker.environment = {}
            with self.assertRaisesRegex(RuntimeError, "mirror failed"):
                module.run_round_trip(self.ctx, verify_api=False)
            module.ensure_original_present.assert_called_once_with(self.ctx, self.fixture)
            self.assertEqual(self.fixture.phase, "recovered_after_incomplete_demo")

    def test_round_trip_full_sequence_with_cloud_boundaries_mocked(self):
        module = demo_module("demo_03_restore_round_trip.py")
        initial = {"chunks": 3, "status": "indexed"}
        restored = {"status": "indexed", "doc_key": self.fixture.doc_key, "sha256": self.fixture.sha256,
                    "generation": "202", "chunks": 3, "reused": 3, "embedded": 0}
        worker = SimpleNamespace(environment={})
        inspector = Mock()
        inspector.inspect.return_value = {"actions": [], "summary": {"drift": 0}}
        self.ctx.api.check_fresh_answers.return_value = {"semantic_cache": "off"}
        with patch.multiple(module, read_serving=Mock(return_value=worker), asdict=Mock(return_value={}),
                            create_fixture=Mock(return_value=self.fixture), save_fixture=Mock(),
                            upload_original=Mock(side_effect=["101", "202"]), wait_indexed=Mock(side_effect=[initial, restored]),
                            ReconcileInspector=Mock(return_value=inspector), require_fixture_plan=Mock(),
                            delete_live_object=Mock(), source_row=Mock(return_value=initial),
                            print_plan=Mock(), require_complete_retirement=Mock(return_value={"status": "retired"}),
                            check_answer=Mock(), worker_events=Mock(), ensure_original_present=Mock()):
            self.assertEqual(module.run_round_trip(self.ctx, verify_api=True), restored)
            self.assertEqual([call.kwargs["present"] for call in module.check_answer.call_args_list], [True, False, True])
            self.ctx.kit.apply_fixture_retirement.assert_called_once_with(self.ctx, self.fixture, {})
            module.ensure_original_present.assert_not_called()
            self.assertEqual(self.fixture.phase, "restored")


if __name__ == "__main__":
    unittest.main()
