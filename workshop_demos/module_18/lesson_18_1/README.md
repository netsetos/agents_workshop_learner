# Lesson 18.1: Trace and authorize gateway routes

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_gateway_routes.py](demo_01_gateway_routes.py) | Inspect gateway routes and their configured destinations. |
| 3 | [demo_02_gateway_authorization.py](demo_02_gateway_authorization.py) | Exercise the authenticated route and deployment checks. |
| 4 | [demo_03_routing_and_cost_headers.py](demo_03_routing_and_cost_headers.py) | Trace PAN rerouting and inspect the returned cost metadata. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The intended gateway backend services and IAM configuration.

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

### demo_01_gateway_routes.py

Inspect gateway routes and their configured destinations.

**`step_01_example(session)` — The hook's decisions, traced / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model).

Expected shape, not a promised result:

```text
en_core_web_lg installed: the image's model, 400 MB
```

**`step_02_example(session)` — The hook's decisions, traced / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network).

Expected shape, not a promised result:

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

### demo_02_gateway_authorization.py

Exercise the authenticated route and deployment checks.

**`step_01_example(session)` — The token the proxy sends / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the token proxy's token, with the metadata server stood in; no network).

Expected shape, not a promised result:

```text
the SLM, first call       <token 1>   minted so far: 1
the SLM, a minute later   <token 1>   minted so far: 1
the SLM, 55 minutes in    <token 2>   minted so far: 2
the vLLM engine           <token 3>   minted so far: 3
the proxy drops these request headers, then adds its own Authorization: authorization, connection, content-length, host, transfer-encoding
```

**`step_02_example(session)` — The gateway, deployed and smoke-tested / Do it**

Do it

Operation: bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state).

Expected shape, not a promised result:

```text
...
>> gateway: https://documind-gateway-NUMBER.asia-south1.run.app (the API and the UI's account may call it)
```

**`step_03_example(session)` — The gateway, deployed and smoke-tested / Do it**

Do it

Operation: bash — run in the operator shell, in the kit.

Expected shape, not a promised result:

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

### demo_03_routing_and_cost_headers.py

Trace PAN rerouting and inspect the returned cost metadata.

**`step_01_example(session)` — A PAN re-routed, and the cost header / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (three short answers through the gateway).

Expected shape, not a promised result:

```text
documind-general is priced at 1.50 and 7.50 USD a million tokens, in and out (config.yaml)
  no personal data  HTTP 200  answered by gemini-3.6-flash; 11 tokens in, 20 out; x-litellm-response-cost 0.0001665
  a bare PAN        HTTP 200  answered by gemini-3.6-flash; 16 tokens in, 20 out; x-litellm-response-cost 0.000174
  a PAN and a date  HTTP 500  no answer: the route the hook chose has no backend yet, and no fallback
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html`. All 24 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `99278f7195b558586eb8943607137376aa5cbb66`.
