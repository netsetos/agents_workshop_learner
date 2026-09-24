# Lesson 18.2: Serve a supplied or stock model using Ollama

**Summary:** the cold start timed; a gated answer from the small model. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html); Git blob `d166600ec95e7f9de71575062e0a57c623378f5c`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 7 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell (once: a venv with a transformers that can read the tokenizer) |
| s3 · window 8 | [demo_03_02_do_it.py](demo_03_02_do_it.py) | bash — run in the operator shell, in the kit (downloads the tokenizer's files, about 31 MB; no GPU, no Google Cloud) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (reads the kit's files; no network) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (a GPU service: it bills while an instance lives) |
| s5 · window 19 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit, right after the deploy |
| s6 · window 21 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, after documind-slm has been idle for more than 10 minutes |
| s7 · window 25 | [demo_07_01_do_it.py](demo_07_01_do_it.py) | bash — run in the operator shell, in the kit (lesson 18.1's three requests, through the gateway) |
| s7 · window 27 | [demo_07_02_do_it.py](demo_07_02_do_it.py) | bash — run in the operator shell, in the kit (a no-traffic revision; the live one keeps its settings) |
| s7 · window 29 | [demo_07_03_do_it.py](demo_07_03_do_it.py) | bash — run in the operator shell, in the kit (one golden question through the candidate) |
| s7 · window 31 | [demo_07_04_do_it.py](demo_07_04_do_it.py) | bash — run in the operator shell, in the kit (the gate, scoped to the HR policy's rows) |
| s7 · window 33 | [demo_07_05_do_it.py](demo_07_05_do_it.py) | bash — run in the operator shell (reads the gate's report) |
| s7 · window 35 | [demo_07_06_do_it.py](demo_07_06_do_it.py) | bash — run in the operator shell, in the kit, when you are done |

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

**HTML: A Modelfile from the tokenizer / Do it**

Do it

Run instruction: bash — run in the operator shell (once: a venv with a transformers that can read the tokenizer).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it.py

**HTML: A Modelfile from the tokenizer / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (downloads the tokenizer's files, about 31 MB; no GPU, no Google Cloud).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
[transformers] PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
# GENERATED by make_modelfile.py from the tokenizer. Do not hand-edit.
# Regenerate whenever the checkpoint changes - the template belongs to the
# weights, not to the project.

FROM ./documind-slm.gguf

TEMPLATE """<bos><|turn>user
{{ .Prompt }}<turn|>
<|turn>model
"""

PARAMETER stop "<turn|>"

PARAMETER num_ctx 4096
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The waits and the bill, from the kit / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the kit's files; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the SLM: 1 nvidia-l4, 8 vCPU, 32Gi; 0 to 1 instance; 4 requests at a time; 600 s a request
its startup probe: /api/tags after 10 s, every 5 s, 30 failures allowed: 160 s for Ollama to list the model
make smoke-slm waits 240 s a call
a gate row: run_eval waits 90 s for the API, and asks once more two seconds after a timeout
the API waits 90 s for the gateway (GATEWAY_TIMEOUT_S)
the gateway waits 110 s for documind-slm, then falls back to documind-general
the gateway waits 110 s for documind-sensitive, then stops: it has no fallback
the bill, by the instance: (0.0001867 + 8 x 0.000018 + 32 x 0.000002) USD a second = 1.4209 USD an hour = Rs 120.78
  up to 10 idle minutes after the last request: Rs 20.13; min-instances 1 for a 720-hour month: Rs 86,960
  the kit's own figure: Rs 86,904/month, at $1.42 an hour
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The stand-in, deployed and smoke-tested / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a GPU service: it bills while an instance lives).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> stand-in: gemma3:4b will be served as documind-slm
gcloud run deploy documind-slm \
  --source services/slm --region us-central1 --project documind-ai-YOUR-ID \
  --gpu 1 --gpu-type nvidia-l4 --no-gpu-zonal-redundancy \
  --cpu 8 --memory 32Gi \
  --max-instances 1 --min-instances 0 --timeout 600 --concurrency 4 \
  --no-allow-unauthenticated --labels slm-source=stock \
  --startup-probe httpGet.path=/api/tags,httpGet.port=8080,initialDelaySeconds=10,periodSeconds=5,failureThreshold=30 --quiet
...
>> slm: https://documind-slm-NUMBER.us-central1.run.app (min-instances 0; make slm-off after every session anyway)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: The stand-in, deployed and smoke-tested / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit, right after the deploy.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
DocuMind SLM - live smoke test
  target: https://documind-slm-NUMBER.us-central1.run.app
  --------------------------------------------------------
  [PASS] /api/tags lists documind-slm  HTTP 200 in 0.1s (cold start included): ['documind-slm:latest']
  [PASS] /api/generate answers  'OK' in 12.0s
  [PASS] /v1/chat/completions answers (the OpenAI-compatible door)  'OK' in 0.6s
  [PASS] through the gateway's documind-slm route  HTTP 200, served by 'ollama_chat/documind-slm' in 0.6s
  [PASS] what the service serves  stock	us-central1-docker.pkg.dev/documind-ai-YOUR-ID/cloud-run-source-deploy/documind-slm@sha256:DIGEST
  --------------------------------------------------------
  5 passed, 0 failed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The cold start, timed / Do it**

Do it

Run instruction: bash — run in the operator shell, after documind-slm has been idle for more than 10 minutes.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
/api/tags              41.4 s   documind-slm:latest (4.3B, Q4_K_M)
/api/generate, first   12.0 s   'OK'
/api/generate, again    0.6 s   'OK'
a cold start: 53.4 s to the first answer - 41.4 s for an instance, then 11.4 s to load the model into the GPU
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (lesson 18.1's three requests, through the gateway).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
USD a million tokens, in and out (config.yaml): documind-general 1.50 and 7.50, documind-sensitive 20.50 and 20.50
  no personal data  HTTP 200  answered by gemini-3.6-flash; 11 tokens in, 1 out; x-litellm-response-cost 2.4e-05
  a bare PAN        HTTP 200  answered by gemini-3.6-flash; 16 tokens in, 1 out; x-litellm-response-cost 3.15e-05
  a PAN and a date  HTTP 200  answered by ollama_chat/documind-slm; 19 tokens in, 30 out; x-litellm-response-cost 0.0010045
                    Your notice period depends on your grade and confirmation status; the documents you shared do not say which applies to you.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a no-traffic revision; the live one keeps its settings).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=documind-slm|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=gateway|ARMOR=off|SEMANTIC_CACHE=off|RETRIEVAL_CURRENT_ONLY=off|RETRIEVAL_GRAPH=off|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-xxx (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (one golden question through the candidate).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lk-06: What is the notice period for a confirmed E3?
answer: A confirmed E3 serves a notice period of 60 days [1].
  cites acme:lk-06#0
model documind-slm, backend gateway: the route the API asked for, whoever answered
cost 0.03977 USD for 1900 tokens in and 40 out: documind-slm's rate, so the small model answered
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_04_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the gate, scoped to the HR policy's rows).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://candidate---documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate        90.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 9 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 9 rows)
  [PASS] must_contain_rate      88.9%  (threshold 85%; 9 rows)
  [PASS] correct_rate           80.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  [ -- ] media_kind_rate         0.0%  (threshold 80%; no rows in scope; 0 rows)
  [ -- ] isolation_403_rate      0.0%  (threshold 100%; no rows in scope; 0 rows)
  [info] quote_support_rate      ...  (quoted words found in the tenant's corpus text; not a threshold - a Doc AI extraction and a pypdf mirror hyphenate differently)

  shape        rows   ok   pass
  lookup          9    9      7
  version         1    1      1
  latency ms  p50   ...  p95   ...   (round trip, 10 rows)
  retrieve_ms p50   ...  p95   ...
  rerank_ms   p50   ...  p95   ...
  generate_ms p50   ...  p95   ...
  pool        avg   ...   semantic cache hits 0

  rows that cost a point (2):
    lk-02  lookup    acme    answered without ['15 June'] | 'form 16 is issued every june [1].'
    lk-08  lookup    acme    REFUSED conf=low cites=0 | Who approves a purchase of Rs 3,00,000?

  report: /home/YOU/slm182.json
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_05_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell (reads the gate's report).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lk-06: pass, 1 citation(s); the route it asked for: documind-slm, through the gateway
8 of 10 rows passed; all thresholds met
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_06_do_it.py

**HTML: The small model behind the gateway and the API / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit, when you are done.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
gcloud run services update documind-slm --region us-central1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
...
documind-slm scaled to zero
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

36 code windows mapped: 14 IDE demo files, 1 shared setup blocks, 21 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
