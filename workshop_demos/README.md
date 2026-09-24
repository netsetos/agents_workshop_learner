# Lesson 4.4: a runnable modular pilot

This sample demonstrates **retiring a missing source and restoring its original bytes without embedding them again**. Each demo is a separate Python file you can Run or Debug in PyCharm or VS Code on your Cloud Workstation.

Use your existing learner kit and `rag-shell-venv`. The sample supplies the lesson files and reusable helpers; your existing kit supplies the real reconciliation and retirement functions.

## Where this lives in the repository

The source is **`agents_workshop/deploy/workshop_demos/`**. This is a new directory inside the existing runnable kit. `lessons/` continues to hold the authored course pages. The normal kit publisher copies `deploy/` to the learner repository root, so learners receive **`workshop_demos/`** beside `services/`, `commands/` and `shared/`.

You can test the pilot directly from an authoring-repository branch: open that checkout's `deploy/` directory in your IDE and follow the setup below. `kit_root: "auto"` works in both the authoring checkout and the published learner kit. A branch in the authoring repository does not by itself update your learner clone; use the authoring branch to test before the normal reviewed merge and publish.

After publication, the learner workstation layout is:

```text
/home/user/deploy_module_rag/
├── services/ingest/                 existing kit: reconcile.py, idempotency.py, managed.py
├── shared/                         existing kit code
└── workshop_demos/                  this sample
    ├── README.md
    ├── setup/
    │   ├── bootstrap.py             install helpers in the selected interpreter
    │   ├── authenticate.py          refresh Python ADC when needed
    │   ├── check_setup.py           check live access without modifying cloud resources
    │   ├── update_kit.py            optional, explicit fast-forward of the learner clone
    │   ├── pyproject.toml           dependency versions and editable helper installation
    │   ├── config/
    │   │   ├── settings.example.json
    │   │   └── settings.local.json  created by bootstrap; your project settings
    │   └── workshop_helpers/
    │       ├── context.py           lazy clients and the lifetime of one demo
    │       ├── config.py            configuration and paths
    │       ├── auth.py              ADC and impersonated API tokens
    │       ├── discovery.py         serving Cloud Run revision configuration
    │       ├── api.py               health, version, uncached query calls
    │       ├── artifacts.py         separate evidence directory per run
    │       ├── kit.py               bridge to the existing kit functions
    │       ├── reconciliation.py    read evidence and produce a plan
    │       └── lifecycle.py         upload, wait, delete, restore and verify
    ├── module_04/
    │   └── lesson_4_4/
    │       ├── demo_01_reconciliation_rules.py
    │       ├── demo_02_inspect_live_tenant.py
    │       ├── demo_03_restore_round_trip.py
    │       └── recover_fixture.py   utility for an interrupted live demo
    ├── tests/
    │   ├── run_tests.py
    │   └── test_pilot.py
    └── results/                    generated locally; ignored by Git
```

The normal imports look like this:

```python
from workshop_helpers import DemoContext
from workshop_helpers.reconciliation import ReconcileInspector, print_plan

def main():
    with DemoContext("02", live=True) as demo:
        report = ReconcileInspector(demo).inspect()
        demo.artifacts.save("live_plan", report)
        print_plan(report)

if __name__ == "__main__":
    main()
```

The lesson shows the experiment. Helpers handle repeated plumbing. Installing the helper package once makes these imports work regardless of the IDE's working directory; individual demos need no `sys.path` edits or repeated exports.

## Start in PyCharm

