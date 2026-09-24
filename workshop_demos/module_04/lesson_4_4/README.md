# Lesson 4.4: Restore documents and reconcile index differences

**Summary:** `ingest_reactivated ... embedded=0`; `make smoke-reindex` green. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html); Git blob `52d1fbe549bb76a2fe1064f01171f2107c260a11`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window queued-example | [demo_02_01_how_do_we_know_a_pdf_is_queued.py](demo_02_01_how_do_we_know_a_pdf_is_queued.py) | Python — simulated facts, actual kit planner; no network |
| s2 · window widget | [demo_02_02_explore_a_different_bucket_and_ledger.py](demo_02_02_explore_a_different_bucket_and_ledger.py) | Python — simulated facts, actual kit planner; no network |
| s3 · window 10 | [demo_03_01_credentials_backend_and_a_clean_baseline.py](demo_03_01_credentials_backend_and_a_clean_baseline.py) | bash — run in the operator shell, in $DEMO_ROOT; prepare once per demonstration |
| s4 · window 11 | [demo_04_01_create_this_chapter_s_note_and_the_checks.py](demo_04_01_create_this_chapter_s_note_and_the_checks.py) | bash — run once; keep the note and its checksum unchanged |
| s4 · window 12 | [demo_04_02_load_the_checks_once.py](demo_04_02_load_the_checks_once.py) | bash — save and load the chapter checks; no cloud writes in this block |
| s5 · window 13 | [demo_05_01_prove_the_document_works.py](demo_05_01_prove_the_document_works.py) | bash — upload, wait for this generation, then ask and record N |
| s5 · window 14 | [demo_05_02_prove_the_document_works.py](demo_05_02_prove_the_document_works.py) | bash — after the checkpoint passes, save the observed chunk count |
| s6 · window 15 | [demo_06_01_delete_the_cloud_file_and_show_the_stale_index.py](demo_06_01_delete_the_cloud_file_and_show_the_stale_index.py) | bash — check the backup before deleting; observe before running reconciliation |
| s7 · window 16 | [demo_07_01_plan_retirement_apply_it_then_prove_zero_drift.py](demo_07_01_plan_retirement_apply_it_then_prove_zero_drift.py) | bash — read-only: require exactly one repair, for this fixture |
| s7 · window 17 | [demo_07_02_plan_retirement_apply_it_then_prove_zero_drift.py](demo_07_02_plan_retirement_apply_it_then_prove_zero_drift.py) | bash — recheck immediately before the tenant-wide apply |
| s7 · window 20 | [demo_07_03_the_code_that_applies_the_plan.py](demo_07_03_the_code_that_applies_the_plan.py) | bash — verify retirement, citations and the next read-only plan |
| s8 · window 22 | [demo_08_01_restore_the_exact_bytes_and_prove_reuse.py](demo_08_01_restore_the_exact_bytes_and_prove_reuse.py) | bash — show this upload's event, restored citation and clean plan |

## Optional extensions

- [demo_09_01_optional_watch_an_incomplete_undo_refuse.py](demo_09_01_optional_watch_an_incomplete_undo_refuse.py) — bash — retire the fixture again; require the exact one-item plan
- [demo_09_02_optional_watch_an_incomplete_undo_refuse.py](demo_09_02_optional_watch_an_incomplete_undo_refuse.py) — bash — optional deliberate fault: remove one verified retired row of this fixture
- [demo_09_03_optional_watch_an_incomplete_undo_refuse.py](demo_09_03_optional_watch_an_incomplete_undo_refuse.py) — bash — return the same bytes, then inspect the refused undo and fresh ingestion
- [demo_09_04_optional_watch_an_incomplete_undo_refuse.py](demo_09_04_optional_watch_an_incomplete_undo_refuse.py) — bash — read the undo refusal for this version; no cloud writes
- [demo_10_01_optional_read_the_deployed_job_and_backfill_plan.py](demo_10_01_optional_read_the_deployed_job_and_backfill_plan.py) — bash — run in the operator shell, in $DEMO_ROOT (all read-only; the backfill is printed, not applied)
- [demo_11_01_optional_run_the_broader_module_validation_separately.py](demo_11_01_optional_run_the_broader_module_validation_separately.py) — bash — optional module smoke; retain its exit status and inspect any failure

