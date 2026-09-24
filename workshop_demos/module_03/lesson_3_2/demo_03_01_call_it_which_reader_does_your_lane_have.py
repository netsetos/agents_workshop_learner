"""Lesson 3.2 / s3: Parse: Document AI, chosen by residency

Summary and purpose:
Two read-only calls. The first prints the worker's environment, where the residency and the processor id live. The second asks the Document AI API to list the processors in each of the two possible locations; exactly one location will list documind-parser.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: {'name': 'RESIDENCY', 'value': 'us'}
{'name': 'DOCAI_PROCESSOR_ID', 'value': 'a1b2c3d4e5f6a7b8'}
== us ==
documind-parser LAYOUT_PARSER_PROCESSOR ENABLED
== asia-south1 ==
(none)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L441

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep -E 'RESIDENCY|DOCAI_PROCESSOR_ID'

for LOC in us asia-south1; do
  echo "== $LOC =="
  curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \\
    "https://$LOC-documentai.googleapis.com/v1/projects/$NUMBER/locations/$LOC/processors" \\
    | python -c "import json,sys; j=json.load(sys.stdin); [print(p['displayName'], p['type'], p['state']) for p in j.get('processors', [])] or print('(none)')"
done
"""


def demonstrate(session):
    """Run Call it: which reader does your lane have? at this checkpoint.

    Two read-only calls. The first prints the worker's environment, where the residency and the processor id live. The second asks the Document AI API to list the processors in each of the two possible locations; exactly one location will list documind-parser.

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
