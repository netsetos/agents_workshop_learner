"""Lesson 4.1 / s6: The batch lane: the 250-page decision, the queued claim, the job

Summary and purpose:
The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker. The corpus has no PDF over 250 pages, so the drill makes one: the CGST Act (236 pages) and the IT Act (34) joined with pypdf on your machine, at no cost. Uploading it costs nothing either, and that is the point of the first half: the worker counts 270 pages, writes the queued claim, answers 200, and no page has been sent to Document AI. The second half is where the money goes. When the job is declared, the worker starts it at once and it parses all 270 pages: about Rs 34 on the OCR processor, about Rs 230 on the Layout Parser (at the list prices lesson 3.2 quoted and Rs 85 to the dollar), plus a few rupees of embeddings for roughly six hundred windows. When the job is not declared, the claim simply waits, and make queued shows it. Decide before you upload.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the join is free; the upload starts the paid parse if the job is declared)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_read_the_lane_rs_0
Expected observation: bundle pages: 270
>> queued: pages, consumer: 270	documind-ingest-batch started (run requested); the hourly schedule backstops it
1 queued document(s)
  acme_3ff3f2ac3237...  gs://documind-ai-YOUR-ID-uploads/acme/cgst_it_bundle.pdf  pages=270  generation=1758543112345678

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L730

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
from pypdf import PdfReader, PdfWriter
w = PdfWriter()
for path in ("evals/corpus/acme/cgst_act_2017.pdf", "evals/corpus/acme/it_act_2000.pdf"):
    for page in PdfReader(path).pages:
        w.add_page(page)
with open("/tmp/cgst_it_bundle.pdf", "wb") as f:
    w.write(f)
print("bundle pages:", len(PdfReader("/tmp/cgst_it_bundle.pdf").pages))
PY

SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gcloud storage cp /tmp/cgst_it_bundle.pdf "gs://$PROJECT-uploads/acme/cgst_it_bundle.pdf"
for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event=\\"ingest_queued_batch\\" AND timestamp>=\\"$SINCE\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.pages,jsonPayload.consumer)')"
  [ -n "$LINE" ] && { echo ">> queued: pages, consumer: $LINE"; break; }
done
make queued PROJECT=$PROJECT
"""


def demonstrate(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker. The corpus has no PDF over 250 pages, so the drill makes one: the CGST Act (236 pages) and the IT Act (34) joined with pypdf on your machine, at no cost. Uploading it costs nothing either, and that is the point of the first half: the worker counts 270 pages, writes the queued claim, answers 200, and no page has been sent to Document AI. The second half is where the money goes. When the job is declared, the worker starts it at once and it parses all 270 pages: about Rs 34 on the OCR processor, about Rs 230 on the Layout Parser (at the list prices lesson 3.2 quoted and Rs 85 to the dollar), plus a few rupees of embeddings for roughly six hundred windows. When the job is not declared, the claim simply waits, and make queued shows it. Decide before you upload.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the join is free; the upload starts the paid parse if the job is declared).
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
