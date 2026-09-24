# Lesson 15.2: Compare Firestore and Spanner graph paths

**Summary:** the CFO question answered without the word CFO. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html); Git blob `7bdd37f0afd091fd34fa8e7a5d9f1fd4a8127ad2`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the seeding rules, run; then the kit's tests; no model, no network) |
| s4 · window 11 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (two walks of the Firestore graph; reads only) |
| s5 · window 15 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (the same graph written to Spanner, then read back) |
| s5 · window 17 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit (one walk of the Spanner graph, seeded by meaning; one embedding call) |
| s6 · window 21 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (a candidate with no traffic: the walk on, from Firestore; one question) |
| s6 · window 23 | [demo_06_02_do_it.py](demo_06_02_do_it.py) | bash — run in the operator shell, in the kit (the same candidate, the walk from Spanner; the same question) |
| s6 · window 26 | [demo_06_03_do_it.py](demo_06_03_do_it.py) | bash — run in the operator shell, in the kit (the template put back, the tag dropped; the live revision was never touched) |

## Conditional recovery

- [recover_06_01_do_it.py](recover_06_01_do_it.py) — bash — run only if step 5 seeded nothing (the threshold, on the candidate alone)

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

**HTML: The seeders, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the seeding rules, run; then the kit's tests; no model, no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
eight names from the handbook's graph: Purchase approval, function head, CFO, Travel reimbursement, Notice period, probation, India, Remote work
Who signs off on a big purchase?
  candidate names ['who signs off on a big purchase?']
  seeds by containment: none   auto: vector
Which purchases need the CFO?
  candidate names ['which purchases need the cfo?']
  seeds by containment: CFO   auto: graph
What does the CFO approve?
  candidate names ['what does the cfo approve?']
  seeds by containment: CFO   auto: vector
Who approves a purchase above two lakh?
  candidate names ['who approves a purchase above two lakh?']
  seeds by containment: none   auto: vector
Who approves a Purchase above two lakh?
  candidate names ['purchase']
  seeds by containment: Purchase approval   auto: graph
Who handles Indian travel claims?
  candidate names ['indian']
  seeds by containment: India   auto: graph
........
----------------------------------------------------------------------
Ran 8 tests in 0.004s

