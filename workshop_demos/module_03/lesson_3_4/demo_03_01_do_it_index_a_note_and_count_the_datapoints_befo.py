"""Lesson 3.4 / s3: Write: the order the worker keeps, and a fresh document to watch

Summary and purpose:
The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one small ingest)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: datapoints before: N
>> event doc_key chunks pages embedded: ingest_ok  acme_9c41d0e2b7f5a1...  3  1  3
datapoints now: N+3

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L475

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """idx_count() { gcloud ai indexes describe "$(basename "$VECTOR_INDEX_NAME")" --region="$REGION" --project="$PROJECT" --format='value(indexStats.vectorsCount)' 2>/dev/null; }
BEFORE="$(idx_count)"; echo "datapoints before: ${BEFORE:-0}"
export NOTE="$HOME/lesson34_note.md"
{ cat evals/demo/smoke_note_v1.md; printf '\\nIndexed for lesson 3.4 by %s on %s.\\n' "$ME" "$(date -u +%F)"; } > "$NOTE"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gcloud storage cp "$NOTE" "gs://$PROJECT-uploads/acme/smoke_note_v1.md"
for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.doc_key:\\"acme_\\" AND timestamp>=\\"$SINCE\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.pages,jsonPayload.embedded)')"
  [ -n "$LINE" ] && { echo ">> event doc_key chunks pages embedded: $LINE"; break; }
done
for i in $(seq 1 30); do N="$(idx_count)"; [ "${N:-0}" -ge $(( ${BEFORE:-0} + 3 )) ] && { echo "datapoints now: $N"; break; }; sleep 20; done
"""


def demonstrate(session):
    """Run Do it: index a note, and count the datapoints before and after at this checkpoint.

    The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one small ingest).
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
