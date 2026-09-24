"""Lesson 6.4: demo 02 browser upload and answer

Write the visitor note, upload it in the UI, follow indexing and compare browser/API answers.

Run order inside this file:
1. Do it: write the note, upload it in the browser, follow it (source window 16)
2. Do it: write the note, upload it in the browser, follow it (source window 17)
3. Do it: ask in the browser, ask from the shell, read both rows (source window 23)

Prerequisites: demo_01_authenticated_front_door.
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


# Original CLI workflow for step_01_write_the_note_upload_it_in_the_browser_fo.
COMMANDS_01 = """cat > "$HOME/pune_visitor_rules.md" <<EOF
# Pune warehouse visitor rules

Synthetic note for lesson 6.4, uploaded through the DocuMind UI. Every fact is invented.

## VR-01 - Badges

Every visitor to the Pune warehouse wears an amber badge, issued at gate 2 against a photo identity card and returned at the same gate.

## VR-02 - Escorts

A visitor is escorted at all times by the host who signed them in, and visitors do not enter the loading dock.

Uploaded through the UI for lesson 6.4 by $ME on $(date -u +%F).
EOF
sha256sum "$HOME/pune_visitor_rules.md" | cut -c1-12; cat "$HOME/pune_visitor_rules.md"

"""

def step_01_write_the_note_upload_it_in_the_browser_fo(session):
    """Run Do it: write the note, upload it in the browser, follow it at this checkpoint.

    First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (writes one small file in your home directory).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_write_the_note_upload_it_in_the_browser_fo(session):
    """Run Do it: write the note, upload it in the browser, follow it at this checkpoint.

    First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault. In the browser, open Documents, choose the file, and click Index documents. The page reports the object it wrote and its generation, then says the upload is complete and indexing is still in progress. Wait half a minute and click Refresh indexing status until the note appears in Versions. Then follow it from the shell:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the object, the worker's line, your hash, the ledger row).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint('In the ACME UI, Documents -> Upload: choose the exact ~/pune_visitor_rules.md created in the previous step, then Index documents. Refresh until indexed. If your browser runs elsewhere, download this exact file from the workstation first. Type done after the UI checkpoint.')
    from pathlib import Path
    from workshop_helpers.lesson31 import LessonCloud
    cloud = LessonCloud(session)
    data = (Path.home() / "pune_visitor_rules.md").read_bytes()
    expected = cloud.fixture("acme", "pune_visitor_rules.md", data, upload=False)
    observed = cloud.wait_indexed(expected)
    print("Exact UI upload:", expected, "|", observed["summary"])
    cloud.worker_logs(expected)

# Original CLI workflow for step_03_ask_in_the_browser_ask_from_the_shell_read.
COMMANDS_03 = """curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What colour badge do visitors wear at the Pune warehouse?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; raw=sys.stdin.read(); j=json.loads(raw) if raw.startswith('{') else {'answer': 'not JSON: ' + raw[:80], 'citations': []}; print('from the shell:', j.get('answer', j)[:70], '|', [c['source_uri'].split('/')[-1] for c in j.get('citations', [])[:1]])"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="stream" OR jsonPayload.event="query")' \\
  --project "$PROJECT" --freshness 15m --limit 2 --format='value(timestamp,jsonPayload.event,jsonPayload.user,jsonPayload.brain,jsonPayload.tenant,jsonPayload.pool)'

"""

def step_03_ask_in_the_browser_ask_from_the_shell_read(session):
    """Run Do it: ask in the browser, ask from the shell, read both rows at this checkpoint.

    In the browser, open Chat and ask: What colour badge do visitors wear at the Pune warehouse? The sources arrive first and the answer streams after them. The answer ends with a pill. Hover over it to see the note's clause, and open Sources under the answer. Then ask the same question from the shell and read the two newest rows:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question, a rupee; one log read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint('In the deployed UI Chat, ask the visitor-badge question from this lesson and wait for the cited answer. Type done to compare the browser and operator API records.')
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_16', step_01_write_the_note_upload_it_in_the_browser_fo),
        ('source_17', step_02_write_the_note_upload_it_in_the_browser_fo),
        ('source_23', step_03_ask_in_the_browser_ask_from_the_shell_read),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
