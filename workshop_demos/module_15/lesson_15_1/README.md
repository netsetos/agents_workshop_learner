# Lesson 15.1: Build graph evidence from source documents

**Summary:** node and edge counts. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.1-graph-evidence/Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html); Git blob `d74daf0dbbc7f95660f0a56970362cc9c013c26a`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the rules, run; no model, no network) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build) |
| s5 · window 14 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (reads only) |
| s6 · window 16 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (one extraction against its passage; then the build again) |

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

**HTML: The rules, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the rules, run; no model, no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
extraction: gemini-3.1-flash-lite, entity types person, org, product, policy, system, location, date
resolution: normalise(), then text-embedding-005 cosine >= 0.92
  normalise('ACME Pvt. Ltd.'        ) = 'acme'
  normalise('Acme Private Limited'  ) = 'acme'
  normalise('ACME Inc'              ) = 'acme'
  normalise('function head'         ) = 'function head'
  normalise('Function Head'         ) = 'function head'
  normalise('CFO'                   ) = 'cfo'
  normalise('Chief Financial Officer') = 'chief financial officer'
resolve_entities(), with an embedding that tells every name apart:
  'ACME Pvt. Ltd.'         -> 'ACME Pvt. Ltd.'
  'Acme Private Limited'   -> 'ACME Pvt. Ltd.'
  'ACME Inc'               -> 'ACME Pvt. Ltd.'
  'function head'          -> 'function head'
  'Function Head'          -> 'function head'
  'CFO'                    -> 'CFO'
  'Chief Financial Officer' -> 'Chief Financial Officer'
build_graph() on two passages:
  node 'CFO'                    person  id f3f1496ddec9...  cited by ['c1']
  node 'Purchase approval'      policy  id 36787430c7d6...  cited by ['c1']
  node 'Travel reimbursement'   policy  id 0cbc68db5bda...  cited by ['c2']
  node 'function head'          person  id b4468c254418...  cited by ['c1', 'c2']
  edge CFO -[APPROVES]-> Purchase approval  from c1, confidence 0.9
  edge function head -[APPROVES]-> Travel reimbursement  from c2, confidence 0.9
  2 relations dropped: 'board' is no entity (dangling), and Function Head -[IS]-> itself
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Build the handbook's graph / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --dry-run
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --rebuild
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 11}
tenant acme: 0 graph_edges deleted
tenant acme: 0 graph_nodes deleted
25 nodes, 15 edges written for tenant acme (Firestore)
{"event": "graph_built", "tenant": "acme", "backend": "firestore", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Read it back: the counts, and one edge with its source / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
tenant acme: 25 nodes, 15 edges in Firestore
the nodes the most chunks cite:
  Earned leave                     policy  3 chunk(s)
  Notice period                    policy  2 chunk(s)
  function head                    person  2 chunk(s)
  probation                        policy  2 chunk(s)
one edge, read back with its source chunk:
  CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval   confidence 0.9
  stated in acme:497809ffbaa6...#9 (FIN-02, hr_policy_2026.md):
    FIN-02 — Purchase approval
    Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
    approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  both names in the passage as written: CFO yes, Purchase approval yes
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: Audit an extraction, and build again / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (one extraction against its passage; then the build again).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the extraction cached for FIN-02 (gemini-3.1-flash-lite), beside its passage:
  | FIN-02 — Purchase approval
  | Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
  | approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  entity   'Purchase approval'    policy  in the passage as written
  entity   'function head'        person  in the passage as written
  entity   'CFO'                  person  in the passage as written
  relation function head -[APPROVES_UP_TO_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
  relation CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
3 of 3 entity names are in the passage as written; 11 extractions cached for acme
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 0}
25 nodes, 15 edges written for tenant acme (Firestore)
{"event": "graph_built", "tenant": "acme", "backend": "firestore", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

17 code windows mapped: 6 IDE demo files, 1 shared setup blocks, 10 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