## Conditional recovery

- [recover_08_01_restore_the_exact_bytes_and_prove_reuse.py](recover_08_01_restore_the_exact_bytes_and_prove_reuse.py) — bash — upload only if the original checksum still passes; wait for the new generation
- [recover_08_02_why_the_undo_counts_first.py](recover_08_02_why_the_undo_counts_first.py) — bash — read the retained version; this writes only the verified local backup
- [recover_11_01_run_the_broader_module_validation_separately.py](recover_11_01_run_the_broader_module_validation_separately.py) — bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint)
- [recover_11_02_run_the_broader_module_validation_separately.py](recover_11_02_run_the_broader_module_validation_separately.py) — bash — run in the operator shell, in $DEMO_ROOT (the note withdrawn, the smoke, the note restored)

## Finish and restore settings

- [finish_12_01_verify_the_story_and_restore_the_original_backen.py](finish_12_01_verify_the_story_and_restore_the_original_backen.py) — bash — finish the demo, then restore the pin saved before it began

## Checkpoints and explanation

### demo_02_01_how_do_we_know_a_pdf_is_queued.py

**HTML: How reconciliation decides / How do we know a PDF is queued?**

Explain the page's two-PDF illustration. Reconciliation leaves the matching queued generation to the batch lane; only the new Act contributes to drift.

Run instruction: Python — simulated facts, actual kit planner; no network.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
reingest 1, queued 1, drift 1; applied false
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_02_02_explore_a_different_bucket_and_ledger.py

**HTML: How reconciliation decides / Explore a different bucket and ledger**

Reproduce the five default widget documents before exploring its known-bytes and queued variations. The real plan(), decide_bytes() and drift_of() functions make the decisions.

Run instruction: Python — simulated facts, actual kit planner; no network.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ok 1, retire 1, touch 1, reingest 1, withdrawn 1; drift 2
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_credentials_backend_and_a_clean_baseline.py

**HTML: Credentials, backend and a clean baseline / Credentials, backend and a clean baseline**

Do this before presenting. Stop at an error; do not paste the next stage until its checkpoint passes. Use the same operator shell and virtual environment throughout. Create a chapter directory before changing the backend, save its original pin, and run the offline planner check. These files are local demo state; keep them out of commits.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT; prepare once per demonstration.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Persist that backend cleanup is required even if baseline preparation fails.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_create_this_chapter_s_note_and_the_checks.py

**HTML: Create this chapter's note and the checks / Create this chapter's note and the checks**

A fresh name, a new fact and an unchanged local copy remove the dependencies on earlier lessons. This chapter does not use ~/lesson34_note.md or the smoke-lantern question. Another smoke note may still answer that question even after one copy is retired. Our primary checks are the exact source name, its object generation and its citation; a bare answerable True is insufficient.

Run instruction: bash — run once; keep the note and its checksum unchanged.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_load_the_checks_once.py

**HTML: Create this chapter's note and the checks / Load the checks once**

The helper block is preparation, not a slide to type live. It stops on failed uploads, polls the exact source and generation, checks citations, and refuses to apply an unexplained tenant-wide plan. The log filter includes both the version key and generation, so another acme upload cannot satisfy the wait. To resume after reopening a shell, first run the shared shell setup, then source this directory's session.env and helpers.sh; do not create a new note midway through a restore.

Run instruction: bash — save and load the chapter checks; no cloud writes in this block.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_prove_the_document_works.py

**HTML: Prove the document works / Prove the document works**

Show the source ledger in the UI and the same source's evidence from the API. On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it.

Run instruction: bash — upload, wait for this generation, then ask and record N.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_prove_the_document_works.py

**HTML: Prove the document works / Prove the document works**

