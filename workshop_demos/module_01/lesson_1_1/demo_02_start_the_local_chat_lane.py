"""Lesson 1.1: Start the local chat lane

Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

Run order inside this file:
1. Start the local chat lane (source window plan-2)

Prerequisites: demo_01_inspect_the_workstation_and_corpus.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
Example: open this file at the matching HTML heading, Run once, then inspect
the observations below before continuing to the next numbered section.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_start_the_local_chat_lane(session):
    """Run Start the local chat lane at this checkpoint.

    Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: The local chat server listens on port 8081. Ollama and the model must already be available; inspect the actual service output.
    """
    import sys
    session.start_local_service(["make", "chat-local", "PY=" + sys.executable], "http://127.0.0.1:8081/health")

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_02_start_the_local_chat_lane', step_01_start_the_local_chat_lane),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
