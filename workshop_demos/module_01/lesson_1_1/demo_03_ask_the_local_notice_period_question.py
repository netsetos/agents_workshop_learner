"""Lesson 1.1: Ask the local notice-period question

Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

Run order inside this file:
1. Ask the local notice-period question (source window plan-3)

Prerequisites: demo_02_start_the_local_chat_lane.
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


def step_01_ask_the_local_notice_period_question(session):
    """Run Ask the local notice-period question at this checkpoint.

    Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: A local answer with citations. Starting the server is a prerequisite even though it runs in another console.
    """
    import json, urllib.request
    request = urllib.request.Request("http://127.0.0.1:8081/v1/chat", method="POST",
        data=json.dumps({"question": "What is the notice period for a confirmed E3?", "session_id": "lesson11-local", "brain": "direct"}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        answer = json.load(response)
    print(json.dumps(answer, indent=2))
    assert answer.get("citations"), "The local answer has no citations; inspect its retrieval trace."

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_03_ask_the_local_notice_period_question', step_01_ask_the_local_notice_period_question),
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
