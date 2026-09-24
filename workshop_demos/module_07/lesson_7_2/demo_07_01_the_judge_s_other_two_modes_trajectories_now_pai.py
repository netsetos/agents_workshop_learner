"""Lesson 7.2 / s7: The judge's other two modes: trajectories now, pairwise in lesson 7.3

Summary and purpose:
The chat service's tool calls against the one grounded path, and why the pairwise judge needs a candidate. With CHAT_URL, the judge sends a few answerable acme rows to each of the chat service's three brains, langchain, langgraph and adk. It compares the tool calls each brain returns with the reference path: one retrieve, then the answer. The three matches are computed in judge.py: exact, in order and any order. A brain that answers without retrieving scores 0 on all three, whatever its answer says. --no-vertex skips the Evaluation service, and --reuse skips asking the API again, so this costs only the chat turns.

HTML instruction: bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_where_the_gate_and_the_judge_disagree_read_the_r
Expected observation: no documind-chat service on this lane: trajectories need one

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L792

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """CHAT_URL="$(gcloud run services describe documind-chat --region "$REGION" --project "$PROJECT" --format='value(status.url)' 2>/dev/null)"
if [ -n "$CHAT_URL" ]; then
  make judge PROJECT="$PROJECT" PY="$HOME/judge-venv/bin/python" CHAT_URL="$CHAT_URL" \\
    JUDGE_ARGS="--reuse evals/reports/judge72.json --no-vertex --trajectory-rows 3" | grep -E "reused|trajectory"
else echo "no documind-chat service on this lane: trajectories need one"; fi
"""


def demonstrate(session):
    """Run The judge's other two modes: trajectories now, pairwise in lesson 7.3 at this checkpoint.

    The chat service's tool calls against the one grounded path, and why the pairwise judge needs a candidate. With CHAT_URL, the judge sends a few answerable acme rows to each of the chat service's three brains, langchain, langgraph and adk. It compares the tool calls each brain returns with the reference path: one retrieve, then the answer. The three matches are computed in judge.py: exact, in order and any order. A brain that answers without retrieving scores 0 on all three, whatever its answer says. --no-vertex skips the Evaluation service, and --reuse skips asking the API again, so this costs only the chat turns.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise).
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