On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it. Checkpoint: source indexed at this upload's generation, a cited answer naming locker Q7 in Jaipur, and no pending repair. If the source is indexed but the query has not caught up, repeat ch44_ask present and inspect its evidence; do not upload again merely to wait.

Run instruction: bash — after the checkpoint passes, save the observed chunk count.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_delete_the_cloud_file_and_show_the_stale_index.py

**HTML: Delete the cloud file and show the stale index / Delete the cloud file and show the stale index**

The local original stays safe. Delete only this demonstration's live object.

Run instruction: bash — check the backup before deleting; observe before running reconciliation.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_plan_retirement_apply_it_then_prove_zero_drift.py

**HTML: Plan retirement, apply it, then prove zero drift / Plan retirement, apply it, then prove zero drift**

Keep preview, mutation and verification as three visible operations.

Run instruction: bash — read-only: require exactly one repair, for this fixture.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_plan_retirement_apply_it_then_prove_zero_drift.py

**HTML: Plan retirement, apply it, then prove zero drift / Plan retirement, apply it, then prove zero drift**

Keep preview, mutation and verification as three visible operations. The action must be retire for $SOURCE, with reason gone from the bucket, applied: false and drift 1. A plan is evidence, not a repair. Pause other uploads during the demonstration; the kit's apply does not execute a saved, source-scoped plan.

Run instruction: bash — recheck immediately before the tenant-wide apply.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_the_code_that_applies_the_plan.py

**HTML: Plan retirement, apply it, then prove zero drift / The code that applies the plan**

The code that applies the plan

Run instruction: bash — verify retirement, citations and the next read-only plan.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_08_01_restore_the_exact_bytes_and_prove_reuse.py

**HTML: Restore the exact bytes and prove reuse / Restore the exact bytes and prove reuse**

A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

Run instruction: bash — upload only if the original checksum still passes; wait for the new generation.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_restore_the_exact_bytes_and_prove_reuse.py

**HTML: Restore the exact bytes and prove reuse / Restore the exact bytes and prove reuse**

A new upload generation, the same content hash, and the worker's verified reactivation. The checksum must still match. Changing the memo, adding today's date, or replacing it with a base smoke fixture creates different bytes and does not demonstrate the same-version undo. Keep the same object name too.

Run instruction: bash — show this upload's event, restored citation and clean plan.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_08_02_why_the_undo_counts_first.py

**HTML: Restore the exact bytes and prove reuse / Why the undo counts first**

You have shown a working document, a stale index, a planned repair, consistent absence, and a verified return. Steps 9 to 11 are separate extensions. Finish with step 12 even if you skip them: it restores the backend pin saved before the demonstration. Load this run's saved session variables first. Recover the exact generation named in its source ledger, then verify the content hash before writing the local file. Do not invent replacement text and expect a same-version reactivation. If the recorded generation is no longer retained, stop and inspect version recovery options; this path cannot reconstruct deleted bytes.

Run instruction: bash — read the retained version; this writes only the verified local backup.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_09_01_optional_watch_an_incomplete_undo_refuse.py

**HTML: Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Run instruction: bash — retire the fixture again; require the exact one-item plan.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_09_02_optional_watch_an_incomplete_undo_refuse.py

**HTML: Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Run instruction: bash — optional deliberate fault: remove one verified retired row of this fixture.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_09_03_optional_watch_an_incomplete_undo_refuse.py

**HTML: Watch an incomplete undo refuse / Watch an incomplete undo refuse**

Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

Run instruction: bash — return the same bytes, then inspect the refused undo and fresh ingestion.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_09_04_optional_watch_an_incomplete_undo_refuse.py

**HTML: Watch an incomplete undo refuse / Watch an incomplete undo refuse**

The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents. Checkpoint: a reactivate_incomplete event explains the shortfall, followed by fresh ingest_ok; the restored source and answer are valid again. The reused-N/embedded-0 checkpoint belongs to the successful undo in step 8, not this fault. The strict generation filter may exclude reactivate_incomplete because that event is emitted by the lower-level undo function; use the read below to see it for this version and time window.

Run instruction: bash — read the undo refusal for this version; no cloud writes.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_10_01_optional_read_the_deployed_job_and_backfill_plan.py