1. Open `/home/user/deploy_module_rag` as the project after the pilot is published to the learner kit. To test the authoring branch first, open `<authoring-checkout>/deploy` instead.
2. In the project's Python interpreter settings, select the existing interpreter `/home/user/rag-shell-venv/bin/python`. Check each Run/Debug configuration uses it too. Your earlier `/home/user/deploy_module_rag/.venv/bin/python` was a different environment.
3. Run `workshop_demos/setup/bootstrap.py` once. It installs with **that running interpreter's** `python -m pip`, then keeps the helper code editable. It creates `settings.local.json` and copies the active `gcloud` project into it if available. Existing settings are preserved. For an offline-only trial, set `INSTALL_LIVE_DEPENDENCIES=False` before running bootstrap.
4. Open `setup/config/settings.local.json`. Confirm `project` is your project, `cloud_run_region` is `asia-south1`, and `tenant_id` is `acme`. `kit_root: "auto"` means the parent of `workshop_demos`; set an absolute path if you extracted elsewhere. An empty uploads bucket is resolved as `<project>-uploads`.
5. Run `demo_01_reconciliation_rules.py`. It needs no GCP login. Then run `tests/run_tests.py` for the offline checks.
6. If Python ADC has expired, Run `setup/authenticate.py`, follow the URL, and paste the verification code into its Run console. Then Run `setup/check_setup.py`.
7. Run demo 02, followed by demo 03. Right-click a file and choose Run, or put a breakpoint in `main()` / `run_round_trip()` and choose Debug. There are no required command-line arguments.

Activating a venv in a terminal does not change an existing PyCharm Run configuration. Selecting the correct interpreter replaces `source ~/rag-shell-venv/bin/activate` for these IDE runs.

Python ADC and the `gcloud` CLI account are separate. `authenticate.py` repairs ADC. If a `gcloud` command itself needs a fresh login, use the workstation's normal `gcloud auth login --no-launch-browser` flow. The API token helper impersonates `documind-ui-sa@<project>.iam.gserviceaccount.com`, as in your earlier shell code. Existing Cloud Run invoker and service-account impersonation permissions still apply. See Google's [workstation ADC documentation](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment).

## What to run and what it proves

| File | Reads/writes | What you learn |
|---|---|---|
| `demo_01_reconciliation_rules.py` | Local simulated inputs only | The real planner's seven decisions; drift is 3 in this controlled example. |
| `demo_02_inspect_live_tenant.py` | Reads GCS and Firestore; downloads bytes only when a hash decision is needed | The real tenant's proposed actions and the claim behind each queued decision. No actions are applied. |
| `demo_03_restore_round_trip.py` | Creates, deletes and restores one unique test object; retires its ledger/chunks and configured mirror entries | Same bytes return under a new object generation; the document key stays the same, all N chunks are reused and none are embedded again. |

Demo 03 has `VERIFY_API=True` near the top. With that enabled it also requires an uncached answer citing the fixture before deletion, no citation to it after retirement, and a citation to it after restoration. Its first API check requires the serving API's answer cache to be off. If your API currently has `SEMANTIC_CACHE=on`, set **`VERIFY_API=False` for the first storage/ledger trial**, or use a serving demo API configured with the cache off. The sample does not change deployment settings. A ledger-only run explicitly prints that it does not verify answers.

The API URL, its audience, and the ingest mirror settings are read as JSON from the actual serving Cloud Run revision. This replaces the `svc_env`, `setenv`, `grep` and `sed` shell pipeline, using Google's [service describe command](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/describe). One revision must receive all normal service traffic; split traffic is rejected because it makes configuration ambiguous. Optional `api_revision` / `ingest_revision` settings pin the expected serving revision and detect a changed deployment.

There is no vector index creation in this lesson. Lesson 4.4 uses the deployed ingest worker and its existing stores. Vector endpoint variables are therefore not required as manually filled placeholders here.

## The live demonstration, in order

```text
Create a unique note; save its exact bytes locally
                  |
Upload original -> worker indexes generation G1 -> N current chunks
                  |
Delete only the note's live GCS object
                  |
Read plan -> retire this missing source
                  |
Apply this fixture's retirement -> chunks current=false; retain for undo
                  |
Upload the saved bytes again under the same object name
                  |
Worker restores generation G2 -> same content hash and doc_key
                  |
Assert G2 != G1, reused=N, embedded=0, fixture drift=0
```

