# Lesson 4.4: Restore documents and reconcile index differences

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [demo_01_reconciliation_decisions.py](demo_01_reconciliation_decisions.py) | Use the actual planner for the queued example and interactive widget's scenarios. |
| 2 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 3 | [demo_02_create_and_repair_a_gap.py](demo_02_create_and_repair_a_gap.py) | Create the chapter fixture, prove it works, remove its object and reconcile retirement. |
| 4 | [demo_03_restore_the_exact_bytes.py](demo_03_restore_the_exact_bytes.py) | Restore the saved bytes and verify reactivation, reuse and zero drift. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

A deployed lane. This lesson creates its own smoke-note fixture and does not depend on ~/lesson34_note.md.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Optional extensions

- [optional/incomplete_undo.py](optional/incomplete_undo.py) — Explicit optional: incomplete undo
- [optional/nightly_job_and_backfill.py](optional/nightly_job_and_backfill.py) — Explicit optional: nightly job and backfill
- [optional/module_validation.py](optional/module_validation.py) — Explicit optional: module validation

## Conditional recovery

- [recovery/inspect_incomplete_restore.py](recovery/inspect_incomplete_restore.py) — Explicit recovery: inspect incomplete restore
- [recovery/repair_module_baseline.py](recovery/repair_module_baseline.py) — Explicit recovery: repair module baseline
- [recovery/run_isolated_reindex_smoke.py](recovery/run_isolated_reindex_smoke.py) — Explicit recovery: run isolated reindex smoke

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_reconciliation_decisions.py

Use the actual planner for the queued example and interactive widget's scenarios.

**`step_01_how_do_we_know_a_pdf_is_queued(session)` — How reconciliation decides / How do we know a PDF is queued?**

Explain the page's two-PDF illustration. Reconciliation leaves the matching queued generation to the batch lane; only the new Act contributes to drift.

Operation: Python — simulated facts, actual kit planner; no network.

Expected shape, not a promised result:

```text
reingest 1, queued 1, drift 1; applied false
```

**`step_02_explore_a_different_bucket_and_ledger(session)` — How reconciliation decides / Explore a different bucket and ledger**

Reproduce the five default widget documents before exploring its known-bytes and queued variations. The real plan(), decide_bytes() and drift_of() functions make the decisions.

Operation: Python — simulated facts, actual kit planner; no network.

Expected shape, not a promised result:

```text
ok 1, retire 1, touch 1, reingest 1, withdrawn 1; drift 2
```

### setup/prepare.py

Prepare this lesson's saved settings and dependencies before its live experiments.

**`step_01_credentials_backend_and_a_clean_baseline(session)` — Credentials, backend and a clean baseline / Credentials, backend and a clean baseline**

Do this before presenting. Stop at an error; do not paste the next stage until its checkpoint passes. Use the same operator shell and virtual environment throughout. Create a chapter directory before changing the backend, save its original pin, and run the offline planner check. These files are local demo state; keep them out of commits.

Operation: bash — run in the operator shell, in $DEMO_ROOT; prepare once per demonstration.

IDE adaptation: Persist that backend cleanup is required even if baseline preparation fails.

### demo_02_create_and_repair_a_gap.py

Create the chapter fixture, prove it works, remove its object and reconcile retirement.

**`step_01_create_this_chapter_s_note_and_the_checks(session)` — Create this chapter's note and the checks / Create this chapter's note and the checks**

A fresh name, a new fact and an unchanged local copy remove the dependencies on earlier lessons. This chapter does not use ~/lesson34_note.md or the smoke-lantern question. Another smoke note may still answer that question even after one copy is retired. Our primary checks are the exact source name, its object generation and its citation; a bare answerable True is insufficient.

Operation: bash — run once; keep the note and its checksum unchanged.

**`step_02_load_the_checks_once(session)` — Create this chapter's note and the checks / Load the checks once**

The helper block is preparation, not a slide to type live. It stops on failed uploads, polls the exact source and generation, checks citations, and refuses to apply an unexplained tenant-wide plan. The log filter includes both the version key and generation, so another acme upload cannot satisfy the wait. To resume after reopening a shell, first run the shared shell setup, then source this directory's session.env and helpers.sh; do not create a new note midway through a restore.

