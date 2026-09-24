# Lesson 3.1: three complete demos

**Summary:** follow one document through tenant, source, version, page and chunk contracts. Each file is a complete experiment with short, named functions you can step through in PyCharm or VS Code. These replace the thirteen extracted command fragments.

The sequence and fixtures follow the [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html), reviewed at blob `9be3b915fa81df25778e35f6eaa825f0b365ec21`. The source is private; this README and the Python docstrings supply the runnable instructions in the public learner kit. The [lesson map](lesson_map.json) accounts for all 36 code windows and additional prerequisites in prose.

## Folder and run order

```text
workshop_demos/
  setup/                         # shared configuration, authentication and helpers
    config/settings.local.json   # your project; Git ignores this file
    workshop_helpers/lesson31.py # repeated HTTP, Storage, Firestore and wait operations
  module_03/lesson_3_1/
    setup/prepare.py             # once before the demos
    demo_01_tenant_and_source_contracts.py
    demo_02_document_versions.py
    demo_03_citations_chunks_and_filters.py
    setup/finish.py              # after success OR failure
    README.md
    lesson_map.json
```

| Run | File | Main HTML heading and purpose |
|---|---|---|
| Prepare | [setup/prepare.py](setup/prepare.py) | Section 2: save the previous backend; pin ACME to vector; ensure fresh answers |
| Demo 1 | [demo_01_tenant_and_source_contracts.py](demo_01_tenant_and_source_contracts.py) | Sections 3-4: **Tenant**, then **Source** |
| Demo 2 | [demo_02_document_versions.py](demo_02_document_versions.py) | Section 5: **Version: the bytes decide** |
| Demo 3 | [demo_03_citations_chunks_and_filters.py](demo_03_citations_chunks_and_filters.py) | Sections 6-7: **Page and section**, then **Chunk** and filters |
| Finish | [setup/finish.py](setup/finish.py) | Restore the settings saved during preparation |

Do not use Run All: demo 2 has an explicit UI upload checkpoint. A failed file does not satisfy the next file's prerequisite. A completed file requires `REPEAT=True` for a deliberate rerun; a failed file can simply be retried after fixing its cause. Cleanup remains runnable after failure.

## One-time workstation setup

1. Open the learner checkout `/home/user/deploy_module_rag` in your IDE.
2. Choose interpreter `/home/user/rag-shell-venv/bin/python`. The unrelated project `.venv` may have no Google libraries. No terminal activation or exported variables are needed for IDE runs.
3. Run [../../setup/bootstrap.py](../../setup/bootstrap.py) from that interpreter. Verify `project`, `cloud_run_region`, `uploads_bucket` and `tenant_id: "acme"` in its local settings file. This installs the helper package; imports work from any working directory.
4. If packages are missing, run [../../setup/install_dependencies.py](../../setup/install_dependencies.py) with the operator profile. Expired Python ADC is repaired with [../../setup/authenticate.py](../../setup/authenticate.py); gcloud login alone does not refresh ADC.
5. The lane must already have its API, ingest worker, Firestore database, uploads bucket, deployed Vector Search index and seeded HR/PDF fixtures. These demos do not create the infrastructure. The operator needs the same permissions as the HTML's operator shell, including impersonation, Storage/Firestore access, log reads and any preparation-time Cloud Run update.

Preparation saves ACME's current backend. If the API's `SEMANTIC_CACHE` is `on`, it temporarily sets it to `off` by creating a Cloud Run revision. **This cache setting affects every tenant using that API.** `DISABLE_ANSWER_CACHE=False` makes preparation refuse an enabled cache instead. Preparation rejects split traffic or a service pinned to an older revision. Finish restores the original cache value and backend; it does not delete cache entries.

Keep `workshop_demos/results/`: it contains the original settings needed for restoration. Do not delete the checkout while a lesson is active. If you used the old thirteen-file sequence, the new `setup/finish.py` can restore its saved backend. Then set `LESSON = "3.1"` in [../../setup/start_new_session.py](../../setup/start_new_session.py) and run it before beginning this sequence.

## Demo 1: tenant and source

`establish_roster()` calls the actual kit `commands/lane.py roster`. Like the HTML's `make roster`, it adds your operator membership and the golden service-account memberships/policies; those fixture settings remain after the lesson.

`compare_access()` sends the same notice-period question as a member, an outsider and an unauthenticated caller. Expected: a cited answer with HTTP 200; API JSON 403 saying `not a member of this tenant`; Cloud Run HTML 403. The two refusals are different gates. The outsider fixture must be admitted by Cloud Run but absent from ACME's roster.

