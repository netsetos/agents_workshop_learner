"""Lesson 8.3: demo 01 pii scan and findings

Upload the synthetic PII note and inspect its findings in Firestore and the DLP UI.

Run order inside this file:
1. Do it (source window 8)
2. Do it: the records (source window 10)
3. Do it: the DLP tab (source window 12)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """cat > "$HOME/lesson83_vendor_note.md" <<EOF
# Vendor onboarding note

Synthetic note for lesson 8.3. Every identifier below is the kit's invented, format-valid sample (evals/README.md).

Vendor contact: Asha Verma, mobile +919876543210.
PAN AAAPZ1234C, GSTIN 27AAAPZ1234C1ZV, Aadhaar 2234 5678 9012.

Written for lesson 8.3 at $(date -u +%FT%TZ).
EOF
make ingest-one PROJECT="$PROJECT" TENANT=acme FILE="$HOME/lesson83_vendor_note.md"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a small note with the kit's synthetic identifiers, uploaded to acme).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_the_records(session):
    """Run Do it: the records at this checkpoint.

    Do it: the records

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acme's newest findings records; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    names = {s.get("doc_key"): s.get("name") for s in (d.to_dict() for d in db.collection("sources").stream())}
    rows = [d.to_dict() for d in db.collection("dlp_findings").order_by("scanned_at", direction=firestore.Query.DESCENDING).limit(50).stream()]
    acme = [r for r in rows if r.get("tenant_id") == "acme"]
    for r in acme[:4]:
        types = sorted({f["info_type"] for f in r["findings"]})
        print(f"  {names.get(r.get('doc_key')) or r.get('doc_key') or r.get('chunk_id')}: {r['count']} finding(s), {', '.join(types)}")
    print("one finding, whole:", acme[0]["findings"][0] if acme else "none yet")

# Original CLI workflow for step_03_the_dlp_tab.
COMMANDS_03 = """gcloud run services describe documind-admin --region "$REGION" --project "$PROJECT" --format='value(metadata.name)' >/dev/null 2>&1 \\
  && echo "https://documind-admin-$NUMBER.$REGION.run.app   <- open in your browser, then the DLP tab" \\
  || echo "documind-admin is not deployed on this lane"

"""

def step_03_the_dlp_tab(session):
    """Run Do it: the DLP tab at this checkpoint.

    The console sits behind IAP and admits only the addresses the lane was deployed with as ADMIN_EMAILS. If it answers 403 - Admins only, your address is not among them; the cell above has already read the records the tab draws.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the admin console's address).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    manual_checkpoint("Open the deployed admin DLP tab and inspect the synthetic note's findings. Type done to compare them with the source fields printed next.")
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_example),
        ('source_10', step_02_the_records),
        ('source_12', step_03_the_dlp_tab),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
