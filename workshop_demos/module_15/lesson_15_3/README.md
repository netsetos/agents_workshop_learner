# Lesson 15.3: Configure and query managed retrieval mirrors

**Summary:** `found_by: rag_engine`; a policy skip for an `in` tenant. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html); Git blob `f3b8566f506ca71dad40790c01d60af2bf9f2df5`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the mirror's rules, run; no store, no network) |
| s4 · window 13 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (reads only) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (acme's pin back to RAG Engine, then one question for each tenant) |
| s5 · window 19 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit (the same question to the API, then through the kit's own retrieve()) |
| s6 · window 21 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (a note to globex, whose text may not leave India) |
| s6 · window 23 | [demo_06_02_do_it.py](demo_06_02_do_it.py) | bash — run in the operator shell, in the kit (reads only) |
| s6 · window 25 | [demo_06_03_do_it.py](demo_06_03_do_it.py) | bash — run in the operator shell, in the kit (globex pinned to a store for one question, then unpinned) |

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

**HTML: The mirror's rules, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the mirror's rules, run; no store, no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
policy_of: {'None': 'in', 'any': 'any', 'ANY ': 'any', 'us': 'in'}
permits: {'any -> us-central1': True, 'any -> global': True, 'any -> asia-south1': True, 'in -> us-central1': False, 'in -> global': False, 'in -> asia-south1': True}
1. acme (any) makes version v1 current:
     mirror_ok              rag_engine    upsert            acme_v1 uploaded
     mirror_ok              vertex_search upsert            acme_v1 uploaded
   held {'rag_engine': 'us-central1', 'vertex_search': 'global'}
2. globex (in) adds a note:
     mirror_policy_skipped  rag_engine    upsert            in
     mirror_policy_skipped  vertex_search upsert            in
   held {}
3. globex adds a second note:
   held {}
4. acme's policy is turned to in, and version v2 becomes current:
     mirror_policy_skipped  rag_engine    upsert            in
     mirror_policy_skipped  vertex_search upsert            in
   held {}
   the stores still hold {'rag_engine': ['acme_v1'], 'vertex_search': ['acme_v1']}
5. v1 is retired:
     mirror_ok              rag_engine    delete:superseded 1
     mirror_ok              vertex_search delete:superseded 1
   the stores hold {'rag_engine': [], 'vertex_search': []}
the audit trail:
   doc.mirror upsert rag_engine acme_v1
   doc.mirror upsert vertex_search acme_v1
   doc.mirror delete:superseded rag_engine acme_v1
   doc.mirror delete:superseded vertex_search acme_v1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The policies, the pins and the stores / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: data_region=any
acme: retrieval_backend=vector
zeta: data_region=any
zeta: retrieval_backend=vertex_search
globex: data_region=in
globex: retrieval_backend=default (the deployment RETRIEVAL_BACKEND)
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID RAG_LOCATION=us-central1 AUDIT_BUCKET=documind-ai-YOUR-ID-audit \
  python managed.py --project documind-ai-YOUR-ID --status --mode both
{"tenant": "acme", "store": "rag_engine", "ledger_current": 21, "held": 18, "missing": 3, "orphans": 0, "status": "drift", "missing_doc_keys": ["acme_0994e77d201672aa703e6d5a9a00590d117ad98239b319e900a0d6a787ede170", "acme_80403acbbf9b2ada3bb37bfa6983bd864696ed45ca459a5ad7cf0296596ca987", "acme_ef63c85dc631e96e6c46364c3188f3f7a9a9283ad2e88074494d378399e1a71b"], "orphan_doc_keys": []}
{"tenant": "acme", "store": "vertex_search", "ledger_current": 21, "held": 18, "missing": 3, "orphans": 0, "status": "drift", "missing_doc_keys": ["acme_0994e77d201672aa703e6d5a9a00590d117ad98239b319e900a0d6a787ede170", "acme_80403acbbf9b2ada3bb37bfa6983bd864696ed45ca459a5ad7cf0296596ca987", "acme_ef63c85dc631e96e6c46364c3188f3f7a9a9283ad2e88074494d378399e1a71b"], "orphan_doc_keys": []}
{"tenant": "globex", "store": "rag_engine", "ledger_current": 3, "status": "no store", "hint": "no RAG Engine corpus 'documind-globex' in us-central1: make rag-corpus TENANT=globex"}
{"tenant": "globex", "store": "vertex_search", "ledger_current": 3, "status": "no store", "hint": "no Vertex AI Search data store 'documind-globex' in global: MANAGED_SEARCH=true make plan / make up declares one per tenant (managed.tf)"}
{"tenant": "zeta", "store": "rag_engine", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
{"tenant": "zeta", "store": "vertex_search", "ledger_current": 7, "held": 7, "missing": 0, "orphans": 0, "status": "in sync", "missing_doc_keys": [], "orphan_doc_keys": []}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Ask the stores, and find who found the cited chunk / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (acme's pin back to RAG Engine, then one question for each tenant).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=rag_engine
acme: retrieval_backend rag_engine, policy_fallback 0; pool 17, 14 from a managed store
  A: A confirmed employee at grade E3 or above serves a notice period of 60 days [2].
  cites acme:acme_497809ff...#rag-c31c1f459b60 (hr_policy_2026.md)
zeta: retrieval_backend vertex_search, policy_fallback 0; pool 12, 12 from a managed store
  A: A confirmed employee at grade L4 or above serves a notice period of 30 days [1].
  cites zeta:zeta_e920a147...#vs-9b9cb379153b (hr_policy_zeta_2026.md)
globex: retrieval_backend vector, policy_fallback 0; pool 20, 0 from a managed store
  A: Either party may terminate the agreement for convenience on 120 days' written notice [1].
  cites globex:a0d13745...#2 (msa_globex_2026.md)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: Ask the stores, and find who found the cited chunk / Do it**

The answer's citation carries no found_by, because the kit's Citation has no such field. The stamp is on the chunk in the pool. This cell asks the API again, then runs the kit's own retrieve() in your shell with backend rag_engine, the call the API made, and looks for the cited chunk in that pool.

Run instruction: bash — run in the operator shell, in the kit (the same question to the API, then through the kit's own retrieve()).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the API: retrieval_backend rag_engine, 14 of the pool's 17 chunks from the store
the same question through the kit's retrieve(), backend rag_engine: 17 chunks
  found_by rag_engine    14   for example acme:acme_497809ff...#rag-c31c1f459b60
  found_by (none)         3   for example acme:0994e77d...#0
the chunk the answer cites: acme:acme_497809ff...#rag-c31c1f459b60
  found_by rag_engine, score 0.706 (1 minus its distance), from hr_policy_2026.md
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: globex stays home: the skip, the ledger row, and a pin the policy overrides / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a note to globex, whose text may not leave India).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
>> gs://documind-ai-YOUR-ID-uploads/globex/globex_visitor_note_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	globex_f03a05df186ad39dec858f13c24a17424d7d35438eb57faf83d2f1144d9aee29	1	0	1	0	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=globex_visitor_note_2026.md API=<candidate url>
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it.py

**HTML: globex stays home: the skip, the ledger row, and a pin the policy overrides / Do it**

Then read what the worker's mirror said about the note, and the ledger row it stamped:

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the worker's mirror lines for globex since 2026-09-24T07:30:00Z:
  07:30:09 mirror_policy_skipped  store rag_engine    region us-central1 data_region in
  07:30:10 mirror_policy_skipped  store vertex_search region global      data_region in
the ledger row for globex/globex_visitor_note_2026.md: status indexed, mirrored {}
globex's data_region, as GET /v1/sources reports it: in
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_do_it.py

**HTML: globex stays home: the skip, the ledger row, and a pin the policy overrides / Do it**

If your lines are missing, the worker instance that took the note had already said it: the skip is said once per tenant and store per instance. The cell then prints the last week's lines instead, and the empty mirrored on the row is the record for this document. Last, try to move globex's text with a pin:

Run instruction: bash — run in the operator shell, in the kit (globex pinned to a store for one question, then unpinned).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
globex: retrieval_backend=rag_engine
globex: retrieval_backend vector, policy_fallback 1; pool 20, 0 from a managed store
  A: Either party may terminate the agreement for convenience on 120 days' written notice [1].
  cites globex:a0d13745...#2 (msa_globex_2026.md)
globex: retrieval_backend=default
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

26 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 16 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
