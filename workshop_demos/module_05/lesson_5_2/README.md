# Lesson 5.2: Compare dense and hybrid retrieval

**Summary:** recall@k and MRR per arm on the golden set. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html); Git blob `b281bd202e28501bb0b9d45ea85ed4b27f37555d`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once per shell |
| s3 · window 12 | [demo_03_01_do_it_both_rulers_over_your_rows_rs_0.py](demo_03_01_do_it_both_rulers_over_your_rows_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell, then the same cell for a second question) |
| s4 · window 16 | [demo_04_01_do_it_dense_alpha_0_alpha_0_7.py](demo_04_01_do_it_dense_alpha_0_alpha_0_7.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding of a few dozen characters) |
| s5 · window 20 | [demo_05_01_do_it_fuse_the_saved_lists_compare_with_the_inde.py](demo_05_01_do_it_fuse_the_saved_lists_compare_with_the_inde.py) | bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the lists are on disk) |
| s6 · window 26 | [demo_06_01_do_it_a_wiring_check_then_acme_s_rows_with_a_led.py](demo_06_01_do_it_a_wiring_check_then_acme_s_rows_with_a_led.py) | bash — run in the operator shell, in $DEMO_ROOT (embeddings in paise; the Ranking API per request, a few rupees) |
| s7 · window 31 | [demo_07_01_do_it_hybrid_on_a_candidate_the_same_two_questio.py](demo_07_01_do_it_hybrid_on_a_candidate_the_same_two_questio.py) | bash — run in the operator shell (one new revision, no traffic; two version reads) |
| s7 · window 33 | [demo_07_02_do_it_hybrid_on_a_candidate_the_same_two_questio.py](demo_07_02_do_it_hybrid_on_a_candidate_the_same_two_questio.py) | bash — run in the operator shell (four questions, one or two rupees) |
| s7 · window 35 | [demo_07_03_do_it_hybrid_on_a_candidate_the_same_two_questio.py](demo_07_03_do_it_hybrid_on_a_candidate_the_same_two_questio.py) | bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live mode read again) |
| s8 · window 38 | [demo_08_01_where_hybrid_cannot_go.py](demo_08_01_where_hybrid_cannot_go.py) | bash — run in the operator shell, in $DEMO_ROOT (Rs 0: no call leaves the machine) |

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

### demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index endpoint, the deployed index and the retrieval settings live in the API's environment; steps 3, 4 and 7 use them. An empty value means the setting's default, which the page names where it matters; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and step 8's cell imports the kit. The ablation's sparse leg needs rank_bm25, which the kit's images do not carry because no service runs it; the pip line puts it in the venv once.

Run instruction: bash — run in the operator shell, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
mode: dense (default)  backend: vector
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_both_rulers_over_your_rows_rs_0.py

**HTML: The lane runs dense, and two sparse rulers over its own rows / Do it: both rulers over your rows, Rs 0**

The cell reads the text of every current acme row, no vectors, and scores each row twice for the invoice question; then run it again for the notice-period clause. Firestore reads of this size sit inside the free quota.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell, then the same cell for a second question).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
N current acme rows read, text only

index leg, hashed TF by dot product: anchor inv_2026_0412 at rank 9xx of N
   p28-1      industrial_relations_code_2020.pdf     35.500
   p32-0      cgst_act_2017.pdf                      34.000
   p7-0       payment_of_gratuity_act_1972.pdf       32.000

ablation leg, BM25: anchor inv_2026_0412 at rank 1 of N
   p1-0       inv_2026_0412.md                       21.949   <- anchor
   p36-0      cgst_act_2017.pdf                      16.609
   p40-0      cgst_act_2017.pdf                      16.514
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_dense_alpha_0_alpha_0_7.py

**HTML: Three ways through the index: dense, sparse only, fused / Do it: dense, alpha 0, alpha 0.7**

Do it: dense, alpha 0, alpha 0.7

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding of a few dozen characters).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
dense  first five (anchor at rank 1 of 20):
   p1-0       inv_2026_0412.md                     <- anchor
   p36-0      cgst_act_2017.pdf
   ...

sparse first five (anchor at rank None of 20):
   p28-1      industrial_relations_code_2020.pdf
   p32-0      cgst_act_2017.pdf
   ...

hybrid first five (anchor at rank 2 of 20):
   p36-0      cgst_act_2017.pdf
   p1-0       inv_2026_0412.md                     <- anchor
   ...

overlap of 20: dense/hybrid 18 | dense/sparse 2
saved /tmp/legs52.json for step 5
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_fuse_the_saved_lists_compare_with_the_inde.py

**HTML: RRF by hand: the kit's rule reproduces the server's order / Do it: fuse the saved lists, compare with the index's fused list**

Do it: fuse the saved lists, compare with the index's fused list

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the lists are on disk).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
by hand, alpha 0.7:
   p36-0 cgst_act_2017.pdf               0.01594   dense rank  2  sparse rank  4
   p1-0 inv_2026_0412.md                 0.01148   dense rank  1  sparse rank  -
   ...