When API verification is enabled, the answer checks happen after initial indexing, retirement and restoration. “Absent” checks that this exact fixture URI is no longer cited; it does not claim that all other tenant documents have disappeared or that every question must become unanswerable.

Each run uses a name like `acme/lesson44_<run_id>.md`. The original is saved in that run's `note.md` **before the first cloud upload**. This avoids the earlier missing `/home/user/lesson34_note.md` error. The sample never assumes that a previous lesson created a local file.

The pilot applies only the generated fixture's retirement using the existing kit's `retire_previous()`, `Mirror.retired()` and `refresh_fingerprint()` functions, plus the same source-status update as the kit CLI. It does not run tenant-wide `make reconcile ... APPLY=1`. Other drift, such as your unrelated CGST file, can remain visible in demo 02 without being applied by demo 03.

Retirement flags retained Firestore chunks and stamps their expiry; it is not an immediate purge of all retained rows. The kit's reconciler relies on current-row filtering for retrieval and retires configured managed mirror entries. This pilot follows that behavior. Restoration is performed by the real ingest worker, including its usual vector/mirror updates. The tenant corpus fingerprint is refreshed as part of the normal lifecycle.

## How reconciliation chooses an action

The planner checks current GCS object generations against `sources/` (the source ledger) and `documents/` (per-version ingest claims).

```text
For each live object:
  Matching queued claim for name + generation?
    YES -> queued: leave it to the batch lane
    NO  -> Is there a sources/ row?
             NO  -> hash the bytes (see below)
             YES -> withdrawn? -> keep the tombstone
                    retired?   -> reingest
                    same generation? -> ok
                    changed generation? -> hash the bytes

When bytes must be checked:
  Same hash as the source ledger? -> touch
  Otherwise, tenant + hash claim already indexed/superseded? -> backfill
  Otherwise, tenant + hash claim queued? -> queued
  Otherwise -> reingest

For a ledger source missing from the bucket:
  Already retired? -> no further action
  Withdrawn? -> preserve withdrawal
  Otherwise -> retire
```

| Decision | Plain meaning | Adds to drift? |
|---|---|---|
| `retire` | The source is gone from the bucket; make its indexed content non-current. | Yes |
| `reingest` | This live object needs the normal ingest path. It may have new bytes or be a previously retired source. | Yes |
| `backfill` | The content version was indexed already; recover/update its missing or out-of-date ledger metadata. | Yes |
| `touch` | The generation changed, but the bytes match the ledger; update metadata. | No |
| `queued` | A matching claim says the batch lane owns this work. | No |
| `withdrawn` | A person deliberately withdrew the source; preserve that choice. | No |
| `ok` | The live object and recorded generation agree. | No |

**Drift = retire + reingest + backfill.** `touch` can still require a metadata write even though it contributes zero drift. An apply-run's initial drift count is not proof that drift remains afterward; this demo runs a fresh plan to verify its fixture.

Queued is established by claim data, not inferred from a large filename or from slow ingestion. A claim for generation 4 does not hide a new generation 5. The kit also supports legacy queued claims with no generation, and hash-based queued decisions; demo 02 prints available matching claim evidence. A queued claim means “left to the batch lane,” not “the batch job has been verified healthy or finished.”

## Evidence, errors and recovery

Every run prints a unique results directory. Demo 03 saves `run.json`, `fixture.json`, the original `note.md`, the planner code hash, serving configuration, source snapshots and plans for each stage. With API verification enabled it saves complete answer responses, including cache status and citations. No identity tokens are written to these artifacts.

The decisive restore evidence is `source_restored.json`: the expected source, new generation, original hash/document key, `chunks=N`, `reused=N`, `embedded=0`. Worker events are supplementary; logs can be delayed or unavailable. An empty log search is not reported as a verified ingestion event. The demo creates a small note but reads the actual N; it never hard-codes an expected chunk count.

