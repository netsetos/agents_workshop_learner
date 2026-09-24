"""Demo 1 of 3: tenant membership, refusals and one source across three stores.

HTML sequence: section 3 (Tenant), then section 4 (Source).
Prerequisite: setup/prepare.py. Run/Debug this file with rag-shell-venv.
Steps: write the kit roster -> compare member/outsider/no-token requests ->
inspect Firestore membership -> compare Storage, API and the source ledger.
Purpose: distinguish Cloud Run admission from tenant authorization and prove
that the Documents UI's source row refers to the indexed Storage generation.
Effects: the HTML's roster command adds memberships and golden-tenant policies;
one member query can incur retrieval/generation costs. Other reads are read-only.
Expected: 200, API JSON 403, Cloud Run HTML 403; matching source generations.
Full responses are saved under workshop_demos/results, with no bearer tokens.
"""
import os
import sys

from workshop_helpers.lesson31 import LessonCloud, require
from workshop_helpers.session import DemoSession

REPEAT = False
TENANT = "acme"
SOURCE = "hr_policy_2026.md"
QUESTION = "What is the notice period?"


def establish_roster(cloud):
    """HTML 3: use the kit's actual roster command, including its documented policies."""
    session = cloud.session
    session.command([sys.executable, "commands/lane.py", "--project", session.config.project,
                     "roster", "--tenant", TENANT, "--members", os.environ["ME"]])


def compare_access(cloud):
    """HTML 3: identical bodies, three identities; the refusal body identifies the gate."""
    body = {"query": QUESTION, "tenant_id": TENANT, "stream": False}
    member = cloud.request("member", "/v1/query", body)["json"]
    require(isinstance(member, dict) and member.get("answerable") and member.get("citations"),
            "The member was admitted but no cited answer was produced. Check the seeded HR fixture.")
    outsider = cloud.request("outsider", "/v1/query", body, identity="outsider", expected_status=403)
    require(outsider["json"] == {"detail": "not a member of this tenant"},
            "The outsider did not reach the expected roster refusal. Check its Cloud Run invoker role and roster.")
    anonymous = cloud.request("anonymous", "/v1/query", body, identity="none", expected_status=403)
    require("html" in anonymous["content_type"].lower() and anonymous["json"] is None,
            "The unauthenticated refusal was not the expected Cloud Run HTML response; inspect service admission.")


def inspect_membership(cloud):
    """HTML 3: read the forward roster, UI reverse lookup and tenant settings."""
    from google.cloud.firestore_v1.base_query import FieldFilter
    members = cloud.rows("tenants/acme/members")
    email = os.environ["ME"].lower()
    require(email in members, "The operator is missing from ACME's roster after the roster command.")
    matches = cloud.db.collection_group("members").where(filter=FieldFilter("email", "==", email)).limit(1).get(retry=None, timeout=15)
    tenants = [row.reference.parent.parent.id for row in matches]
    require(tenants, "No membership reverse lookup result for this operator.")
    settings = cloud.document("tenant_settings/acme")
    require(settings.get("retrieval_backend") == "vector", "ACME's vector pin changed; rerun preparation deliberately.")
    cloud.save("membership", {"members": members, "reverse_lookup": tenants, "settings": settings})
    print("Roster:", list(members), "| first reverse lookup:", tenants, "| settings:", settings)
    if tenants != [TENANT]:
        print("This operator belongs to another tenant too; the UI's limit(1) may select it. Select an ACME member for the UI upload.")


def trace_source(cloud):
    """HTML 4: consume complete responses before printing selected rows; no head/pipefail."""
    from services.ingest.idempotency import source_id_for
    objects = [{"name": b.name, "generation": str(b.generation), "size": b.size}
               for b in cloud.bucket.list_blobs(prefix=TENANT + "/", retry=None, timeout=15)]
    cloud.save("bucket_objects", objects)
    print("Tenant objects:", len(objects), "| first five:", objects[:5])
    blob = cloud.bucket.blob(f"{TENANT}/{SOURCE}")
    blob.reload(retry=None, timeout=15)
    api = cloud.request("sources_api", "/v1/sources?tenant_id=acme")["json"]
    require(isinstance(api, dict) and api.get("tenant_id") == TENANT, "Unexpected sources response.")
    require(all(row["name"].startswith(TENANT + "/") for row in api["sources"]), "Cross-tenant source appeared in the API.")
    source = next((r for r in api["sources"] if r["name"] == blob.name), None)
    ledger = cloud.rows("sources", tenant_id=TENANT)
    cloud.save("source_ledger", ledger)
    row = ledger.get(source_id_for(TENANT, blob.name), {})
    require(source and row, "HR source missing from the API or ledger; seed/index the lesson corpus first.")
    require(row.get("status") == source["status"] == "indexed"
            and str(blob.generation) == str(source["generation"]) == str(row.get("generation"))
            and row.get("doc_key") == source["doc_key"]
            and row.get("gcs_uri") == f"gs://{cloud.bucket.name}/{blob.name}",
            "Storage/API/ledger disagree. Wait for ingestion or inspect reconciliation in lesson 4.4.")
    print("Same source:", blob.name, "| generation:", blob.generation, "| version:", row["doc_key"])
    print("Source ledger:", row)


def demonstrate(session):
    """Follow HTML sections 3 and 4; stop at a failed contract, not at every code box."""
    require(not session.state.get("lesson31_closed"), "Run was cleaned up; start a new lesson session.")
    cloud = LessonCloud(session)
    establish_roster(cloud)
    compare_access(cloud)
    inspect_membership(cloud)
    trace_source(cloud)


def main():
    """Run this complete experiment; set breakpoints in its four named steps."""
    with DemoSession(__file__, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
