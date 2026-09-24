# Lesson 17.2: Validate sanitized datasets and run managed tuning

**Summary:** the job id; the endpoint path with its location. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.2-managed-tuning/Netsetos_GCP_Capstone_17.2_Managed_Tuning_WIX.html); Git blob `375a22387caec2be91dbd584d47b3fc5c7046157`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the two self-tests and the rules; no network) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (reads the bucket and Firestore; one DLP scan in asia-south1) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (submits the job and returns: the billed act) |
| s6 · window 19 | [demo_06_01_definition.py](demo_06_01_definition.py) | bash — run in the operator shell, in the kit (waits for the job, a line a minute) |
| s6 · window 21 | [demo_06_02_definition.py](demo_06_02_definition.py) | bash — run in the operator shell, in the kit (one answer from the endpoint, and two calls that are not found) |

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

**HTML: The checks that run before the spend / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the two self-tests and the rules; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
selftest: the evidence rule dropped jn-06's chunk and kept EMEA elsewhere and lk-09's 8, the question rule dropped lk-06's twin, the PAN row dropped, two formats agree, ModelDraft parses, the batch round trip holds
selftest: an untunable base and a rank the SDK cannot spell are refused before submission; adapter 4 is ADAPTER_SIZE_FOUR and the SDK accepts it
gemini-3.6-flash, adapter 4: refused before submission: managed SFT accepts ['gemini-3.1-flash-lite', 'gemini-3.5-flash'] as of 2026-09-04
gemini-3.1-flash-lite, adapter 3: refused before submission: the LoRA rank must be one of [1, 2, 4, 8, 16, 32]
gemini-3.1-flash-lite, adapter 32: accepted, ADAPTER_SIZE_THIRTY_TWO
make tune's defaults: {'epoch_count': 3, 'adapter_size': 'ADAPTER_SIZE_FOUR', 'tuned_model_display_name': 'documind-sft-v1'}
an endpoint whose path says us is called at: us; with GENERATOR_LOCATION=us-central1: us-central1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The frozen file, validated / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the bucket and Firestore; one DLP scan in asia-south1).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the file make tune VERSION=v2 reads: gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.vertex.jsonl
  vertex sha256 as the manifest says
  chat   sha256 as the manifest says
1. the shape: 315 of 315 rows are a system instruction, a user turn and a model turn, text only; the chat file says the same in 315; targets that parse as ModelDraft: 315
2. the test set: the golden set (65 rows) would drop 0 of 315
3. personal data, by the kit's own scan (DLP in asia-south1, LIKELY or above; findings, never the values):
   in the questions and answers, which make trainset scans: 0 rows
   in the chunks the user turns carry, which it does not: 1 row
     acme:cgst_act_2017#p1-0: EMAIL_ADDRESS
4. residency: the rows are acme's, whose data_region is any; may they be held in us-central1? True
5. the size: about 203,451 tokens an epoch by the kit's estimate (characters / 4); the longest row about 863 of the 131,072 Google allows
   3 epochs: about 610,353 training tokens, about Rs 156 at USD 3.00 a million
verdict: ready to tune: the manifest's bytes, the trainer's shape, no golden row, nothing where make trainset looks, and acme may leave India
         1 row carries a finding make trainset never looked for: read the chunks before you pay
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The job, submitted / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (submits the job and returns: the billed act).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python evals/tune.py --project documind-ai-YOUR-ID --dataset gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_${VERSION:-v1}.vertex.jsonl \
  --base gemini-3.1-flash-lite --epochs 3 --adapter 4 --display-name documind-sft-v2 --no-wait
  submitted projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473 on gemini-3.1-flash-lite: 3 epochs, adapter 4, dataset gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.vertex.jsonl
  poll later: python evals/tune.py --project documind-ai-YOUR-ID --poll projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473
JOB=projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_definition.py

**HTML: The endpoint, and where it answers / Definition**

The first cell polls the job once a minute until it ends. The poll only reads, so it costs nothing, and after a disconnect it is safe to run again: it takes the job from step 5's log. When the job succeeds, tune.py prints: The cell keeps the endpoint in ~/poll172.log and in ENDPOINT.

Run instruction: bash — run in the operator shell, in the kit (waits for the job, a line a minute).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
09:53:00 JobState.JOB_STATE_PENDING
  09:54:00 JobState.JOB_STATE_PENDING
  09:55:00 JobState.JOB_STATE_RUNNING
  ...      (a line a minute while the job runs: 33 more here)
  10:29:00 JobState.JOB_STATE_RUNNING
  JOB_STATE_SUCCEEDED
  tuned model : projects/NUMBER/locations/us/models/6156234374247085944@1
  endpoint    : projects/NUMBER/locations/us/endpoints/9136961803583303949

  serve it as a candidate revision, no traffic, and judge it:
    make candidate PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=projects/NUMBER/locations/us/endpoints/9136961803583303949 RAG_MODEL_BASE=gemini-3.1-flash-lite
    make eval-live PROJECT=documind-ai-YOUR-ID API=<the candidate url>
    make judge PROJECT=documind-ai-YOUR-ID API_B=<the candidate url>
ENDPOINT=projects/NUMBER/locations/us/endpoints/9136961803583303949
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_definition.py

**HTML: The endpoint, and where it answers / Definition**

The cell keeps the endpoint in ~/poll172.log and in ENDPOINT. The second cell asks the endpoint one question the way the generator would. It sends SYSTEM, one source under its header and the question, with generator._call's settings: ModelDraft's schema, 2,048 tokens and thinking at LOW. The chunk is not one the rows were written from, and the question is not a golden one. The cell asks in three places: us-central1, the job's region; global, where the served model answers; and the location the generator would use, from the path.

Run instruction: bash — run in the operator shell, in the kit (one answer from the endpoint, and two calls that are not found).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the endpoint's path says us; the generator would call it at us
  us-central1  404 NOT_FOUND
  global       404 NOT_FOUND
  us           answered: 429 tokens in, 97 out; a ModelDraft, answerable True, 1 citation(s), 0 [N] marks in the answer
  the answer: No. A loss of wages from withholding an increment for a good and sufficient cause is not deemed a deduction from wages, where the employer's provisions meet the requirements the appropriate Government notifies.
  the price: Rs 0.0322 as Google bills a tuned Gemini 3 endpoint (1.5 x flash-lite); cost.py would log Rs 0.0215
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

22 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 14 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
