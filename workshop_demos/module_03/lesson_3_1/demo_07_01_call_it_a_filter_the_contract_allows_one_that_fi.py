"""Lesson 3.1 / s7: Chunk: the unit a question can find

Summary and purpose:
The API lets a caller narrow a search by kind or doc_type, because both are stamps on every row. It refuses any other key with a 400 that names the allowed ones - including tenant_id and current, which a caller might try to use as a filter and which are never theirs to set. One honest detail first: the worker stamps kind itself (text, or figure and segment for media), but it does not classify text documents, so every PDF and Markdown file it ingests carries doc_type: unknown. A doc_type: policy filter is allowed, and on your lane it matches nothing, so the API refuses to answer for lack of evidence. A filter is only as good as the stamp the writer put on the row.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_read_it_in_firestore
Expected observation: True ['acme:497809ff...#1', 'acme:497809ff...#2', 'acme:497809ff...#4']
False []
{"detail":"unknown filter key(s) tenant_id; allowed: doc_type, kind"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L801

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """# allowed, and matching: every text chunk carries kind=text
curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false,"filters":{"kind":"text"}}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answerable'], [c['chunk_id'] for c in j['citations']][:3])"

# allowed, but matching nothing: the worker stamps doc_type=unknown on every parsed document
curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false,"filters":{"doc_type":"policy"}}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answerable'], [c['chunk_id'] for c in j['citations']][:3])"

# refused: the tenant is not a filter
curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false,"filters":{"tenant_id":"zeta"}}'
"""


def demonstrate(session):
    """Run Call it: a filter the contract allows, one that finds nothing, and one it refuses at this checkpoint.

    The API lets a caller narrow a search by kind or doc_type, because both are stamps on every row. It refuses any other key with a 400 that names the allowed ones - including tenant_id and current, which a caller might try to use as a filter and which are never theirs to set. One honest detail first: the worker stamps kind itself (text, or figure and segment for media), but it does not classify text documents, so every PDF and Markdown file it ingests carries doc_type: unknown. A doc_type: policy filter is allowed, and on your lane it matches nothing, so the API refuses to answer for lack of evidence. A filter is only as good as the stamp the writer put on the row.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
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
