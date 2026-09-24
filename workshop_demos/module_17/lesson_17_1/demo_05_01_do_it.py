"""Lesson 17.1 / s5: Your training file, as v2

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (about twenty minutes: one flash call a chunk)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it
Expected observation: python evals/make_trainset.py --project documind-ai-YOUR-ID --tenant acme --rows ${ROWS:-300} \\
  --upload gs://documind-ai-YOUR-ID-datasets/sft/ --version v2
  300 chunks sampled from acme's corpus mirrors
  315 rows (30 refusals) from 12 documents; dropped 15 for golden overlap ['jn-10', 'jn-11', 'lk-14', 'lk-17', 'lk-18', 'lk-23', 'lk-24', 'lk-26', 'lk-28'] and 0 by the PII scan
  wrote /home/YOU/deploy_module_rag/evals/sft/documind_sft_v2.{vertex,chat}.jsonl + .manifest.json (sha ac73343d2550)
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.chat.jsonl
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.manifest.json
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.vertex.jsonl
  review the rows before you commit them: a generated question inherits the generator's blind spots (4.7)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.1-tuning-decision/Netsetos_GCP_Capstone_17.1_Tuning_Decision_WIX.html#L694

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q google-genai==2.22.0 google-cloud-dlp==3.39.0   # the ingest image's pins: the model that writes the rows, the PII scan
make trainset PROJECT="$PROJECT" TRAINSET_ARGS="--version v2"     # v1 is the kit's own file: yours is v2
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (about twenty minutes: one flash call a chunk).
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
