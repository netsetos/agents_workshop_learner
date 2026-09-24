"""Lesson 6.4 / s4: The upload: a note you write, uploaded in the browser, followed to the ledger

Summary and purpose:
First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault. In the browser, open Documents, choose the file, and click Index documents. The page reports the object it wrote and its generation, then says the upload is complete and indexing is still in progress. Wait half a minute and click Refresh indexing status until the note appears in Versions. Then follow it from the shell:

HTML instruction: bash — run in the operator shell (the object, the worker's line, your hash, the ledger row)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_write_the_note_upload_it_in_the_browser_fo
Expected observation: text/plain	4xx	17586xxxxxxxxxxx
2026-09-2xT1x:xx:xx.xxxxxxZ	acme_3f9c2b7e1a04...	3	0	3
your file's hash begins: 3f9c2b7e1a04
acme/pune_visitor_rules.md indexed chunks 3 reused 0 embedded 3
versions NN | last event ingest_ok

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L545

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud storage objects describe "gs://$PROJECT-uploads/acme/pune_visitor_rules.md" --format='value(content_type,size,generation)'
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" AND jsonPayload.event="ingest_ok" AND jsonPayload.tenant="acme"' \\
  --project "$PROJECT" --freshness 30m --limit 1 --format='value(timestamp,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.reused,jsonPayload.embedded)'
echo "your file's hash begins: $(sha256sum "$HOME/pune_visitor_rules.md" | cut -c1-12)"
curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; j=json.load(sys.stdin); [print(r['name'], r['status'], 'chunks', r['chunks'], 'reused', r['reused'], 'embedded', r['embedded']) for r in j['sources'] if 'visitor' in r['name']]; print('versions', j['versions'], '| last event', j['last_event'])"
"""


def demonstrate(session):
    """Run Do it: write the note, upload it in the browser, follow it at this checkpoint.

    First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault. In the browser, open Documents, choose the file, and click Index documents. The page reports the object it wrote and its generation, then says the upload is complete and indexing is still in progress. Wait half a minute and click Refresh indexing status until the note appears in Versions. Then follow it from the shell:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the object, the worker's line, your hash, the ledger row).
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
