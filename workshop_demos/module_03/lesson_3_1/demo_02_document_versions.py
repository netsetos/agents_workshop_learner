"""Demo 2 of 3: the same bytes produce two tenant-scoped version keys (HTML 5).

First complete demo 1. In the deployed UI as an ACME member: Documents -> Upload
-> choose evals/demo/gratuity_amendment_2026.md from THIS checkout -> Index
documents. Then Run this file. It verifies those bytes, uploads the same file
to Zeta, waits for each exact Storage generation and reads both version claims.
ACME_UPLOAD='operator' is an explicit all-Python alternative; it does not prove
the UI's identity or tenant selection. Existing identical fixtures are reused;
different existing bytes are never overwritten. Uploads remain after cleanup.
Expected: equal SHA-256 suffixes, distinct acme_/zeta_ keys, indexed claims and
nonempty current chunks. Counts come from your lane, not a hard-coded example.
"""
from workshop_helpers.lesson31 import LessonCloud, require
from workshop_helpers.session import DemoSession

REPEAT = False
ACME_UPLOAD = "ui"  # Change to "operator" only for the documented Python-only variant.
FILENAME = "gratuity_amendment_2026.md"


def upload_same_bytes(cloud):
    """Check ACME first so a missing UI step cannot leave an unexplained Zeta-only run."""
    require(ACME_UPLOAD in {"ui", "operator"}, "ACME_UPLOAD must be 'ui' or 'operator'.")
    path = cloud.session.config.kit_root / "evals/demo" / FILENAME
    data = path.read_bytes()  # Binary read preserves the SHA, including line endings.
    print("Fixture:", path, "| ACME upload mode:", ACME_UPLOAD)
    versions = [cloud.fixture("acme", FILENAME, data, upload=ACME_UPLOAD == "operator"),
                cloud.fixture("zeta", FILENAME, data, upload=True)]
    cloud.session.state["lesson31_versions"] = versions
    cloud.session.save()  # Later files use exactly these version keys, not today's latest document.
    cloud.save("expected_versions", versions)
    print("SHA-256:", versions[0]["sha256"])
    return versions


def inspect_indexed_versions(cloud, versions):
    """Upload completion is not indexing; wait for matching ledger, claim and chunks."""
    for version in versions:
        observed = cloud.wait_indexed(version)
        claim = observed["claim"]
        print(version["tenant"], version["doc_key"], claim["status"], claim["chunks"], claim["gcs_uri"])
        cloud.worker_logs(version)
    require(versions[0]["sha256"] == versions[1]["sha256"]
            and versions[0]["doc_key"] != versions[1]["doc_key"], "Expected equal bytes with distinct tenant keys.")
    print("Version proof: same content hash; separate claims for acme and zeta.")


def demonstrate(session):
    """Execute the complete section 5 experiment in order, including its UI prerequisite."""
    require(not session.state.get("lesson31_closed"), "Run was cleaned up; start a new lesson session.")
    cloud = LessonCloud(session)
    versions = upload_same_bytes(cloud)
    inspect_indexed_versions(cloud, versions)


def main():
    """Run after the ACME UI upload; a failed attempt can be retried without new uploads."""
    with DemoSession(__file__, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
