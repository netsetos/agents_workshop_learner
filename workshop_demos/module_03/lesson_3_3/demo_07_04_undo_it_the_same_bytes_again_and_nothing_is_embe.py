"""Lesson 3.3 / s7: Carry-over: re-issue the handbook, embed only what changed

Summary and purpose:
Upload version 1 again under the same name. Its doc_key is the one the lane retired a minute ago, so the worker does not parse, chunk or embed anything: it flips the retired rows back to current, retires revision 2, and logs ingest_reactivated with embedded 0. This is the undo from lesson 3.1, seen from the embedding side: nothing was ever deleted, so nothing has to be made again.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the undo; no model call)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_03_see_it_in_the_ui_then_read_it_three_more_ways
Expected observation: >> reactivated: chunks reused embedded retired: 283	283	0	283
A confirmed employee at grade E3 or above serves a notice period of 60 days ... [Source 1]

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L918

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gcloud storage cp evals/corpus/acme/hr_policy_2026.md "gs://$PROJECT-uploads/acme/hr_policy_2026.md"
for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event=\\"ingest_reactivated\\" AND jsonPayload.tenant=\\"acme\\" AND timestamp>=\\"$SINCE\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.chunks,jsonPayload.reused,jsonPayload.embedded,jsonPayload.retired)')"
  [ -n "$LINE" ] && { echo ">> reactivated: chunks reused embedded retired: $LINE"; break; }
done

curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"How many days of notice does a confirmed employee at grade E3 serve?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; print(json.load(sys.stdin)['answer'][:120])"
"""


def demonstrate(session):
    """Run Undo it: the same bytes again, and nothing is embedded at this checkpoint.

    Upload version 1 again under the same name. Its doc_key is the one the lane retired a minute ago, so the worker does not parse, chunk or embed anything: it flips the retired rows back to current, retires revision 2, and logs ingest_reactivated with embedded 0. This is the undo from lesson 3.1, seen from the embedding side: nothing was ever deleted, so nothing has to be made again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the undo; no model call).
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
