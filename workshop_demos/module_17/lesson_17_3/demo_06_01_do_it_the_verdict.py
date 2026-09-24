"""Lesson 17.3 / s6: The verdict and the delta

Summary and purpose:
Do it: the verdict

HTML instruction: bash — run in the operator shell, in the kit (the judge's venv from lesson 7.2: 65 answers from each revision, then Vertex AI Evaluation)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: >> https://documind-api-NUMBER.asia-south1.run.app
  65/65 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  65/65 candidate answers from https://candidate---documind-api-NUMBER.asia-south1.run.app
  context: 46/46 cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070:
    groundedness/mean                                1.000
    groundedness/mean[isolation]                     1.000
    groundedness/mean[join]                          1.000
    groundedness/mean[lookup]                        1.000
    groundedness/mean[refusal]                       1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L695

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" API_B="$CAND"
"""


def demonstrate(session):
    """Run Do it: the verdict at this checkpoint.

    Do it: the verdict

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the judge's venv from lesson 7.2: 65 answers from each revision, then Vertex AI Evaluation).
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