`inspect_membership()` reads the roster, UI reverse lookup and tenant settings. If your email belongs to several tenants, the UI's first membership may differ; use an ACME UI session for the next demo. `trace_source()` compares `acme/hr_policy_2026.md` in Storage, `/v1/sources` and Firestore. It checks generation and version key, rather than just printing them. Full JSON is consumed and saved before the console is shortened, avoiding broken-pipe failures from `head`.

## Demo 2: same bytes, two tenants

If this exact ACME fixture is already indexed and has not been overwritten, reuse it; do not upload another identical generation. For a new fixture, before Run: as an ACME member in the deployed UI, open **Documents -> Upload**, select **the exact checkout file** `evals/demo/gratuity_amendment_2026.md`, and click **Index documents**. The script verifies the ACME object's bytes before doing anything to Zeta. A missing UI upload produces a direct instruction rather than a `None` claim error.

For a Python-only demonstration, set `ACME_UPLOAD = "operator"` in demo 2. This uploads both tenants as the operator and demonstrates the version contract, **without proving the UI service account or UI tenant selection**. The default `"ui"` mode preserves the lesson sequence. Neither mode overwrites a different existing file; inspect a mismatch, including line endings, before proceeding.

`upload_same_bytes()` reads the fixture as bytes, computes the kit's SHA-256/version keys and retains each Storage generation. Existing identical objects are reused to avoid an unnecessary duplicate-ingest event. `inspect_indexed_versions()` waits for that exact source generation and content key, an indexed claim, and the expected count of current chunks. Missing or queued claims are observations to wait for, not success. The poll deadline defaults to shared `ingest_wait_seconds`; each SDK read also has a bounded timeout.

Expect equal hash suffixes and distinct `acme_<sha>`/`zeta_<sha>` keys. Do not expect a universal chunk count. Logs are filtered by tenant, version key **and generation**, so another document's latest success cannot pass the example. Old logs may have expired; matching ledger, claim and chunks are the primary evidence. An identical reupload can be acknowledged as a duplicate without advancing the ledger. If that happened, the exact-generation check intentionally times out; inspect lesson 4.4 reconciliation before rerunning. A claim describes content and can retain an older upload generation; the source ledger describes the current object generation.

## Demo 3: citations, chunks and filters

`inspect_citations()` asks both original questions: the confirmed E3 notice period and payment of wages under the Code on Wages. It first waits out any remaining part of the API's 60-second tenant-settings cache after the backend pin. It rejects answer-cache hits and requires actual Vector Search contribution, then checks that citations resolve to current ACME chunks with the same source/page. Merely pinning a backend would allow an old cached answer to look like a new retrieval.

`inspect_locators()` shows Markdown section/locator fields and PDF page numbers. `compare_filters()` demonstrates `kind=text`, the stock corpus's empty `doc_type=policy` match, and a rejected `tenant_id=zeta` filter. A customized corpus with real `policy` rows will stop at the stock empty-match expectation; inspect the evidence rather than treating that as an API bug.

`compare_tenant_chunks()` uses demo 2's saved exact versions. It checks separate tenant IDs and equal **multisets** of chunk hashes, so duplicate or missing rows are not hidden. `prove_local_contract_rules()` calls the actual kit's `chunk_hash()` and `IngestMessage`: whitespace rewrapping preserves a chunk hash, changing words changes it, and an object without a tenant prefix is rejected. This final validator example is local. Observing a live worker's `ingest_poison` log remains the HTML's separate cloud checklist exercise; no poison file is uploaded by this demo.

## Evidence, cleanup and testing

Each function explains its purpose in its docstring. Repeated I/O is in [../../setup/workshop_helpers/lesson31.py](../../setup/workshop_helpers/lesson31.py); lesson-specific questions and comparisons stay visible in the three demos. Put breakpoints inside those functions and inspect their ordinary Python dictionaries.

Complete responses and observations live in the active attempt directory printed by each run. A timeout keeps the last ledger/claim/chunk observation. Fix missing fixture/index/IAM issues before retrying; do not extend timeouts to conceal a failed worker. Cleanup attempts both restorations even if one fails, and keeps pending flags so you can retry it. Uploads, roster fixture entries and evidence remain.

Offline tests cover stale generations, missing/queued claims, cache/fallback rejection, upload safeguards, refusal handling and recoverable setup/cleanup. The source mapping and all scripts are checked without credentials. **These are not recorded live GCP results:** your workstation run verifies IAM, asynchronous indexing and model responses on your own lane.