If a step fails after deletion, the `finally` block tries to leave the original object indexed again. A recovered run remains failed because recovery does not prove the missed assertions. If you force-stop the Python process, its cleanup may not execute. Open `recover_fixture.py`, paste that run's exact directory into `RUN_DIRECTORY`, and Run it. Recovery verifies project, tenant, generated object name, local hash and ownership; it refuses to overwrite a different object. Keep the results directory until recovery is complete.

A successful run intentionally leaves the restored fixture indexed for inspection. Re-running demo 03 creates a new fixture. Avoid many repeated runs in the teaching tenant; these are real stored documents, not automatically purged test records.

| Symptom | Action |
|---|---|
| `No module named workshop_helpers` | Run bootstrap with the same interpreter used by this demo. Keep the extracted folder in place after the editable install. |
| `No module named google` | Select `rag-shell-venv`; run bootstrap with `INSTALL_LIVE_DEPENDENCIES=True`. |
| ADC refresh / reauthentication error | Run `setup/authenticate.py`. Check whether the Run configuration sets `GOOGLE_APPLICATION_CREDENTIALS` to a different credential source. |
| `gcloud` not found | Run inside the Cloud Workstation and make sure the IDE process inherits the Google Cloud SDK PATH. |
| Permission denied during demo 03 | Inspect the failing storage, Firestore, mirror or API operation; read preflight cannot prove write permissions. Retain the backup and recovery results. |
| API cache is on | Use `VERIFY_API=False` for ledger-only proof, or configure your serving demo API with its answer cache off. |
| Ingest wait times out | Inspect the saved last source row, Pub/Sub delivery and `documind-ingest` logs; do not treat a still-indexed older generation as successful restoration. |
| Retained chunks are incomplete | Reuse cannot be claimed after expiry/purge or a partial retirement. Inspect evidence; use a fresh run once the underlying problem is resolved. |
| Hash read limit exceeded in demo 02 | Increase `max_hash_bytes` deliberately in settings. Default is 64 MiB per object needing a hash; 0 means unlimited. |

GCS and Firestore reads are not one atomic snapshot. Run this fixture demonstration without another process changing that fixture. Generation preconditions prevent overwriting or deleting a changed object; Firestore/current-row checks detect many concurrent changes. They do not make the whole multi-service workflow transactional.

## Extend the pattern after this pilot passes

Add a `module_05/lesson_5_1/` directory containing `demo_01_...py`, `demo_02_...py`, and as many examples as the lesson needs. Each file has its own `main()` and runs independently. For results routing, use `DemoContext("01", module=5, lesson="5.1", live=True)`.

Keep setup, ADC, service discovery, clients, API calls and result writing in the installed helpers. Add a helper only when behavior repeats; keep question text, teaching steps and expected observations visible in the lesson files. Do not create one giant lesson switchboard or a class hierarchy for every demo.

This pilot is based on the kit's [reconciliation planner](https://github.com/netsetos/agents_workshop/blob/main/deploy/services/ingest/reconcile.py), [idempotency functions](https://github.com/netsetos/agents_workshop/blob/main/deploy/services/ingest/idempotency.py) and [managed mirror](https://github.com/netsetos/agents_workshop/blob/main/deploy/services/ingest/managed.py). It loads your local kit at runtime rather than shipping a second copy of that logic. The explicit optional updater is for the existing learner clone and refuses a dirty worktree or an unexpected origin/branch; it never does the forced checkout in the earlier shell snippet.

Validation: offline planner execution and 17 tests covering generation checks, queued claims, exact-byte recovery and a mocked live workflow. The authoring repository's checks workflow runs these tests and demo 01 on pull requests. **The live GCP round trip has not been executed in your project.** Run demos 02 and 03 on the workstation to complete that validation before extending the rest of the course.
