"""Lesson 7.2 / s5: The judge: the lane's own answers, read with the context they cite

Summary and purpose:
--reuse keeps the collected answers in a file. If the Evaluation step stops, the rerun judges the same answers without asking the lane again.

HTML instruction: bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_the_judge_s_venv_and_its_self_test
Expected observation: >> https://documind-api-NUMBER.asia-south1.run.app
  65/65 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  context: .../... cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-tcd7070)
  pairwise: off (no --api-b)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-tcd7070:
    groundedness/mean                                ...
    groundedness/mean[isolation]                     ...
    groundedness/mean[join]                          ...
    groundedness/mean[lookup]                        ...
    groundedness/mean[refusal]                       ...
    groundedness/mean[version]                       ...
    groundedness/std              

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L707

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """mkdir -p evals/reports
make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" JUDGE_ARGS="--reuse evals/reports/judge72.json"
"""


def demonstrate(session):
    """Run Do it: the judge on your lane at this checkpoint.

    --reuse keeps the collected answers in a file. If the Evaluation step stops, the rerun judges the same answers without asking the lane again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them).
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