**HTML: The nightly job, the number it ends on, and the lane older than the ledger / Read the deployed job and backfill plan**

Read the deployed job and backfill plan

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (all read-only; the backfill is printed, not applied).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
no nightly job on this lane: make reconcile-job declares and schedules it (RECONCILE_JOB=true, a Terraform apply)
no schedule either: make reconcile from a shell is the walk until then
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}

documind-reconcile
30 23 * * *	Asia/Kolkata	ENABLED
{"event": "reconcile_backfill", "chunks": 0, "sources": N, "applied": false}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_11_01_optional_run_the_broader_module_validation_separately.py

**HTML: Run the broader module validation separately / Run the broader module validation separately**

The reindex smoke tests a different fixture and a wider lifecycle; it is not the proof of this chapter's deletion repair. make smoke-reindex uploads the kit's version 1 and version 2 under its own name, checks carry-over and reactivation, and asks the smoke-lantern question. Existing copies of that fact can affect the answer checks. Rehearse this separately, inspect its citations and fixture state, and report its actual pass/fail result. Do not replace the exact source and generation checks above with a green answer from this other note.

Run instruction: bash — optional module smoke; retain its exit status and inspect any failure.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_11_01_run_the_broader_module_validation_separately.py

**HTML: Run the broader module validation separately / Run the broader module validation separately**

The smoke leaves its own fixture indexed. That does not demonstrate that $SOURCE was retired or restored. Count embedding work from the worker's actual events; a refused undo can require fresh embeddings, while a successful reactivation reuses retained vectors. Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the worker's lines for the smoke's uploads; the kit pulled; the subscription's endpoint).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Do not discard local smoke-script edits; a fast-forward update refuses conflicts so they can be inspected.

Expected shape from the HTML (actual counts/timing can differ):

```text
2026-09-2xT1x:xx:xx.xxxxxxZ	ingest_duplicate	acme_9c41d0e2b7f5...
1
https://documind-ingest-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_11_02_run_the_broader_module_validation_separately.py

**HTML: Run the broader module validation separately / Run the broader module validation separately**

Two causes, told apart by one log read. A kit older than 23 September 2026 waits for a worker line carrying jsonPayload.tenant, and the line the worker writes for the unchanged fixture bytes, ingest_duplicate, carries only the document key, so the smoke waits its five minutes for a match that cannot come. The setup block pulls the latest kit every session; on a clone, one pull is the fix, after putting back any copy of the smoke file made by hand, and the count on the second line must be at least 1 afterwards. If the read shows nothing at all, the event never reached the worker, and the push subscription's endpoint is the place to look: it must be the worker's URL. The check wants the answer to say bay 7 and not bay 4. Lesson 3.4's note, acme/smoke_note_v1.md, which step 5 restored, carries the same clause with bay 4 and no date, so with it current the model reads two sources that disagree; rule six tells it to follow the dated one and say from when it applies, and an answer that mentions the old bay fails the check although it is right. Withdraw the note for the smoke and restore it after: both are the kit's own targets from lesson 4.3, and the restore embeds nothing.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the note withdrawn, the smoke, the note restored).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Restore the temporarily withdrawn smoke note even when the separate smoke fails.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", ...}
  ...
  6 pass · 0 fail
{"event": "reconcile_restored", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "generation": "...", ...}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### finish_12_01_verify_the_story_and_restore_the_original_backen.py

**HTML: Verify the story and restore the original backend / Verify the story and restore the original backend**

Use the state transition and the exact evidence, then return the tenant to its saved configuration. Before reporting the chapter complete, check the final source and plan. If the optional incomplete-undo variation was run, record its fresh ingestion separately from the successful reuse in step 8. Leave the verified fixture and local original available for the audience to inspect.

Run instruction: bash — finish the demo, then restore the pin saved before it began.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Restore the saved backend in finally even when the final observation fails; the failed observation remains a failure.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

46 code windows mapped: 23 IDE demo files, 1 shared setup blocks, 22 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
