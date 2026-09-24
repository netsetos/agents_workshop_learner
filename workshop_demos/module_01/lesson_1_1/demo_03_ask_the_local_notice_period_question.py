"""Lesson 1.1 / plan-3: Ask the local notice-period question

Summary and purpose:
Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_start_the_local_chat_lane
Expected observation: A local answer with citations. Starting the server is a prerequisite even though it runs in another console.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Ask the local notice-period question at this checkpoint.

    Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, urllib.request
    request = urllib.request.Request("http://127.0.0.1:8081/v1/chat", method="POST",
        data=json.dumps({"question": "What is the notice period for a confirmed E3?", "session_id": "lesson11-local", "brain": "direct"}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        answer = json.load(response)
    print(json.dumps(answer, indent=2))
    assert answer.get("citations"), "The local answer has no citations; inspect its retrieval trace."


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