OK
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The Firestore path: a name the question contains / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (two walks of the Firestore graph; reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --ask "Who signs off on a big purchase?"
{
 "question": "Who signs off on a big purchase?",
 "backend": "firestore",
 "seeded_by": "containment",
 "seeds": [],
 "nodes": [],
 "chunk_ids": []
}
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --ask "Which purchases need the CFO?"
{
 "question": "Which purchases need the CFO?",
 "backend": "firestore",
 "seeded_by": "containment",
 "seeds": [
  "CFO"
 ],
 "nodes": [
  "CFO",
  "Purchase approval"
 ],
 "chunk_ids": [
  "acme:497809ffbaa603c49577add351033f4374ad1aefa3394f761be0c9df5e3f3173#9"
 ]
}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The Spanner path: build it, read it, walk it by meaning / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the same graph written to Spanner, then read back).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend spanner --source hr_policy_2026.md --rebuild
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 0}
{"event": "graph_built", "tenant": "acme", "backend": "spanner", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
tenant acme: 25 nodes (25 with a 768-number vector), 15 edges in Spanner
the edges that name the CFO, as tables (the names joined from GraphNode):
  CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval   stated in FIN-02
one hop from CFO, by the kit's GQL walk: CFO, Purchase approval
  the chunks they cite: FIN-02
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: The Spanner path: build it, read it, walk it by meaning / Do it**

The CFO's edge came back two ways. As tables, GraphEdge is joined to GraphNode twice, for the names at both ends. As a graph, the kit's GQL walk goes from the CFO. Both reach Purchase approval and FIN-02. Now the kit's question, seeded by meaning. On Spanner, --ask prints the five nearest names, each with its distance and whether it passed 0.4. Then it walks from the names that passed.

Run instruction: bash — run in the operator shell, in the kit (one walk of the Spanner graph, seeded by meaning; one embedding call).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend spanner --ask "Who signs off on a big purchase?"
{
 "question": "Who signs off on a big purchase?",
 "backend": "spanner",
 "seeded_by": "meaning",
 "seed_distance": 0.4,
 "nearest": [
  {
   "name": "Purchase approval",
   "kind": "policy",
   "distance": 0.183,
   "seeded": true
  },
  {
   "name": "CFO",
   "kind": "person",
   "distance": 0.415,
   "seeded": false
  },
  {
   "name": "approved cloud bucket",
   "kind": "system",
   "distance": 0.434,
   "seeded": false
  },
  {
   "name": "tax clearance",
   "kind": "policy",
   "distance": 0.434,
   "seeded": false
  },
  {
   "name": "Travel reimbursement",
   "kind": "policy",
   "distance": 0.459,
   "seeded": false
  }
 ],
 "seeds": [
  "Purchase approval"
 ],
 "nodes": [
  "Purchase approval",
  "function head",
  "CFO"
 ],
 "chunk_ids": [
  "acme:497809ffbaa603c49577add351033f4374ad1aefa3394f761be0c9df5e3f3173#5",
  "acme:497809ffbaa603c49577add351033f4374ad1aefa3394f761be0c9df5e3f3173#9"
 ]
}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The walk in front of the dense pool, on a candidate / Do it**

First with the walk from Firestore:

Run instruction: bash — run in the operator shell, in the kit (a candidate with no traffic: the walk on, from Firestore; one question).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|...|RETRIEVAL_GRAPH=auto|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
/version: retrieval_graph=auto graph_backend=firestore embedding=text-embedding-005@1
Q: Who signs off on a big purchase?
A: Purchases up to Rs 2,00,000 are approved by the function head; above that, the CFO approves [1].
pool 20: the walk put 0 chunk(s) first; retrieval_backend vector
cites FIN-02 (hr_policy_2026.md): Purchases up to Rs 2,00,000 are approved by the function head.
the word CFO: not in the question, in the answer
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it.py

**HTML: The walk in front of the dense pool, on a candidate / Do it**

First with the walk from Firestore: Then the same candidate, walking from Spanner:

Run instruction: bash — run in the operator shell, in the kit (the same candidate, the walk from Spanner; the same question).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|...|RETRIEVAL_GRAPH=auto|GRAPH_BACKEND=spanner|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
/version: retrieval_graph=auto graph_backend=spanner embedding=text-embedding-005@1
Q: Who signs off on a big purchase?
A: Purchases up to Rs 2,00,000 are approved by the function head; above that, the CFO approves [1].
pool 20: the walk put 2 chunk(s) first; retrieval_backend vector
cites FIN-02 (hr_policy_2026.md): Purchases up to Rs 2,00,000 are approved by the function head.
the word CFO: not in the question, in the answer
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_06_01_do_it.py

**HTML: The walk in front of the dense pool, on a candidate / Do it**

Notice what the first answer says, too. Dense retrieval found FIN-02 without any graph, because the handbook is small and the clause says "purchase". The Spanner walk made sure FIN-02 was in the pool whatever the dense ranking did. On a corpus where the answer's words are far from the question's, that is the difference. Set the threshold on the candidate alone, from your own numbers, and ask again. make candidate cannot pass it (step 7 says why), so this is a gcloud line:

Run instruction: bash — run only if step 5 seeded nothing (the threshold, on the candidate alone).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_do_it.py

**HTML: The walk in front of the dense pool, on a candidate / Do it**

Choose a value just past the purchase or approval name, and below the first name that has nothing to do with purchases. The undo below removes it. Last, put the template back. Environment variables carry over from one revision to the next, so the candidate's settings would ride into the next gcloud run services update of the API. The undo writes RETRIEVAL_GRAPH=off and GRAPH_BACKEND=firestore, removes any GRAPH_SEED_DISTANCE, drops the tag, and deletes .candidate-revision.

Run instruction: bash — run in the operator shell, in the kit (the template put back, the tag dropped; the live revision was never touched).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
100	documind-api-000NN-xxx
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

27 code windows mapped: 10 IDE demo files, 1 shared setup blocks, 16 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
