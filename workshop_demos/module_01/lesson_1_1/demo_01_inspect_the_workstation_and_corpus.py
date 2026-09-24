"""Lesson 1.1 / plan-1: Inspect the workstation and corpus

Summary and purpose:
Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: The IDE interpreter and tool paths are visible; the ACME handbook exists.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
