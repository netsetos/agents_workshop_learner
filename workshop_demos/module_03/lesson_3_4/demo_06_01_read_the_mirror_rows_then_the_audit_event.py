"""Lesson 3.4 / s6: Inspect the mirror and the audit trail

Summary and purpose:
Read the mirror rows, then the audit event

HTML instruction: bash — run in the operator shell (two BigQuery queries, then one read from the audit bucket)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_read_one_datapoint_back_then_search_for_it
Expected observation: +--------------------------------------------------+---------------------------+------+----------+----------+----------+
|                     chunk_id                     |       heading_path        | kind | doc_type | pii_flag |    at    |
+--------------------------------------------------+---------------------------+------+----------+----------+----------+
| acme:9c41d0e2b7f5...#0                           | NULL                      | text | unknown  |    false | 10:39:52 |
| acme:9c41d0e2b7f5...#1                           | SM-01 - The smoke lantern | text | unknown  |    false | 10:39:52 |
| acme:9c41d0e2b7f5...#2                           | SM-02 - The ladder        | text | unknown  |    false | 10:39:52 |
+--------------------------------------------------+---------------------------+------+----------+----------+----------+
+-----------+-----------+
| rows_ever | documents |
+

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L807

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """bq --project_id="$PROJECT" query --use_legacy_sql=false --format=pretty \\
  "SELECT chunk_id, heading_path, kind, doc_type, pii_flag, FORMAT_TIMESTAMP('%H:%M:%S', ingested_at) AS at
   FROM \\`$BQ_CHUNK_TABLE\\` WHERE tenant_id = 'acme' AND source_uri = 'gs://$PROJECT-uploads/acme/smoke_note_v1.md' ORDER BY chunk_id"

bq --project_id="$PROJECT" query --use_legacy_sql=false --format=pretty \\
  "SELECT COUNT(*) AS rows_ever, COUNT(DISTINCT source_uri) AS documents FROM \\`$BQ_CHUNK_TABLE\\` WHERE tenant_id = 'acme'"

gcloud storage cat "gs://$AUDIT_BUCKET/$(date -u +%Y/%m/%d)/acme/doc.upload-*.json" \\
  | python -c "import json,sys,hashlib,os; sha=hashlib.sha256(open(os.environ.get('NOTE', os.path.expanduser('~/lesson34_note.md')),'rb').read()).hexdigest(); [print(json.dumps(e, indent=1)) for e in map(json.loads, sys.stdin.read().replace('}{', '}\\n{').split('\\n')) if e['target']['id'].endswith(sha)]"
"""


def demonstrate(session):
    """Run Read the mirror rows, then the audit event at this checkpoint.

    Read the mirror rows, then the audit event

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two BigQuery queries, then one read from the audit bucket).
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
