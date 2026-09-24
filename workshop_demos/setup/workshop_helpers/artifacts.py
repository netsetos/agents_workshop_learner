"""A unique local run directory; exact inputs and results remain inspectable."""
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import uuid


def json_default(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, default=json_default), encoding="utf-8")
    temporary.replace(path)


class ArtifactStore:
    def __init__(self, config, demo, module=4, lesson="4.4"):
        if not re.fullmatch(r"[0-9]{2}", demo):
            raise ValueError("Demo IDs use two digits.")
        if not isinstance(module, int) or module < 1 or not re.fullmatch(r"[0-9]+\.[0-9]+", lesson):
            raise ValueError("Use a positive module number and a numeric lesson such as 4.4.")
        self.run_id = uuid.uuid4().hex[:16]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.directory = config.results_dir / f"module_{module:02}" / f"lesson_{lesson.replace('.', '_')}" / f"demo_{demo}" / f"{stamp}_{self.run_id}"
        self.directory.mkdir(parents=True, exist_ok=False)
        self.manifest = {
            "schema_version": 1, "module": module, "lesson": lesson, "demo": demo, "run_id": self.run_id,
            "started_at": datetime.now(timezone.utc).isoformat(), "status": "running",
            "project": config.project, "tenant_id": config.tenant_id, "kit_root": str(config.kit_root),
        }
        self.save("run", self.manifest)

    def save(self, name, value):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise ValueError("Artifact names must be simple filenames.")
        path = self.directory / f"{name}.json"
        write_json(path, value)
        return path

    def finish(self, error=None):
        self.manifest.update(status="failed" if error else "complete",
                             finished_at=datetime.now(timezone.utc).isoformat())
        if error:
            self.manifest["error"] = f"{type(error).__name__}: {error}"
        self.save("run", self.manifest)
