"""Lesson 7.3 / s5: The pairwise judge: which answer is better, row by row

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (twenty rows on each revision, then the Evaluation service)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_gate_on_the_live_revision_then_on_the
Expected observation: >> https://documind-api-NUMBER.asia-south1.run.app
  20/20 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  20/20 candidate answers from https://candidate---documind-api-NUMBER.asia-south1.run.app
  context: .../... cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070:
    groundedness/mean                                ...
    groundedness/mean[join]                          ...
    groundedness/mean[lookup]                        ...
    groundedness/std                                 ...
    instruction_following/mean                       ...
   

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html#L589

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" API_B="$CAND" JUDGE_ARGS="--rows 20"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (twenty rows on each revision, then the Evaluation service).
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
