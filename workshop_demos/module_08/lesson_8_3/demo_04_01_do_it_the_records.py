"""Lesson 8.3 / s4: The findings: types and offsets, in Firestore and in the DLP tab

Summary and purpose:
Do it: the records

HTML instruction: bash — run in the operator shell, in the kit (acme's newest findings records; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: acme/lesson83_vendor_note.md: 5 finding(s), INDIA_AADHAAR_INDIVIDUAL, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PERSON_NAME, PHONE_NUMBER
  acme/inv_2026_0412.md: 4 finding(s), EMAIL_ADDRESS, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PHONE_NUMBER
one finding, whole: {'info_type': 'PERSON_NAME', 'likelihood': 'LIKELY', 'offset': 159, 'chunk_id': 'acme:SHA#0'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html#L471

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
