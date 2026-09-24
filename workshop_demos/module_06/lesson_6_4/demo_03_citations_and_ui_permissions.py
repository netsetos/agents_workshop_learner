"""Lesson 6.4: demo 03 citations and ui permissions

Open a cited source, render the transcript and inspect the UI account's grants.

Run order inside this file:
1. Do it: open the source, then render your own transcript (source window 28)
2. Do it: read the account's grants, Rs 0 (source window 33)

Prerequisites: demo_02_browser_upload_and_answer.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_open_the_source_then_render_your_own_trans.
COMMANDS_01 = """curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What colour badge do visitors wear at the Pune warehouse?","tenant_id":"acme","top_k":5}' > /tmp/stream64.txt
echo "citation events: $(grep -c '^event: citation' /tmp/stream64.txt) | tokens: $(grep -c '^event: token' /tmp/stream64.txt) | done: $(grep -c '^event: done' /tmp/stream64.txt)"
grep -m1 '^data: {"n": 1' /tmp/stream64.txt | cut -c7- \\
  | python -c "import json,sys; d=json.load(sys.stdin); print('first citation:', d['source'].split('/')[-1], '| kind', d['kind'], '| page', d['page'], '| quote', repr(d['quote'][:48]))"
cat /tmp/stream64.txt

"""

def step_01_open_the_source_then_render_your_own_trans(session):
    """Run Do it: open the source, then render your own transcript at this checkpoint.

    In the browser, under the answer from step 5, open Sources and click Open source on the note. A new tab shows the note's text from the bucket, through a link that stops working in 15 minutes. Then capture the same answer as a transcript and paste it into the renderer in step 1:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one stream, a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint("Open the answer's citation/source in the UI and inspect the signed link. Type done to render and inspect the transcript from Python.")
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_read_the_account_s_grants_rs_0.
COMMANDS_02 = """SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com"
echo "project roles:"; gcloud projects get-iam-policy "$PROJECT" --flatten=bindings --filter="bindings.members:serviceAccount:$SA" --format='value(bindings.role)'
has() { python -c "import json,sys; raw=sys.stdin.read(); m='serviceAccount:$SA'; j=json.loads(raw) if raw.strip() else None; print('no such service' if j is None else [b['role'] for b in j.get('bindings', []) if m in b.get('members', [])] or 'none')"; }
echo "uploads bucket: $(gcloud storage buckets get-iam-policy "gs://$PROJECT-uploads" --format=json | has)"
for S in documind-api documind-chat documind-ingest; do echo "may invoke $S: $(gcloud run services get-iam-policy "$S" --region "$REGION" --project "$PROJECT" --format=json 2>/dev/null | has)"; done
echo "on itself: $(gcloud iam service-accounts get-iam-policy "$SA" --project "$PROJECT" --format=json | has)"

"""

def step_02_read_the_account_s_grants_rs_0(session):
    """Run Do it: read the account's grants, Rs 0 at this checkpoint.

    Do it: read the account's grants, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_28', step_01_open_the_source_then_render_your_own_trans),
        ('source_33', step_02_read_the_account_s_grants_rs_0),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
