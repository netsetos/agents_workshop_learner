"""Offline regressions for grouped experiments; all effects use temporary files."""
from contextlib import redirect_stdout
from dataclasses import replace
import importlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from workshop_helpers.artifacts import write_json
from workshop_helpers.config import load_config
from workshop_helpers.gates import expect_failure, live_gate
from workshop_helpers.poison import matches
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import ManualCheckpoint, backup_files, manual_checkpoint, restore_files, run_steps


class GroupedTests(unittest.TestCase):
    """Use real persisted sessions to exercise failures across separate IDE launches."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.kit = self.root / "kit"
        self.kit.mkdir()
        self.lesson = self.root / "lesson"
        (self.lesson / "setup").mkdir(parents=True)
        self.config = replace(load_config(), kit_root=self.kit, results_dir=self.root / "results", project="test-project")
        self.mapping = {"lesson": "5.3", "source_sha": "same-source", "layout_version": 2,
            "persist_variables": ["Q", "SECRET_TOKEN"], "demos": [
                {"id": "demo", "file": "demo.py", "category": "required", "requires": [], "heading": "Example", "purpose": "Test"},
                {"id": "next", "file": "next.py", "category": "required", "requires": ["demo"], "heading": "Next", "purpose": "Test"},
                {"id": "finish", "file": "setup/finish.py", "category": "cleanup", "requires": [], "heading": "Finish", "purpose": "Restore"}]}
        write_json(self.lesson / "lesson_map.json", self.mapping)
        for r in self.mapping["demos"]:
            (self.lesson / r["file"]).write_text("# fixture\n")
        self.capture = redirect_stdout(io.StringIO())
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def open(self, file="demo.py", **kw):
        return DemoSession(self.lesson / file, live=False, config=self.config, **kw)

    def test_failure_requires_decision_then_skips_completed_upload(self):
        calls = []
        def upload(s):
            calls.append("upload")
            os.environ["Q"] = "saved question"
            os.environ["SECRET_TOKEN"] = "not-on-disk"
        def failed(s):
            calls.append("read")
            raise ValueError("read failed after upload")
        steps = [("one", upload), ("two", failed)]
        with self.assertRaises(ValueError):
            with self.open() as s:
                run_steps(s, steps)
                self.fail("failure swallowed")
        with self.assertRaisesRegex(RuntimeError, "RETRY_FAILED_STEP"):
            with self.open() as s:
                run_steps(s, steps)
        with self.assertRaisesRegex(RuntimeError, "prerequisite"):
            with self.open("next.py"):
                pass
        def succeeds(s):
            self.assertEqual(os.environ["Q"], "saved question")
            calls.append("repaired")
        with self.open() as s:
            run_steps(s, [("one", upload), ("two", succeeds)], retry_failed=True)
            state = s.state
        self.assertEqual(calls, ["upload", "read", "repaired"])
        self.assertNotIn("not-on-disk", json.dumps(state))

    def test_manual_pause_resumes_without_acknowledging_eof(self):
        calls = []
        def first(s): calls.append("first")
        def browser(s):
            manual_checkpoint("Upload the exact file")
            calls.append("browser")
        with patch("builtins.input", side_effect=EOFError), self.assertRaises(ManualCheckpoint):
            with self.open() as s:
                run_steps(s, [("one", first), ("two", browser)])
        with patch("builtins.input", return_value="done"):
            with self.open() as s:
                run_steps(s, [("one", first), ("two", browser)])
        self.assertEqual(calls, ["first", "browser"])

    def test_running_checkpoint_requires_retry_decision(self):
        with self.assertRaises(RuntimeError):
            with self.open() as s:
                s.state["function_checkpoints"] = {"demo": {"one": {"status": "running"}}}
                run_steps(s, [("one", lambda s: self.fail("interrupted mutation replayed"))])

    def test_cleanup_attempts_remaining_restoration_and_resumes(self):
        calls = []
        def bad(s): raise ValueError("cache restore failed")
        def good(s): calls.append("backend restored")
        with self.assertRaisesRegex(RuntimeError, "Cleanup incomplete"):
            with self.open("setup/finish.py") as s:
                run_steps(s, [("cache", bad), ("backend", good)], cleanup=True)
        with self.open("setup/finish.py") as s:
            run_steps(s, [("cache", lambda s: calls.append("cache restored")), ("backend", good)], cleanup=True)
        self.assertEqual(calls, ["backend restored", "cache restored"])
        with self.assertRaisesRegex(RuntimeError, "finished"):
            with self.open(): pass

    def test_old_layout_blocks_demos_but_allows_saved_cleanup(self):
        with self.open() as s:
            s.state["layout_version"] = 1
            s.state["original_backend"] = "rag_engine"
        with self.assertRaisesRegex(RuntimeError, "old file layout"):
            with self.open("next.py"): pass
        with self.open("setup/finish.py") as s:
            self.assertEqual(s.state["original_backend"], "rag_engine")

    def test_original_bytes_and_missing_file_state_are_restored(self):
        edited = self.kit / "fixture.py"
        edited.write_bytes(b"learner edits\r\n")
        with self.open() as s:
            backup_files(s, ["fixture.py", "absent.txt"])
            edited.write_bytes(b"lesson change\n")
            (self.kit / "absent.txt").write_text("created")
            backup_files(s, ["fixture.py"])
            restore_files(s)
            self.assertEqual(edited.read_bytes(), b"learner edits\r\n")
            self.assertFalse((self.kit / "absent.txt").exists())
            self.assertTrue(list(s.attempt.glob("*.lesson-edited")))
            with self.assertRaises(ValueError):
                backup_files(s, ["../escape"])

    def test_import_path_and_module_are_isolated_between_cells(self):
        for name, value in (("left", 1), ("right", 2)):
            directory = self.kit / name
            directory.mkdir()
            (directory / "lesson_test_config.py").write_text(f"VALUE = {value}\n")
        seen = []
        def left(s):
            sys.path.insert(0, str(self.kit / "left"))
            seen.append(importlib.import_module("lesson_test_config").VALUE)
            os.chdir(self.kit / "left")
        def right(s):
            self.assertEqual(Path.cwd(), self.kit)
            sys.path.insert(0, str(self.kit / "right"))
            seen.append(importlib.import_module("lesson_test_config").VALUE)
        with self.open() as s:
            run_steps(s, [("left", left), ("right", right)])
        self.assertEqual(seen, [1, 2])
        self.assertNotIn("lesson_test_config", sys.modules)

    def test_expected_failure_requires_its_diagnostic(self):
        with self.open() as s:
            args = [sys.executable, "-c", "print('iso-11: OWN corpus'); raise SystemExit(1)"]
            expect_failure(s, args, status=1, messages=["iso-11:", "OWN corpus"])
            with self.assertRaisesRegex(RuntimeError, "not the intended"):
                expect_failure(s, [sys.executable, "-c", "raise SystemExit(1)"], status=1, messages=["OWN corpus"])

    def test_dead_letter_requires_bucket_name_and_generation(self):
        expected = {"bucket": "example-uploads", "name": "acme/poison-one.pdf", "generation": "123"}
        self.assertTrue(matches(dict(expected), expected))
        for field in expected:
            self.assertFalse(matches({**expected, field: "different"}, expected))

    def test_live_red_gate_cannot_pass_with_http_failure(self):
        with self.open() as s:
            report = self.kit / "report.json"
            def fake_command(args, **kw):
                write_json(report, {"records": [{"pass": False, "outcome": "denied"}]})
                return 2
            with patch.object(s, "command", side_effect=fake_command):
                with self.assertRaisesRegex(RuntimeError, "HTTP/auth/schema"):
                    live_gate(s, report=report, expect_red=True)
