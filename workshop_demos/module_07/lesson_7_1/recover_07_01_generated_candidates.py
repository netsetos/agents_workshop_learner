"""Lesson 7.1 / s7: Paraphrase pairs and generated candidates: two kinds of row that are not golden

Summary and purpose:
The candidate fails twice. It has no figure, so it would accept any answer. Its anchor names a version by its hash, which no file contains, and which would point at a retired version the day the handbook is re-issued. The reviewed row, with a figure, a code and a slug, is lk-32. That rewrite is what review means: a figure a person checked in the clause, and anchors that survive a new version. Last, the generator itself, if your feed has rows. The chunk feature job and the Dataplex quality scan fill the feed, and lesson 13.2 runs them (make features). Before that, the count is zero and the cell stops there.

HTML instruction: bash — run in the operator shell, in the kit (one BigQuery count; ten Gemini calls only if the feed has rows)
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: feed rows for acme: 0
no feed rows yet: lesson 13.2 builds the feed (make features)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L910

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """N=$(bq --project_id="$PROJECT" query --nouse_legacy_sql --format=csv \\
  "SELECT COUNT(*) FROM \\`$PROJECT.rag_data.index_feed\\` WHERE tenant_id = 'acme'" | tail -1)
echo "feed rows for acme: $N"
if [ "${N:-0}" -gt 0 ] 2>/dev/null; then make make-evalset PROJECT="$PROJECT" TENANT=acme ROWS=10 && wc -l evals/golden_generated.jsonl
else echo "no feed rows yet: lesson 13.2 builds the feed (make features)"; fi
"""


def demonstrate(session):
    """Run Generated candidates at this checkpoint.

    The candidate fails twice. It has no figure, so it would accept any answer. Its anchor names a version by its hash, which no file contains, and which would point at a retired version the day the handbook is re-issued. The reviewed row, with a figure, a code and a slug, is lk-32. That rewrite is what review means: a figure a person checked in the clause, and anchors that survive a new version. Last, the generator itself, if your feed has rows. The chunk feature job and the Dataplex quality scan fill the feed, and lesson 13.2 runs them (make features). Before that, the count is zero and the cell stops there.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one BigQuery count; ten Gemini calls only if the feed has rows).
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