the index's fused first five: ['p36-0 cgst_act_2017.pdf', 'p1-0 inv_2026_0412.md', ...]
heads agree on 5 of 5 | first is the same: True
alpha 1.0 gives the dense list back: True
alpha 0.0 gives the sparse list back: True
the bound: dense #1 0.01148, dense #20 0.00875, sparse #1 alone 0.00492
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_a_wiring_check_then_acme_s_rows_with_a_led.py

**HTML: The ablation: one knob per arm, no model in the loop / Do it: a wiring check, then acme's rows with a ledger**

The first run takes five rows and about a minute; the second takes acme's 40 rows and a few minutes, and appends one JSON line per arm to a ledger you keep. make ablate passes your exported REGION as the embedding region, which is where the API embeds; the direct call is the same line without make.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (embeddings in paise; the Ranking API per request, a few rupees).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
40 rows with anchors, NN anchors, one knob per arm (project documind-ai-YOUR-ID, embeddings in asia-south1, ranker on global)

arm                                          recall@depth  recall@5    mrr rows@1.0  p95 ms
dense 5, no reranker                                 0.9x      0.9x   0.8x       3x    xxxx
dense 20 -> rerank 5   (the lane)                    0.9x      0.9x   0.9x       3x    xxxx
       lost: lk-xx: PB-02 - ranked out (in the candidates, not the five)
dense 50 -> rerank 5                                 0.9x      0.9x   0.9x       3x    xxxx
hybrid 20 -> rerank 5  (4.5, not wired)              0.9x      0.9x   0.9x       3x    xxxx

Read it in this order: recall@depth is the reranker's ceiling - if the 20 and 50 rows agree, depth is not the knob;
recall@5 of the lane's row minus the first row is the reranker's lift, and p95 is what it costs;
the hybrid row says whether a BM25 leg is worth wiring - twenty of the anchors are clause codes, its home ground;
the rag_engine row (--arms all) is 4.3's corpus against the lane's own rows - a managed chunk that splits a clause from its code shows up as a miss.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_hybrid_on_a_candidate_the_same_two_questio.py

**HTML: The knob: hybrid on a candidate that takes no traffic, compared, then removed / Do it: hybrid on a candidate, the same two questions to both revisions, then undo**

Do it: hybrid on a candidate, the same two questions to both revisions, then undo

Run instruction: bash — run in the operator shell (one new revision, no traffic; two version reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-api-NUMBER                  mode dense | backend vector
candidate---documind-api-NUMBER      mode hybrid | backend vector
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_do_it_hybrid_on_a_candidate_the_same_two_questio.py

**HTML: The knob: hybrid on a candidate that takes no traffic, compared, then removed / Do it: hybrid on a candidate, the same two questions to both revisions, then undo**

Do it: hybrid on a candidate, the same two questions to both revisions, then undo

Run instruction: bash — run in the operator shell (four questions, one or two rupees).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
What is the total payable on invoice INV-2026-0412?
   documind-  ['  0 inv_2026_0412.md', ' 36 cgst_act_2017.pdf', ...] | retrieve_ms 6xx | pool 20 | vector_chunks 20
   candidate  ['  0 inv_2026_0412.md', ' 36 cgst_act_2017.pdf', ...] | retrieve_ms 7xx | pool 20 | vector_chunks 20
What is the notice period for a confirmed E3?
   documind-  ['  1 hr_policy_2026.md', '  4 hr_policy_2026.md', '  2 hr_policy_2026.md'] | retrieve_ms 6xx | pool 20 | vector_chunks 20
   candidate  ['  1 hr_policy_2026.md', '  4 hr_policy_2026.md', '  2 hr_policy_2026.md'] | retrieve_ms 7xx | pool 20 | vector_chunks 20
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_do_it_hybrid_on_a_candidate_the_same_two_questio.py

**HTML: The knob: hybrid on a candidate that takes no traffic, compared, then removed / Do it: hybrid on a candidate, the same two questions to both revisions, then undo**

Do it: hybrid on a candidate, the same two questions to both revisions, then undo

Run instruction: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live mode read again).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
live mode: dense
100;documind-api-00042-xyz
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_where_hybrid_cannot_go.py

**HTML: What hybrid costs, where it cannot go, and what the harness does not measure / Where hybrid cannot go**

Two places, one at startup and one at runtime. A managed backend has no sparse leg to fuse and the Firestore rung's vector index takes one dense vector and nothing else, so check_retrieval_modes() refuses both pairs before the service serves; a tenant pinned to a managed store under hybrid mode is served from the deployment's backend with a retrieval_pin_ignored line instead. At runtime the chaos rung applies to hybrid as to dense: an unreachable index degrades to the Firestore rung, which is dense only, with a vector_search_fallback line and never a 500. The cell asks the validator the two questions offline.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: no call leaves the machine).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
vector     hybrid -> allowed
firestore  hybrid -> refused: RETRIEVAL_MODE=hybrid needs RETRIEVAL_BACKEND=vector: the Firestore backend is dense-only. Set RETR...
rag_engine hybrid -> refused: RETRIEVAL_MODE=hybrid needs RETRIEVAL_BACKEND=vector: rag_engine embeds and searches on its own ...
firestore  dense  -> allowed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

40 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 28 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
