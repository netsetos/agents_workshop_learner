"""Lesson 6.4 / s7: The UI's account: what it may do, and the checks the page makes first

Summary and purpose:
Do it: read the account's grants, Rs 0

HTML instruction: bash — run in the operator shell (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_open_the_source_then_render_your_own_trans
Expected observation: project roles:
roles/aiplatform.user
roles/datastore.user
roles/documentai.apiUser
roles/secretmanager.secretAccessor
roles/speech.editor
uploads bucket: ['roles/storage.objectAdmin']
may invoke documind-api: ['roles/run.invoker']
may invoke documind-chat: ['roles/run.invoker']
may invoke documind-ingest: none
on itself: ['roles/iam.serviceAccountTokenCreator']

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L731

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com"
echo "project roles:"; gcloud projects get-iam-policy "$PROJECT" --flatten=bindings --filter="bindings.members:serviceAccount:$SA" --format='value(bindings.role)'
has() { python -c "import json,sys; raw=sys.stdin.read(); m='serviceAccount:$SA'; j=json.loads(raw) if raw.strip() else None; print('no such service' if j is None else [b['role'] for b in j.get('bindings', []) if m in b.get('members', [])] or 'none')"; }
echo "uploads bucket: $(gcloud storage buckets get-iam-policy "gs://$PROJECT-uploads" --format=json | has)"
for S in documind-api documind-chat documind-ingest; do echo "may invoke $S: $(gcloud run services get-iam-policy "$S" --region "$REGION" --project "$PROJECT" --format=json 2>/dev/null | has)"; done
echo "on itself: $(gcloud iam service-accounts get-iam-policy "$SA" --project "$PROJECT" --format=json | has)"
"""


def demonstrate(session):
    """Run Do it: read the account's grants, Rs 0 at this checkpoint.

    Do it: read the account's grants, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (reads only).
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
