"""Lesson 1.1: demo 01 inspect the workstation and corpus

Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

Run order inside this file:
1. Inspect the workstation and corpus (source window plan-1)

Prerequisites: workshop setup; see this lesson README.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_inspect_the_workstation_and_corpus(session):
    """Run Inspect the workstation and corpus at this checkpoint.

    Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import shutil, sys
    from pathlib import Path
    print("Python:", sys.executable)
    for name in ("git", "gcloud", "terraform", "docker", "ollama", "make"):
        print(name, "->", shutil.which(name) or "NOT INSTALLED")
    corpus = Path("evals/corpus")
    for tenant in ("acme", "zeta", "globex"):
        print(tenant, len(list((corpus / tenant).glob("*"))), "corpus files")
    assert (corpus / "acme/hr_policy_2026.md").is_file()
    print("Read shared/local_corpus.py: the local lane keeps tenant and citation identity.")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_01_inspect_the_workstation_and_corpus', step_01_inspect_the_workstation_and_corpus),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
