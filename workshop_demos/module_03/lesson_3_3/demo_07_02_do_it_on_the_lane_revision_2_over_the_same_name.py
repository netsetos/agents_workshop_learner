"""Lesson 3.3 / s7: Carry-over: re-issue the handbook, embed only what changed

Summary and purpose:
The upload must keep the object name, acme/hr_policy_2026.md, or it is a new source and nothing is held. The loop then waits for the worker's ingest_ok line and prints its counts. Cost: two clauses, 453 characters, about a hundredth of a paisa; a Markdown file pays no Document AI.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one re-issue; the worker takes under a minute)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_plan_it_locally_rs_0
Expected observation: >> chunks reused embedded retired effective_from: 283	281	2	283	2026-10-01

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L871

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gcloud storage cp evals/demo/hr_policy_2026_v2.md "gs://$PROJECT-uploads/acme/hr_policy_2026.md"
for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event=\\"ingest_ok\\" AND jsonPayload.tenant=\\"acme\\" AND timestamp>=\\"$SINCE\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.chunks,jsonPayload.reused,jsonPayload.embedded,jsonPayload.retired,jsonPayload.effective_from)')"
  [ -n "$LINE" ] && { echo ">> chunks reused embedded retired effective_from: $LINE"; break; }
done
"""


def demonstrate(session):
    """Run Do it on the lane: revision 2 over the same name at this checkpoint.

    The upload must keep the object name, acme/hr_policy_2026.md, or it is a new source and nothing is held. The loop then waits for the worker's ingest_ok line and prints its counts. Cost: two clauses, 453 characters, about a hundredth of a paisa; a Markdown file pays no Document AI.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one re-issue; the worker takes under a minute).
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
