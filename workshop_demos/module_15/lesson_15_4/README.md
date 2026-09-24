# Lesson 15.4: Compare quality and test update/withdrawal freshness

**Summary:** `make managed-status` matches after a reindex, an undo, a withdrawal. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html); Git blob `66b57f935533d5d3d7f44538e669dbf20a968426`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 7 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the kit's mirror through the four events; no store, no network) |
| s4 · window 11 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (retrieval only, no model: a few minutes) |
| s5 · window 13 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (a second version of zeta's handbook, then the check) |
| s5 · window 16 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit (the first version's bytes again, then the check) |
| s6 · window 20 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the handbook withdrawn by hand, then the check) |
| s6 · window 22 | [demo_06_02_do_it.py](demo_06_02_do_it.py) | bash — run in the operator shell, in the kit (the handbook brought back, then the check) |

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

### demo_03_01_do_it.py

**HTML: The four events through the kit's mirror, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the kit's mirror through the four events; no store, no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. v1 is ingested: the worker's swap, then after_swap()
     mirror_ok     rag_engine    upsert            v1 uploaded, 73 characters
     mirror_ok     vertex_search upsert            v1 uploaded, 73 characters
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
2. v2 replaces it: after_swap(), with v1 in the swap's retired_doc_keys
     mirror_ok     rag_engine    upsert            v2 uploaded, 73 characters
     mirror_ok     vertex_search upsert            v2 uploaded, 73 characters
     mirror_ok     rag_engine    delete:superseded 1
     mirror_ok     vertex_search delete:superseded 1
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
3. the undo, v1's bytes again: the worker flips the rows back, then after_undo(), which is given no text
     mirror_ok     rag_engine    upsert            v1 uploaded, 73 characters
     mirror_ok     vertex_search upsert            v1 uploaded, 73 characters
     mirror_ok     rag_engine    delete:superseded 1
     mirror_ok     vertex_search delete:superseded 1
   the stores now hold for v1: {'rag_engine': '...a notice period of 30 days.', 'vertex_search': '...a notice period of 30 days.'}
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
4. make retire: the rows retired, the ledger row withdrawn, then retired(..., 'withdrawn')
     mirror_ok     rag_engine    delete:withdrawn  1
     mirror_ok     vertex_search delete:withdrawn  1
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
5. make restore, while Vertex AI Search refuses one import: the worker's reactivation, then after_undo()
     mirror_ok     rag_engine    upsert            v1 uploaded, 73 characters
     mirror_failed vertex_search upsert            TimeoutError: the import did not finish
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search drift, missing ['v1']
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Six arms, one golden set: is a store as good? / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (retrieval only, no model: a few minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python evals/ablate.py --project documind-ai-YOUR-ID --region asia-south1 --arms all
47 rows with anchors, 66 anchors, one knob per arm (project documind-ai-YOUR-ID, embeddings in asia-south1, ranker on global)

arm                                          recall@depth  recall@5    mrr rows@1.0  p95 ms
dense 5, no reranker                                 0.94      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - not retrieved at depth 5
       lost: lk-21: code_on_wages_2019 - not retrieved at depth 5
       lost: jn-11: labour_codes_compliance_handbook - not retrieved at depth 5
dense 20 -> rerank 5   (the lane)                    1.00      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - ranked out (in the candidates, not the five)
       lost: lk-21: code_on_wages_2019 - ranked out (in the candidates, not the five)
       lost: jn-11: labour_codes_compliance_handbook - ranked out (in the candidates, not the five)
dense 50 -> rerank 5                                 1.00      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - ranked out (in the candidates, not the five)
       lost: lk-21: code_on_wages_2019 - ranked out (in the candidates, not the five)
       lost: jn-11: labour_codes_compliance_handbook - ranked out (in the candidates, not the five)
hybrid 20 -> rerank 5  (4.5, not wired)              1.00      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - ranked out (in the candidates, not the five)
       lost: lk-21: code_on_wages_2019 - ranked out (in the candidates, not the five)
       lost: jn-11: labour_codes_compliance_handbook - ranked out (in the candidates, not the five)
rag_engine 20 -> rerank 5  (4.3's corpus, P9.4)         0.96      0.91   0.76       41     ...   (2 rows failed)
       jn-04: RuntimeError: no RAG Engine corpus 'documind-globex': make rag-corpus TENANT=globex, then MANAGED_MIRROR=rag_engine
       lk-28: RuntimeError: no RAG Engine corpus 'documind-globex': make rag-corpus TENANT=globex, then MANAGED_MIRROR=rag_engine
       lost: lk-02: PR-05, hr_policy_2026 - ranked out (in the candidates, not the five)
       lost: lk-05: IT-SEC-04, hr_policy_2026 - not retrieved at depth 1
       lost: jn-07: IT-SEC-04 - not retrieved at depth 2
       lost: jn-11: labour_codes_compliance_handbook - ranked out (in the candidates, not the five)
vertex_search 20 -> rerank 5  (4.4's data store, R4)         0.88      0.71   0.61       30     ...   (2 rows failed)
       jn-04: NotFound: 404 DataStore documind-globex not found
       lk-28: NotFound: 404 DataStore documind-globex not found
       lost: lk-05: IT-SEC-04, hr_policy_2026 - not retrieved at depth 0
       lost: lk-08: FIN-02 - ranked out (in the candidates, not the five)
       lost: lk-09: WFH-01 - not retrieved at depth 6
       lost: lk-13: MSA-09 - not retrieved at depth 3
       lost: jn-01: LV-07 - not retrieved at depth 12
       lost: jn-02: NP-03, LV-07 - not retrieved at depth 15
       lost: jn-03: LV-07, NP-03 - not retrieved at depth 18
       lost: jn-07: IT-SEC-04 - not retrieved at depth 5
       lost: lk-15: maternity_benefit_amendment_act_2017 - ranked out (in the candidates, not the five)
       lost: lk-24: osh_code_2020 - ranked out (in the candidates, not the five)
       lost: lk-25: osh_code_2020 - ranked out (in the candidates, not the five)
       lost: lk-26: dpdp_act_2023 - ranked out (in the candidates, not the five)
       lost: lk-29: osh_code_2020 - ranked out (in the candidates, not the five)
       lost: lk-30: dpdp_act_2023 - ranked out (in the candidates, not the five)
       lost: lk-31: code_on_social_security_2020 - ranked out (in the candidates, not the five)

Read it in this order: recall@depth is the reranker's ceiling - if the 20 and 50 rows agree, depth is not the knob;
recall@5 of the lane's row minus the first row is the reranker's lift, and p95 is what it costs;
the hybrid row says whether a BM25 leg is worth wiring - twenty of the anchors are clause codes, its home ground;
the rag_engine row (--arms all) is 4.3's corpus against the lane's own rows - a managed chunk that splits a clause from its code shows up as a miss.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: A new version, then the undo / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a second version of zeta's handbook, then the check).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
>> gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	zeta_025c4143c0a1115dda29f3556faff8cbe552249f4576c78036ea07a80f9be422	283	282	1	283	
>> retired (doc_keys, chunks, expire days): zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a	283	30
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_zeta_2026.md API=<candidate url>
the mirror's doc.mirror events for zeta since 2026-09-24T08:00:00Z (the audit bucket):
  08:00:48  upsert            rag_engine    us-central1 zeta_025c4143...
  08:00:48  upsert            vertex_search global      zeta_025c4143...
  08:00:49  delete:superseded rag_engine    us-central1 zeta_e920a147...
  08:00:49  delete:superseded vertex_search global      zeta_e920a147...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook indexed):
  0:00  handbook indexed; rag_engine in sync; vertex_search drift, missing zeta_025c4143...
  0:20  handbook indexed; rag_engine in sync; vertex_search in sync
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant": "zeta", "store": "vertex_search", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
zeta, answered from vertex_search: A confirmed employee at grade L4 or above serves a notice period of 45 days [1].
  cites zeta:zeta_025c4143...#vs-f44cd45f3eb8
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: A new version, then the undo / Do it**

Now the undo: the same name, with the first version's bytes, straight from the kit's corpus. This is the worker's branch for a version it has seen before:

Run instruction: bash — run in the operator shell, in the kit (the first version's bytes again, then the check).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
>> gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a	283	283	0	283	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_zeta_2026.md API=<candidate url>
the mirror's doc.mirror events for zeta since 2026-09-24T08:10:00Z (the audit bucket):
  08:10:48  upsert            rag_engine    us-central1 zeta_e920a147...
  08:10:48  upsert            vertex_search global      zeta_e920a147...
  08:10:49  delete:superseded rag_engine    us-central1 zeta_025c4143...
  08:10:49  delete:superseded vertex_search global      zeta_025c4143...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook indexed):
  0:00  handbook indexed; rag_engine in sync; vertex_search drift, missing zeta_e920a147...
  0:20  handbook indexed; rag_engine in sync; vertex_search in sync
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant": "zeta", "store": "vertex_search", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
zeta, answered from vertex_search: A confirmed employee at grade L4 or above serves a notice period of 30 days [1].
  cites zeta:zeta_e920a147...#vs-e9fd5992049d
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: A withdrawal, then the restore / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the handbook withdrawn by hand, then the check).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md", "fingerprint": "756528d4215dfc80", "retired_doc_keys": ["zeta_e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a"], "retired_ids": ["zeta:e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a#0", "...", "zeta:e920a147e36b71710f6ba542f63694634bb3755a581d443c2603d899f125256a#99"], "retired_chunks": 283, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}
the mirror's doc.mirror events for zeta since 2026-09-24T08:20:00Z (the audit bucket):
  08:20:24  delete:withdrawn  rag_engine    us-central1 zeta_e920a147...
  08:20:24  delete:withdrawn  vertex_search global      zeta_e920a147...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook withdrawn):
  0:00  handbook withdrawn; rag_engine in sync; vertex_search in sync
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 6, "held": 6, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant": "zeta", "store": "vertex_search", "ledger_current": 6, "held": 6, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
zeta, answered from vertex_search: The context does not say.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it.py

**HTML: A withdrawal, then the restore / Do it**

Then the restore:

Run instruction: bash — run in the operator shell, in the kit (the handbook brought back, then the check).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_restored", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md", "generation": "1758000000021000", "next": "ingest_reactivated inside the undo window, ingest_ok (a fresh version) after it"}
the mirror's doc.mirror events for zeta since 2026-09-24T08:30:00Z (the audit bucket):
  08:30:39  upsert            rag_engine    us-central1 zeta_e920a147...
  08:30:39  upsert            vertex_search global      zeta_e920a147...
make managed-status TENANT_ONLY=zeta, until the stores match the ledger (the handbook indexed):
  0:00  handbook indexed; rag_engine in sync; vertex_search drift, missing zeta_e920a147...
  0:20  handbook indexed; rag_engine in sync; vertex_search in sync
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant": "zeta", "store": "vertex_search", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
zeta, answered from vertex_search: A confirmed employee at grade L4 or above serves a notice period of 30 days [1].
  cites zeta:zeta_e920a147...#vs-e9fd5992049d
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

23 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 14 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
