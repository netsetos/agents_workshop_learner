"""Lesson 3.2: demo 01 readers and page counts

Inspect parser selection, count the corpus and parse the small four-page PDF.

Run order inside this file:
1. Call it: which reader does your lane have? (source window 9)
2. Do it: count the corpus, Rs 0 (source window 12)
3. Prove it on the lane: one small PDF, four pages (source window 14)

Prerequisites: setup_prepare.
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


# Original CLI workflow for step_01_which_reader_does_your_lane_have.
COMMANDS_01 = """gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='value(spec.template.spec.containers[0].env)' | tr ';' '\\n' | grep -E 'RESIDENCY|DOCAI_PROCESSOR_ID'

for LOC in us asia-south1; do
  echo "== $LOC =="
  curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \\
    "https://$LOC-documentai.googleapis.com/v1/projects/$NUMBER/locations/$LOC/processors" \\
    | python -c "import json,sys; j=json.load(sys.stdin); [print(p['displayName'], p['type'], p['state']) for p in j.get('processors', [])] or print('(none)')"
done

"""

def step_01_which_reader_does_your_lane_have(session):
    """Run Call it: which reader does your lane have? at this checkpoint.

    Two read-only calls. The first prints the worker's environment, where the residency and the processor id live. The second asks the Document AI API to list the processors in each of the two possible locations; exactly one location will list documind-parser.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_count_the_corpus_rs_0(session):
    """Run Do it: count the corpus, Rs 0 at this checkpoint.

    The same count, on the PDFs in your kit folder, with the same library. The cell prints pages and slices per PDF, then the totals and what one parse of the whole corpus would cost at each processor's list price - the rates as the course reads them on the pricing page, to re-verify before quoting.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import glob, math, os
    from pypdf import PdfReader
    LIMIT, INLINE, USD_INR = 15, 250, 85
    OCR_USD, LAYOUT_USD = 1.50, 10.00            # per 1,000 pages, list price as read on the pricing page - re-verify
    total = calls = 0
    for path in sorted(glob.glob("evals/corpus/*/*.pdf")):
        n = len(PdfReader(path).pages)
        s = math.ceil(n / LIMIT)
        total += n; calls += s
        lane = "BATCH LANE" if n > INLINE else "inline"
        print(f"{path[13:]:48} pages={n:4} slices={s:3} {lane}")
    print(f"\n{total} pages in {calls} Document AI requests")
    print(f"one full parse: OCR Rs {total/1000*OCR_USD*USD_INR:,.0f}   Layout Parser Rs {total/1000*LAYOUT_USD*USD_INR:,.0f}")

# Original CLI workflow for step_03_prove_it_on_the_lane_one_small_pdf_four_pa.
COMMANDS_03 = """make ingest-one PROJECT=$PROJECT TENANT=globex FILE=evals/corpus/acme/maternity_benefit_amendment_act_2017.pdf

gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" AND jsonPayload.event="ingest_ok" AND jsonPayload.tenant="globex"' \\
  --project "$PROJECT" --limit 1 --format='value(jsonPayload.doc_key,jsonPayload.pages,jsonPayload.chunks,jsonPayload.embedded)'

"""

def step_03_prove_it_on_the_lane_one_small_pdf_four_pa(session):
    """Run Prove it on the lane: one small PDF, four pages at this checkpoint.

    The amendment Act is four pages and globex does not hold it, so ingesting it there is a fresh source, one Document AI request, and a few paise. Then read the worker's line for it, which carries the page count as pages.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (costs about four pages of Document AI).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_which_reader_does_your_lane_have),
        ('source_12', step_02_count_the_corpus_rs_0),
        ('source_14', step_03_prove_it_on_the_lane_one_small_pdf_four_pa),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
