# Lesson 4.3: Publish versions, retire documents and reject stale events

**Summary:** `ingest_stale_event`; `withdrawn` after `make retire`. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html); Git blob `f336737e3da708a11e2863a2d9742fafed531016`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_read_the_handbook_s_versions_rs_0.py](demo_03_01_read_the_handbook_s_versions_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s4 · window 14 | [demo_04_01_do_it_the_purge_plan_rs_0.py](demo_04_01_do_it_the_purge_plan_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (read-only without APPLY=1) |
| s5 · window 19 | [demo_05_01_do_it_three_events_three_verdicts_rs_0.py](demo_05_01_do_it_three_events_three_verdicts_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (three messages; nothing is indexed) |
| s6 · window 25 | [demo_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py](demo_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py) | bash — run in the operator shell, in $DEMO_ROOT (the object, or its last generation; then the hash against the ledger) |
| s6 · window 29 | [demo_06_02_do_it_withdraw_the_note_test_the_tombstone_resto.py](demo_06_02_do_it_withdraw_the_note_test_the_tombstone_resto.py) | bash — run in the operator shell, in $DEMO_ROOT (the withdrawal, then two reads) |
| s6 · window 31 | [demo_06_03_do_it_withdraw_the_note_test_the_tombstone_resto.py](demo_06_03_do_it_withdraw_the_note_test_the_tombstone_resto.py) | bash — run in the operator shell (one question; paise) |
| s6 · window 33 | [demo_06_04_do_it_withdraw_the_note_test_the_tombstone_resto.py](demo_06_04_do_it_withdraw_the_note_test_the_tombstone_resto.py) | bash — run in the operator shell (the same bytes again: refused; then the restore) |
| s7 · window 36 | [demo_07_01_read_the_ledger_as_the_operator_does_rs_0.py](demo_07_01_read_the_ledger_as_the_operator_does_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT |

## Conditional recovery

- [recover_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py](recover_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py) — bash — only if the check said DIFFERENT or the bucket had nothing (rebuilds the note from the kit's fixture and the ledger's hash)

## Finish and restore settings

- [finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) — bash — run in the operator shell when you finish the lesson, not now

## Checkpoints and explanation

### demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Run instruction: bash — run in the operator shell now, before the lesson's first step.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=vector
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Run instruction: bash — run in the operator shell when you finish the lesson, not now.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Run at lesson end despite its early HTML position, as the source label explicitly instructs.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_read_the_handbook_s_versions_rs_0.py

**HTML: Publish: the swap, and the reader's guard / Read the handbook's versions, Rs 0**

Read the handbook's versions, Rs 0

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme_497809ff...  rows 283  current 283  retired   0
acme_55603088...  rows 283  current   0  retired 283  superseded_by acme_497809ff...  expire_at 2026-10-22  effective_to None
acme_54337b4b...  rows 283  current   0  retired 283  superseded_by acme_497809ff...  expire_at 2026-10-22  effective_to None
current versions: 1 | staged rows: 0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_purge_plan_rs_0.py

**HTML: Superseded: the retired rows' bookkeeping, and the clock that removes them / Do it: the purge plan, Rs 0**

Do it: the purge plan, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only without APPLY=1).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_purge_plan", "expired": 0, "retired": 566, "applied": false, "note": "the TTL policy on chunks.expire_at (firestore_indexes.tf) deletes these on its own within a day; this is the manual twin for a lane that has not applied it"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_three_events_three_verdicts_rs_0.py

**HTML: Stale: the generation guard, and three replayed events / Do it: three events, three verdicts, Rs 0**

The block reads the handbook's generation off the ledger, then publishes three records into the ingest topic exactly as Cloud Storage would, with the generation before the ledger's, the ledger's own, and one after it. The push subscription delivers them to the worker, and the worker's three lines say what it did with each. Nothing on the lane changes.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (three messages; nothing is indexed).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the ledger's generation for the handbook: 1758554107123456
TIMESTAMP                 EVENT               GENERATION        LEDGER_GENERATION  REASON
2026-09-22T15:02:31.512Z  ingest_stale_event  1758554107123457                     generation gone: the object was overwritten
2026-09-22T15:02:30.907Z  ingest_duplicate
2026-09-22T15:02:30.211Z  ingest_stale_event  1758554107123455  1758554107123456   older than the ledger
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py

**HTML: Withdrawn: retire a document by hand, then restore it / Do it: withdraw the note, test the tombstone, restore it**

The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the object, or its last generation; then the hash against the ledger).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ledger abcdef0123456789 | file abcdef0123456789 | the same bytes
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_06_01_do_it_withdraw_the_note_test_the_tombstone_resto.py

**HTML: Withdrawn: retire a document by hand, then restore it / Do it: withdraw the note, test the tombstone, restore it**

The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

Run instruction: bash — only if the check said DIFFERENT or the bucket had nothing (rebuilds the note from the kit's fixture and the ledger's hash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
rebuilt, dated 2026-09-DD
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_withdraw_the_note_test_the_tombstone_resto.py

**HTML: Withdrawn: retire a document by hand, then restore it / Do it: withdraw the note, test the tombstone, restore it**

The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the withdrawal, then two reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "fingerprint": "7c2e91a4d05b3f68", "retired_doc_keys": ["acme_9c41d0e2b7f5..."], "retired_ids": ["acme:9c41d0e2b7f5...#0", "acme:9c41d0e2b7f5...#1", "acme:9c41d0e2b7f5...#2"], "retired_chunks": 3, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}
acme/smoke_note_v1.md withdrawn chunks 3
fingerprint 7c2e91a4d05b3f68 | last event reconcile_withdrawn
3 rows | current: 0 | with expire_at: 3 | superseded_by: {'None'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_do_it_withdraw_the_note_test_the_tombstone_resto.py

**HTML: Withdrawn: retire a document by hand, then restore it / Do it: withdraw the note, test the tombstone, restore it**

The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

Run instruction: bash — run in the operator shell (one question; paise).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
answerable False | citations 0 | The corpus holds nothing near this question: no passage of this tenant's current documents
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_04_do_it_withdraw_the_note_test_the_tombstone_resto.py

**HTML: Withdrawn: retire a document by hand, then restore it / Do it: withdraw the note, test the tombstone, restore it**

The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

Run instruction: bash — run in the operator shell (the same bytes again: refused; then the restore).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ingest_withdrawn	acme_9c41d0e2b7f5...	make restore SOURCE= clears the tombstone
{"event": "reconcile_restored", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "generation": "1758555302345678", "next": "ingest_reactivated inside the undo window, ingest_ok (a fresh version) after it"}
>> event chunks reused embedded: ingest_reactivated	3	3	0
acme/smoke_note_v1.md indexed reused 3 embedded 0
answerable True | The smoke lantern is kept in bay 4 of the Pune warehouse ... [Source 1]
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_read_the_ledger_as_the_operator_does_rs_0.py

**HTML: The three states side by side / Read the ledger as the operator does, Rs 0**

Read the ledger as the operator does, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
source                                       status            gen chunks reused embed retired effective  embedding              indexed_at
acme/code_on_wages_2019.pdf                  indexed    ...2671234567     67      0    67       0 -          text-embedding-005@1   2026-09-20T09:14:02
acme/hr_policy_2026.md                       indexed    ...4107123456    283    283     0     283 -          text-embedding-005@1   2026-09-22T13:41:55
acme/smoke_note_v1.md                        indexed    ...5302345678      3      3     0       0 -          text-embedding-005@1   2026-09-22T15:21:40
...
{"ledger": "acme", "fingerprint": "3a9f0c17e5d2b846", "versions": 9, "last_event": "ingest_reactivated"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

38 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 26 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
