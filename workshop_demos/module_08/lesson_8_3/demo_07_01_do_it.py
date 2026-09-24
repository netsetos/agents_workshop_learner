"""Lesson 8.3 / s7: The audit trail: the events in the retention bucket

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_clean_up_the_candidate_s_tag
Expected observation: YYYY/MM/DD/acme/doc.upload-UUID1.json
  YYYY/MM/DD/acme/dlp.finding-UUID2.json
  YYYY/MM/DD/acme/doc.upload-UUID3.json
    id: "UUID"
    ts: "YYYY-MM-DDTHH:MM:SS.ssssss+00:00"
    action: "dlp.finding"
    actor: {"tenant_id": "acme", "email": "system:ingest"}
    target: {"type": "document", "id": "acme_SHA", "tenant_id": "acme"}
    meta: {"types": ["INDIA_AADHAAR_INDIVIDUAL", "INDIA_GST_INDIVIDUAL", "INDIA_PAN_INDIVIDUAL", "PERSON_NAME", "PHONE_NUMBER"], "count": 5}
retention 157680000 s (5 years), locked False
delete refused: 403 Forbidden

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html#L660

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import datetime, json, os
    from google.cloud import storage
    p = os.environ["PROJECT"]
    client = storage.Client(project=p)
    bucket = client.get_bucket(f"{p}-audit")
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    blobs = sorted(bucket.list_blobs(prefix=f"{day}/acme/"), key=lambda b: b.time_created)
    for b in blobs[-3:]:
        print(" ", b.name)
    finding = next((b for b in reversed(blobs) if "/dlp.finding-" in b.name), None)
    for k, v in (json.loads(finding.download_as_text()).items() if finding else [("dlp.finding", "none today")]):
        print(f"    {k}: {json.dumps(v)}")
    rp = bucket.retention_period or 0
    print(f"retention {rp} s ({rp / 31536000:.0f} years), locked {bucket.retention_policy_locked}")
    if finding and rp:                                   # only against a policy: the delete must be refused
        try:
            finding.delete()
            print("DELETED: this bucket did not enforce its retention policy")
        except Exception as e:
            print("delete refused:", getattr(e, "code", ""), type(e).__name__)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
