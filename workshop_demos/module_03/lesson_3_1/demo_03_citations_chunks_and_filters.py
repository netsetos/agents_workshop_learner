"""Demo 3 of 3: citations point to real chunks, with tenant and locator contracts.

HTML order: section 6 (Markdown/PDF answers and locators), then section 7
(accepted/refused filters and the twin chunk sets from demo 2), then the
whitespace/root-object contract checks advertised by the lesson checklist.
Prerequisites: both earlier demos and their saved exact-version evidence.
Effects: four valid API questions incur retrieval/generation work; other cloud
operations are reads. The root-object check is LOCAL validation, not a poison
upload, and makes no claim that a live worker logged ingest_poison.
Expected: fresh vector retrieval, cited IDs resolving to current ACME rows,
equal chunk hashes but disjoint tenant IDs, and rejection of a tenant filter.
Finish with setup/finish.py even if an observation fails. Read README.md.
"""
from collections import Counter

from workshop_helpers.lesson31 import LessonCloud, require
from workshop_helpers.session import DemoSession

REPEAT = False
QUESTIONS = [
    ("markdown", "What is the notice period for a confirmed E3?", "hr_policy_2026.md"),
    ("pdf", "What does the Code on Wages say about the payment of wages?", "code_on_wages_2019.pdf"),
]


def inspect_citations(cloud):
    """HTML 6: ask both source questions and resolve each citation back to Firestore."""
    for label, question, expected_source in QUESTIONS:
        answer = cloud.query(label + "_answer", question)
        require(answer.get("answerable") and answer.get("citations"), f"{label}: no cited answer; inspect the saved response and seeded corpus.")
        require(any(c["source_uri"].endswith("/" + expected_source) for c in answer["citations"]),
                f"{label}: the expected lesson source was not cited. This live observation did not reproduce the example.")
        print(question, "\n", answer["answer"])
        for citation in answer["citations"]:
            row = cloud.document("chunks/" + citation["chunk_id"])
            require(row.get("tenant_id") == "acme" and row.get("current") is True
                    and row.get("source_uri") == citation["source_uri"], "Citation did not resolve to its current ACME chunk.")
            require(citation.get("page") == (row.get("page_start") or row.get("page")), "Citation page disagrees with the stored chunk.")
            print("  cited:", citation["chunk_id"], "page", citation.get("page"), "locator", row.get("locator"))


def inspect_locators(cloud):
    """HTML 6: section labels locate Markdown passages; page numbers locate PDF passages."""
    for _, _, filename in QUESTIONS:
        rows = cloud.chunks("acme", filename)
        require(rows, f"No current chunks for {filename}; ingest the lesson fixture first.")
        cloud.save(filename.replace(".", "_") + "_locators", rows)
        print(filename, "->", len(rows), "current chunks")
        for cid, row in sorted(rows.items())[:5]:
            print(" ", cid, "locator", row.get("locator"), "page_start", row.get("page_start"), "section", row.get("section"))
        require(all(row.get("locator") for row in rows.values()), "Some chunks lack locators; inspect the ingest schema/backfill.")
        if filename.endswith(".pdf"):
            require(all(isinstance(row.get("page_start"), int) and row["page_start"] > 0 for row in rows.values()), "PDF rows need positive page_start values.")


