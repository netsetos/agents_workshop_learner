"""Lesson 3.3 / s3: One declared embedding, from Terraform to the row

Summary and purpose:
All read-only. The first prints the worker's environment, the second asks the API what it is serving, the third reads the pair off the ledger rows the Versions table renders.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: {'name': 'EMBEDDING_MODEL', 'value': 'text-embedding-005'}
{'name': 'EMBEDDING_VERSION', 'value': '1'}
api serves embedding text-embedding-005@1 | generator gemini-3.6-flash | retrieval hybrid vector
acme/code_on_wages_2019.pdf                  chunks   67  reused    0  embedded   67  text-embedding-005@1
acme/dpdp_act_2023.pdf                       chunks   44  reused    0  embedded   44  text-embedding-005@1
acme/hr_policy_2026.md                       chunks  283  reused    0  embedded  283  text-embedding-005@1
...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L481

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep -E 'EMBEDDING_MODEL|EMBEDDING_VERSION'

curl -s "$API/version" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; j=json.load(sys.stdin); print('api serves embedding', j['embedding'], '| generator', j['generator_model'], '| retrieval', j['retrieval_mode'], j['retrieval_backend'])"

curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; [print(f\\"{r['name']:44} chunks {r['chunks']:>4}  reused {r['reused']:>4}  embedded {r['embedded']:>4}  {r['embedding']}\\") for r in json.load(sys.stdin)['sources']]"
"""


def demonstrate(session):
    """Run Call it: three reads of one pair at this checkpoint.

    All read-only. The first prints the worker's environment, the second asks the API what it is serving, the third reads the pair off the ledger rows the Versions table renders.

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
