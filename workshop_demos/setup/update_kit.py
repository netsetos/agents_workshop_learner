"""Optional explicit update. Never reset, force checkout, or discard local files."""
import shutil
import subprocess
from workshop_helpers.config import load_config


def main():
    root = load_config().kit_root
    executable = shutil.which("git")
    if not executable:
        raise RuntimeError("git is not on PATH.")

    def git(*args):
        return subprocess.run([executable, "-C", str(root), *args], check=True,
                              text=True, capture_output=True, timeout=120).stdout.strip()

    origin = git("remote", "get-url", "origin")
    if origin.rstrip("/").removesuffix(".git") not in {
        "https://github.com/netsetos/agents_workshop_learner",
        "git@github.com:netsetos/agents_workshop_learner",
    }:
        raise RuntimeError("This updater expects the existing agents_workshop_learner clone. Inspect origin manually.")
    if git("branch", "--show-current") != "main":
        raise RuntimeError("Switch to main explicitly before using this updater.")
    # Published demos are tracked kit files too; refuse their local edits as well.
    dirty = git("status", "--porcelain", "--", ".")
    if dirty:
        raise RuntimeError("The kit has local changes. Commit or preserve them yourself before updating.\n" + dirty)
    print(git("pull", "--ff-only", "origin", "main"))
    print(git("log", "-1", "--format=kit %h, %cd", "--date=short"))


if __name__ == "__main__":
    main()