Operation: bash — save and load the chapter checks; no cloud writes in this block.

**`step_03_prove_the_document_works(session)` — Prove the document works / Prove the document works**

Show the source ledger in the UI and the same source's evidence from the API. On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it.

Operation: bash — upload, wait for this generation, then ask and record N.

**`step_04_prove_the_document_works(session)` — Prove the document works / Prove the document works**

On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it. Checkpoint: source indexed at this upload's generation, a cited answer naming locker Q7 in Jaipur, and no pending repair. If the source is indexed but the query has not caught up, repeat ch44_ask present and inspect its evidence; do not upload again merely to wait.

Operation: bash — after the checkpoint passes, save the observed chunk count.

**`step_05_delete_the_cloud_file_and_show_the_stale_i(session)` — Delete the cloud file and show the stale index / Delete the cloud file and show the stale index**

The local original stays safe. Delete only this demonstration's live object.

Operation: bash — check the backup before deleting; observe before running reconciliation.

**`step_06_plan_retirement_apply_it_then_prove_zero_d(session)` — Plan retirement, apply it, then prove zero drift / Plan retirement, apply it, then prove zero drift**

Keep preview, mutation and verification as three visible operations.

Operation: bash — read-only: require exactly one repair, for this fixture.

**`step_07_plan_retirement_apply_it_then_prove_zero_d(session)` — Plan retirement, apply it, then prove zero drift / Plan retirement, apply it, then prove zero drift**

Keep preview, mutation and verification as three visible operations. The action must be retire for $SOURCE, with reason gone from the bucket, applied: false and drift 1. A plan is evidence, not a repair. Pause other uploads during the demonstration; the kit's apply does not execute a saved, source-scoped plan.

Operation: bash — recheck immediately before the tenant-wide apply.

**`step_08_the_code_that_applies_the_plan(session)` — Plan retirement, apply it, then prove zero drift / The code that applies the plan**

The code that applies the plan

Operation: bash — verify retirement, citations and the next read-only plan.

### demo_03_restore_the_exact_bytes.py

Restore the saved bytes and verify reactivation, reuse and zero drift.

**`step_01_restore_the_exact_bytes_and_prove_reuse(session)` — Restore the exact bytes and prove reuse / Restore the exact bytes and prove reuse**

A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

Operation: bash — upload only if the original checksum still passes; wait for the new generation.

**`step_02_restore_the_exact_bytes_and_prove_reuse(session)` — Restore the exact bytes and prove reuse / Restore the exact bytes and prove reuse**

A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

Operation: bash — show this upload's event, restored citation and clean plan.

### recovery/inspect_incomplete_restore.py

Explicit recovery: inspect incomplete restore

**`step_01_why_the_undo_counts_first(session)` — Restore the exact bytes and prove reuse / Why the undo counts first**

You have shown a working document, a stale index, a planned repair, consistent absence, and a verified return. Steps 9 to 11 are separate extensions. Finish with step 12 even if you skip them: it restores the backend pin saved before the demonstration. Load this run's saved session variables first. Recover the exact generation named in its source ledger, then verify the content hash before writing the local file. Do not invent replacement text and expect a same-version reactivation. If the recorded generation is no longer retained, stop and inspect version recovery options; this path cannot reconstruct deleted bytes.

Operation: bash — read the retained version; this writes only the verified local backup.

### optional/incomplete_undo.py

Explicit optional: incomplete undo

**`step_01_watch_an_incomplete_undo_refuse(session)` — Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Operation: bash — retire the fixture again; require the exact one-item plan.

**`step_02_watch_an_incomplete_undo_refuse(session)` — Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Operation: bash — optional deliberate fault: remove one verified retired row of this fixture.

**`step_03_watch_an_incomplete_undo_refuse(session)` — Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Operation: bash — return the same bytes, then inspect the refused undo and fresh ingestion.

**`step_04_watch_an_incomplete_undo_refuse(session)` — Watch an incomplete undo refuse / Watch an incomplete undo refuse**

