"""Lesson 9.3 / s4: The replay: the same pairs, asked live at 0.95

Summary and purpose:
Each question gets a second try, two seconds after a 5xx or a timeout, as the kit's own run_eval.py gives it: one retry separates a blip from an outage. A blip, such as the first request to a fresh revision failing once, shows as a line saying how many questions were answered on a second try. A question that fails twice is listed with its HTTP status, and the replay carries on without it. The status is all the client sees. The reason is in the API's own log, and this reads the last three tracebacks, with the revision that threw each one:

HTML instruction: bash — run in the operator shell, only if the replay listed questions with no answer (the API's last three tracebacks)
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L571

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND textPayload:"Traceback"' --project "$PROJECT" --freshness=30m --limit 3 --format='value(timestamp,resource.labels.revision_name,textPayload)'
"""


def demonstrate(session):
    """Run Do it: the replay at this checkpoint.

    Each question gets a second try, two seconds after a 5xx or a timeout, as the kit's own run_eval.py gives it: one retry separates a blip from an outage. A blip, such as the first request to a fresh revision failing once, shows as a line saying how many questions were answered on a second try. A question that fails twice is listed with its HTTP status, and the replay carries on without it. The status is all the client sees. The reason is in the API's own log, and this reads the last three tracebacks, with the revision that threw each one:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, only if the replay listed questions with no answer (the API's last three tracebacks).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
