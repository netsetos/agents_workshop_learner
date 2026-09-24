"""Inspect a lock left by an interrupted IDE process; never replay cloud writes.

Edit LESSON. First run prints the lock. Once the named process is known to have
stopped, set REMOVE_STOPPED_PROCESS_LOCK=True and run again. The next lesson
recovery/finish file can then use the saved state and original fixture.
"""
import os
from pathlib import Path
from workshop_helpers.config import load_config

LESSON = "4.4"
REMOVE_STOPPED_PROCESS_LOCK = False


def main():
    """Release a verified dead process lock without changing any lesson artifacts.
    
    Example: main()
    """
    config = load_config()
    lock = config.results_dir / f"module_{int(LESSON.split('.')[0]):02}" / f"lesson_{LESSON.replace('.', '_')}" / "session.lock"
    if not lock.exists():
        print("No lock to recover.")
        return
    contents = lock.read_text(encoding="utf-8")
    print(lock, "\n", contents)
    if not REMOVE_STOPPED_PROCESS_LOCK:
        print("Inspect the named process. This run made no changes.")
        return
    if os.name != "posix":
        raise RuntimeError("Verify the process on the Cloud Workstation before removing its lock.")
    pid = int(contents.splitlines()[0].split("=", 1)[1])
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        lock.unlink()
        print("Dead-process lock removed. Saved session and evidence are unchanged.")
    else:
        raise RuntimeError("That process still exists. Stop/finish it before recovery.")


if __name__ == "__main__":
    main()
