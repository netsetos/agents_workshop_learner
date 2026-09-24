"""Lesson 4.3 / s5: Stale: the generation guard, and three replayed events

Summary and purpose:
The block reads the handbook's generation off the ledger, then publishes three records into the ingest topic exactly as Cloud Storage would, with the generation before the ledger's, the ledger's own, and one after it. The push subscription delivers them to the worker, and the worker's three lines say what it did with each. Nothing on the lane changes.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (three messages; nothing is indexed)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_purge_plan_rs_0
Expected observation: the ledger's generation for the handbook: 1758554107123456
TIMESTAMP                 EVENT               GENERATION        LEDGER_GENERATION  REASON
2026-09-22T15:02:31.512Z  ingest_stale_event  1758554107123457                     generation gone: the object was overwritten
2026-09-22T15:02:30.907Z  ingest_duplicate
2026-09-22T15:02:30.211Z  ingest_stale_event  1758554107123455  1758554107123456   older than the ledger

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L574

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """GEN="$(curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; print(next(r['generation'] for r in json.load(sys.stdin)['sources'] if r['name'].endswith('hr_policy_2026.md')))")"
SIZE="$(stat -c %s evals/corpus/acme/hr_policy_2026.md)"; echo "the ledger's generation for the handbook: $GEN"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for G in $((GEN - 1)) $GEN $((GEN + 1)); do
  gcloud pubsub topics publish documind-ingest --project "$PROJECT" \\
    --message "{\\"bucket\\":\\"$PROJECT-uploads\\",\\"name\\":\\"acme/hr_policy_2026.md\\",\\"generation\\":\\"$G\\",\\"size\\":\\"$SIZE\\",\\"contentType\\":\\"text/markdown\\"}" >/dev/null
done
sleep 25
gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$SINCE\\"" \\
  --project "$PROJECT" --limit 5 --format='table(timestamp,jsonPayload.event,jsonPayload.generation,jsonPayload.ledger_generation,jsonPayload.reason)'
"""


def demonstrate(session):
    """Run Do it: three events, three verdicts, Rs 0 at this checkpoint.

    The block reads the handbook's generation off the ledger, then publishes three records into the ingest topic exactly as Cloud Storage would, with the generation before the ledger's, the ledger's own, and one after it. The push subscription delivers them to the worker, and the worker's three lines say what it did with each. Nothing on the lane changes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (three messages; nothing is indexed).
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