The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents. Checkpoint: a reactivate_incomplete event explains the shortfall, followed by fresh ingest_ok; the restored source and answer are valid again. The reused-N/embedded-0 checkpoint belongs to the successful undo in step 8, not this fault. The strict generation filter may exclude reactivate_incomplete because that event is emitted by the lower-level undo function; use the read below to see it for this version and time window.

Operation: bash — read the undo refusal for this version; no cloud writes.

### optional/nightly_job_and_backfill.py

Explicit optional: nightly job and backfill

**`step_01_read_the_deployed_job_and_backfill_plan(session)` — The nightly job, the number it ends on, and the lane older than the ledger / Read the deployed job and backfill plan**

Read the deployed job and backfill plan

Operation: bash — run in the operator shell, in $DEMO_ROOT (all read-only; the backfill is printed, not applied).

Expected shape, not a promised result:

```text
no nightly job on this lane: make reconcile-job declares and schedules it (RECONCILE_JOB=true, a Terraform apply)
no schedule either: make reconcile from a shell is the walk until then
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}

documind-reconcile
30 23 * * *	Asia/Kolkata	ENABLED
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}
```

### optional/module_validation.py

Explicit optional: module validation

**`step_01_run_the_broader_module_validation_separate(session)` — Run the broader module validation separately / Run the broader module validation separately**

The reindex smoke tests a different fixture and a wider lifecycle; it is not the proof of this chapter's deletion repair. make smoke-reindex uploads the kit's version 1 and version 2 under its own name, checks carry-over and reactivation, and asks the smoke-lantern question. Existing copies of that fact can affect the answer checks. Rehearse this separately, inspect its citations and fixture state, and report its actual pass/fail result. Do not replace the exact source and generation checks above with a green answer from this other note.

Operation: bash — optional module smoke; retain its exit status and inspect any failure.

### recovery/repair_module_baseline.py

Explicit recovery: repair module baseline

**`step_01_run_the_broader_module_validation_separate(session)` — Run the broader module validation separately / Run the broader module validation separately**

The smoke leaves its own fixture indexed. That does not demonstrate that $SOURCE was retired or restored. Count embedding work from the worker's actual events; a refused undo can require fresh embeddings, while a successful reactivation reuses retained vectors. Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL.

Operation: bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint).

IDE adaptation: Do not discard local smoke-script edits; a fast-forward update refuses conflicts so they can be inspected.

Expected shape, not a promised result:

```text
2026-09-2xT1x:xx:xx.xxxxxxZ	ingest_duplicate	acme_9c41d0e2b7f5...
1
https://documind-ingest-NUMBER.asia-south1.run.app
```

### recovery/run_isolated_reindex_smoke.py

Explicit recovery: run isolated reindex smoke

**`step_01_run_the_broader_module_validation_separate(session)` — Run the broader module validation separately / Run the broader module validation separately**

Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL. The check wants the answer to say bay 7 and not bay 4. Lesson 3.4's note, acme/smoke_note_v1.md, which step 5 restored, carries the same clause with bay 4 and no date, so with it current the model reads two sources that disagree; rule six tells it to follow the dated one and say from when it applies, and an answer that mentions the old bay fails the check although it is right. Withdraw the note for the smoke and restore it after: both are the kit's own targets from lesson 4.3, and the restore embeds nothing.

Operation: bash — run in the operator shell, in $DEMO_ROOT (the note withdrawn, the smoke, the note restored).

IDE adaptation: Restore the temporarily withdrawn smoke note even when the separate smoke fails.

Expected shape, not a promised result:

```text
{"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", ...}
  ...
  6 pass · 0 fail
{"event": "reconcile_restored", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "generation": "...", ...}
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_verify_the_story_and_restore_the_original(session)` — Verify the story and restore the original backend / Verify the story and restore the original backend**

Use the state transition and the exact evidence, then return the tenant to its saved configuration. Before reporting the chapter complete, check the final source and plan. If the optional incomplete-undo variation was run, record its fresh ingestion separately from the successful reuse in step 8. Leave the verified fixture and local original available for the audience to inspect.

Operation: bash — finish the demo, then restore the pin saved before it began.

IDE adaptation: Restore the saved backend in finally even when the final observation fails; the failed observation remains a failure.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html). All 44 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `52d1fbe549bb76a2fe1064f01171f2107c260a11`.