def compare_filters(cloud):
    """HTML 7: an allowed field can match nothing; tenant_id is never an allowed filter."""
    question = QUESTIONS[0][1]
    text = cloud.query("filter_text", question, filters={"kind": "text"})
    require(text.get("answerable") and text.get("citations"), "kind=text returned no cited answer.")
    require(all(c.get("kind", "text") == "text" for c in text["citations"]), "A non-text citation bypassed kind=text.")
    policy = cloud.query("filter_policy", question, filters={"doc_type": "policy"}, fresh=False)
    require(policy.get("cache_hit") == "none", "Filter example unexpectedly used the answer cache.")
    # The stock writer stamps doc_type=unknown. A customized corpus may legitimately
    # have policy rows, in which case the HTML's empty-match example needs new data.
    require(not policy.get("answerable") and not policy.get("citations"),
            "doc_type=policy matched your corpus; the stock lesson expects unknown. Inspect saved filter_policy.json.")
    refused = cloud.request("filter_tenant_refused", "/v1/query",
                            {"query": question, "tenant_id": "acme", "stream": False, "filters": {"tenant_id": "zeta"}},
                            expected_status=400)
    require(isinstance(refused["json"], dict) and "tenant_id" in str(refused["json"].get("detail", "")),
            "Expected a validation refusal naming the forbidden tenant_id filter.")


def compare_tenant_chunks(cloud):
    """HTML 7: use demo 2's exact keys, then compare IDs and the multiset of text hashes."""
    versions = cloud.session.state["lesson31_versions"]
    groups = [cloud.wait_indexed(v)["chunks"] for v in versions]
    acme, zeta = groups
    require(not (set(acme) & set(zeta)), "Identical tenant chunk IDs would overwrite each other's payloads.")
    for version, rows in zip(versions, groups):
        require(all(cid.startswith(version["tenant"] + ":" + version["sha256"] + "#") for cid in rows),
                "Chunk IDs do not carry this tenant and version SHA.")
        require(all(row.get("chunk_hash") for row in rows.values()), "A current chunk is missing its content hash.")
    require(Counter(r["chunk_hash"] for r in acme.values()) == Counter(r["chunk_hash"] for r in zeta.values()),
            "Same bytes did not produce the same chunk-hash multiset; inspect chunker/schema differences.")
    cid, row = next(iter(acme.items()))
    print("Chunk proof:", len(acme), len(zeta), "rows; no IDs shared; same hashes.")
    print("Example ID:", cid)
    for key in ("tenant_id", "doc_key", "current", "locator", "chunk_hash", "embedding_model", "embedding_task_type", "schema_version"):
        print(f"{key:22}", row.get(key))
    print("Vector dimensions:", len(row.get("embedding", [])))


def prove_local_contract_rules():
    """Call the actual kit validators; rewrapping changes bytes but preserves chunk identity."""
    from pydantic import ValidationError
    from services.ingest.contracts import IngestMessage, chunk_hash, sha256_of
    original, rewrapped = "Notice period is ninety days.", " Notice\nperiod  is ninety\tdays. "
    require(sha256_of(original.encode()) != sha256_of(rewrapped.encode()), "The example must change file bytes.")
    require(chunk_hash(original) == chunk_hash(rewrapped), "Rewrapped text should keep its chunk hash.")
    require(chunk_hash(original) != chunk_hash("Notice period is thirty days."), "Changed words should change the chunk hash.")
    event = dict(bucket="example-uploads", name="acme/note.md", size=1, contentType="text/markdown", generation="1")
    require(IngestMessage(**event).tenant_id == "acme", "Tenant should derive from the object prefix.")
    try:
        IngestMessage(**{**event, "name": "note.md"})
    except ValidationError as error:
        require("tenant prefix" in str(error), "Validator rejected the event for an unexpected reason.")
        print("Local contracts: rewrapped chunk hash unchanged; root-level object rejected.")
    else:
        raise RuntimeError("A root-level object unexpectedly passed validation.")


def demonstrate(session):
    """Follow sections 6–7 and then the two pure checklist proofs."""
    require(not session.state.get("lesson31_closed"), "Run was cleaned up; start a new lesson session.")
    cloud = LessonCloud(session)
    inspect_citations(cloud)
    inspect_locators(cloud)
    compare_filters(cloud)
    compare_tenant_chunks(cloud)
    prove_local_contract_rules()


def main():
    """Run this final demo, then run setup/finish.py to restore saved settings."""
    with DemoSession(__file__, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
