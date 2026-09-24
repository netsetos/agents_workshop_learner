# Lesson 18.1: Trace and authorize gateway routes

**Summary:** a PAN re-routed; the cost header. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html); Git blob `99278f7195b558586eb8943607137376aa5cbb66`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model) |
| s3 · window 10 | [demo_03_02_do_it.py](demo_03_02_do_it.py) | bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network) |
| s4 · window 14 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state) |
| s5 · window 19 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit |
| s6 · window 23 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (three short answers through the gateway) |

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

**HTML: The hook's decisions, traced / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
en_core_web_lg installed: the image's model, 400 MB
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it.py

**HTML: The hook's decisions, traced / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Presidio's recognizers: CreditCard, Crypto, Date, Email, Iban, Ip, MacAddress, MedicalLicense, Nhs, Phone, Spacy, Url, UsBank, UsItin, UsLicense, UsPassport, UsSsn
the classifier's own test cases, which nothing runs:
  'What is GDPR?'                  expected PUBLIC       got PUBLIC
  'Email me at user@acme.com'      expected CONFIDENTIAL got CONFIDENTIAL
  'My Aadhaar is 2345-6789-0123'   expected RESTRICTED   got PUBLIC
  'SSN 123-45-6789'                expected RESTRICTED   got PUBLIC
  'PAN ABCDE1234F'                 expected RESTRICTED   got PUBLIC
the hook, on four requests for documind-general:
  PUBLIC       -> documind-general   'What is the notice period for a confirmed E3?'
  PUBLIC       -> documind-general   'My PAN is ABCDE1234F. What is the notice period for a confirmed E3?'
  RESTRICTED   -> documind-sensitive 'My PAN is ABCDE1234F and I joined on 5 March 2026. What is my notice period?'
  CONFIDENTIAL -> documind-general   'Context:'
and what the last one sends to Gemini:
  Context:
  [Source 1] hr_policy_<URL>
  NP-03. A confirmed <US_DRIVER_LICENSE> serves a notice period of <DATE_TIME>. Queries go to <EMAIL_ADDRESS>.
  
  Question: What is the notice period for a confirmed <US_DRIVER_LICENSE>?
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The token the proxy sends / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the SLM, first call       <token 1>   minted so far: 1
the SLM, a minute later   <token 1>   minted so far: 1
the SLM, 55 minutes in    <token 2>   minted so far: 2
the vLLM engine           <token 3>   minted so far: 3
the proxy drops these request headers, then adds its own Authorization: authorization, connection, content-length, host, transfer-encoding
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The gateway, deployed and smoke-tested / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
>> gateway: https://documind-gateway-NUMBER.asia-south1.run.app (the API and the UI's account may call it)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: The gateway, deployed and smoke-tested / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
DocuMind gateway - live smoke test
  target: https://documind-gateway-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] no token is refused at the door  HTTP 403
  [PASS] liveliness as the member's account  HTTP 200 in ...s
  [PASS] documind-general answers JSON  '{"ok": true}' in ...s, model gemini-3.6-flash
  [PASS] the cost header rag-api prices from  x-litellm-response-cost=3.45e-05
  [PASS] a PAN is routed by the guardrail  served by 'gemini-3.6-flash' in ...s (the sensitive route is the self-hosted model, no fallback)
  [PASS] documind-slm answers, or its fallback does  model 'gemini-3.6-flash' in ...s, cost 1.8e-05
  --------------------------------------------------------
  6 passed, 0 failed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: A PAN re-routed, and the cost header / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (three short answers through the gateway).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-general is priced at 1.50 and 7.50 USD a million tokens, in and out (config.yaml)
  no personal data  HTTP 200  answered by gemini-3.6-flash; 11 tokens in, 20 out; x-litellm-response-cost 0.0001665
  a bare PAN        HTTP 200  answered by gemini-3.6-flash; 16 tokens in, 20 out; x-litellm-response-cost 0.000174
  a PAN and a date  HTTP 500  no answer: the route the hook chose has no backend yet, and no fallback
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

24 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 15 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
