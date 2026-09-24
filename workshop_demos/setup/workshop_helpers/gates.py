"""Observe deliberate evaluation failures without hiding unrelated command errors."""
import json
import os
from pathlib import Path


def expect_failure(session, args, *, status, messages):
    """Require both the expected exit code and the intended diagnostic in its log."""
    before = set(session.attempt.glob("command_*.log"))
    actual = session.command(args, check=False)
    logs = set(session.attempt.glob("command_*.log")) - before
    output = "\n".join(p.read_text(encoding="utf-8") for p in logs)
    if actual != status or not all(message in output for message in messages):
        raise RuntimeError(f"Expected exit {status} and diagnostics {messages!r}; got exit {actual}. Inspect the command log; this is not the intended red-gate proof.")
    print("Expected gate failure observed:", status, "|", "; ".join(messages))


def live_gate(session, *, report, source=None, expect_red=False):
    """Keep a live gate's report and status so later functions can inspect red rows.

Make wraps evaluator nonzero exits as 2. A fresh structured report distinguishes
quality failure from a failed command/token/import. HTTP/malformed failures
cannot satisfy the deliberate handbook-revision quality-failure experiment.
"""
    path = Path(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.replace(session.attempt / (path.name + ".previous"))
    args = ["make", "eval-live", f"PROJECT={session.config.project}", f"REGION={session.config.cloud_run_region}", f"REPORT={path}"]
    if source:
        args.append(f"SOURCE={source}")
    status = session.command(args, check=False)
    if status not in {0, 2} or not path.exists():
        raise RuntimeError(f"Gate exited {status} without a valid fresh report; inspect the command log.")
    value = json.loads(path.read_text(encoding="utf-8"))
    rows = value.get("records", [])
    if not rows:
        raise RuntimeError("The gate report has no evaluated rows.")
    print("Gate exit:", status, "| report:", path, "| failed:", value.get("failed"))
    if expect_red:
        if status != 2 or any(r.get("outcome") != "ok" for r in rows) or not any(not r["pass"] for r in rows):
            raise RuntimeError("Expected evaluated answers failing the golden assertions. An HTTP/auth/schema error or a green gate does not prove this experiment.")
        print("Revision-change red gate observed; the next step restores the original bytes.")
