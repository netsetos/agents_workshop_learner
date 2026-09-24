# Lesson 17.2: Validate sanitized datasets and run managed tuning

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_sanitize_and_validate.py](demo_01_sanitize_and_validate.py) | Run the sanitization/validation gates and inspect the accepted dataset. |
| 3 | [demo_02_submit_managed_tuning.py](demo_02_submit_managed_tuning.py) | Submit the reviewed dataset and retain the exact tuning job identity. |
| 4 | [demo_03_poll_and_inspect_tuned_endpoint.py](demo_03_poll_and_inspect_tuned_endpoint.py) | Resume polling that job and inspect its resulting endpoint and configuration. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The reviewed sanitized datasets from 17.1. Submission creates a billed tuning job; resume polling the saved job instead of resubmitting.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

Prepare this lesson's saved settings and dependencies before its live experiments.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Operation: bash — run in the operator shell now, before the lesson's first step.

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

### demo_01_sanitize_and_validate.py

Run the sanitization/validation gates and inspect the accepted dataset.

**`step_01_example(session)` — The checks that run before the spend / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the two self-tests and the rules; no network).

Expected shape, not a promised result:

```text
selftest: the evidence rule dropped jn-06's chunk and kept EMEA elsewhere and lk-09's 8, the question rule dropped lk-06's twin, the PAN row dropped, two formats agree, ModelDraft parses, the batch round trip holds
selftest: an untunable base and a rank the SDK cannot spell are refused before submission; adapter 4 is ADAPTER_SIZE_FOUR and the SDK accepts it
gemini-3.6-flash, adapter 4: refused before submission: managed SFT accepts ['gemini-3.1-flash-lite', 'gemini-3.5-flash'] as of 2026-09-04
gemini-3.1-flash-lite, adapter 3: refused before submission: the LoRA rank must be one of [1, 2, 4, 8, 16, 32]
gemini-3.1-flash-lite, adapter 32: accepted, ADAPTER_SIZE_THIRTY_TWO
make tune's defaults: {'epoch_count': 3, 'adapter_size': 'ADAPTER_SIZE_FOUR', 'tuned_model_display_name': 'documind-sft-v1'}
an endpoint whose path says us is called at: us; with GENERATOR_LOCATION=us-central1: us-central1
```

**`step_02_example(session)` — The frozen file, validated / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (reads the bucket and Firestore; one DLP scan in asia-south1).

Expected shape, not a promised result:

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

### demo_02_submit_managed_tuning.py

Submit the reviewed dataset and retain the exact tuning job identity.

**`step_01_example(session)` — The job, submitted / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (submits the job and returns: the billed act).

Expected shape, not a promised result:

```text
python evals/tune.py --project documind-ai-YOUR-ID --dataset gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_${VERSION:-v1}.vertex.jsonl \
  --base gemini-3.1-flash-lite --epochs 3 --adapter 4 --display-name documind-sft-v2 --no-wait
  submitted projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473 on gemini-3.1-flash-lite: 3 epochs, adapter 4, dataset gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.vertex.jsonl
  poll later: python evals/tune.py --project documind-ai-YOUR-ID --poll projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473
JOB=projects/NUMBER/locations/us-central1/tuningJobs/7240862654976436473
```

### demo_03_poll_and_inspect_tuned_endpoint.py

Resume polling that job and inspect its resulting endpoint and configuration.

**`step_01_definition(session)` — The endpoint, and where it answers / Definition**

The first cell polls the job once a minute until it ends. The poll only reads, so it costs nothing, and after a disconnect it is safe to run again: it takes the job from step 5's log. When the job succeeds, tune.py prints: The cell keeps the endpoint in ~/poll172.log and in ENDPOINT.

Operation: bash — run in the operator shell, in the kit (waits for the job, a line a minute).

Expected shape, not a promised result:

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

**`step_02_definition(session)` — The endpoint, and where it answers / Definition**

The cell keeps the endpoint in ~/poll172.log and in ENDPOINT. The second cell asks the endpoint one question the way the generator would. It sends SYSTEM, one source under its header and the question, with generator._call's settings: ModelDraft's schema, 2,048 tokens and thinking at LOW. The chunk is not one the rows were written from, and the question is not a golden one. The cell asks in three places: us-central1, the job's region; global, where the served model answers; and the location the generator would use, from the path.

Operation: bash — run in the operator shell, in the kit (one answer from the endpoint, and two calls that are not found).

Expected shape, not a promised result:

```text
the endpoint's path says us; the generator would call it at us
  us-central1  404 NOT_FOUND
  global       404 NOT_FOUND
  us           answered: 429 tokens in, 97 out; a ModelDraft, answerable True, 1 citation(s), 0 [N] marks in the answer
  the answer: No. A loss of wages from withholding an increment for a good and sufficient cause is not deemed a deduction from wages, where the employer's provisions meet the requirements the appropriate Government notifies.
  the price: Rs 0.0322 as Google bills a tuned Gemini 3 endpoint (1.5 x flash-lite); cost.py would log Rs 0.0215
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.2-managed-tuning/Netsetos_GCP_Capstone_17.2_Managed_Tuning_WIX.html). All 22 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `375a22387caec2be91dbd584d47b3fc5c7046157`.
