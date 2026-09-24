"""Lesson 1.1 / plan-2: Start the local chat lane

Summary and purpose:
Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_inspect_the_workstation_and_corpus
Expected observation: The local chat server listens on port 8081. Ollama and the model must already be available; inspect the actual service output.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Start the local chat lane at this checkpoint.

    Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.start_local_service(["make", "chat-local", "PY=" + sys.executable], "http://127.0.0.1:8081/health")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
