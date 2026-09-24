"""Recovery utility for an interrupted demo 03, including a forced IDE Stop.

Paste the exact results directory printed by the interrupted run below.
This restores only that run's original fixture and waits for indexing.
"""
from dataclasses import asdict
import json
from pathlib import Path
from workshop_helpers import DemoContext
from workshop_helpers.artifacts import write_json
from workshop_helpers.lifecycle import Fixture, ensure_original_present

RUN_DIRECTORY = ""  # Example: /home/user/deploy_module_rag/workshop_demos/results/.../20260924T..._...


def main():
    if not RUN_DIRECTORY:
        raise ValueError("Set RUN_DIRECTORY to the interrupted run's exact directory containing fixture.json and note.md.")
    directory = Path(RUN_DIRECTORY).expanduser().resolve()
    fixture = Fixture(**json.loads((directory / "fixture.json").read_text()))
    with DemoContext("04", live=True) as demo:
        restored = ensure_original_present(demo, fixture, directory)
        demo.artifacts.save("recovery", {"original_run": str(directory), "source": restored})
        fixture.phase = "recovered_manually"
        write_json(directory / "fixture.json", asdict(fixture))
        print("Original fixture is present and indexed:", fixture.uri)
        print("Recovery does not turn the original run into a passed demo.")


if __name__ == "__main__":
    main()
