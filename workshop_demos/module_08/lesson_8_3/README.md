# Lesson 8.3: Exercise DLP, guardrails and audit behavior

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_pii_scan_and_findings.py](demo_01_pii_scan_and_findings.py) | Upload the synthetic PII note and inspect its findings in Firestore and the DLP UI. |
| 3 | [demo_02_guarded_candidate.py](demo_02_guarded_candidate.py) | Inspect Model Armor and compare plain, injected and PAN-bearing requests on a candidate. |
| 4 | [demo_03_audit_records.py](demo_03_audit_records.py) | Inspect immutable audit objects and the records used by the admin console. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

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

### demo_01_pii_scan_and_findings.py

Upload the synthetic PII note and inspect its findings in Firestore and the DLP UI.

**`step_01_example(session)` — The PII scan: one list, and a note that trips it / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (a small note with the kit's synthetic identifiers, uploaded to acme).

Expected shape, not a promised result:

```text
Copying file:///home/you/lesson83_vendor_note.md to gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md
  Completed files 1/1 | 303.0B/303.0B
>> gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md - waiting for the worker (up to 5 min)
>> indexed: acme_...	1	1
```

**`step_02_the_records(session)` — The findings: types and offsets, in Firestore and in the DLP tab / Do it: the records**

Do it: the records

Operation: bash — run in the operator shell, in the kit (acme's newest findings records; reads only).

Expected shape, not a promised result:

```text
acme/lesson83_vendor_note.md: 5 finding(s), INDIA_AADHAAR_INDIVIDUAL, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PERSON_NAME, PHONE_NUMBER
  acme/inv_2026_0412.md: 4 finding(s), EMAIL_ADDRESS, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PHONE_NUMBER
one finding, whole: {'info_type': 'PERSON_NAME', 'likelihood': 'LIKELY', 'offset': 159, 'chunk_id': 'acme:SHA#0'}
```

**`step_03_the_dlp_tab(session)` — The findings: types and offsets, in Firestore and in the DLP tab / Do it: the DLP tab**

The console sits behind IAP and admits only the addresses the lane was deployed with as ADMIN_EMAILS. If it answers 403 - Admins only, your address is not among them; the cell above has already read the records the tab draws.

Operation: bash — run in the operator shell, in the kit (the admin console's address).

Manual action: Open the deployed admin DLP tab and inspect the synthetic note's findings. Type done to compare them with the source fields printed next.

IDE adaptation: Pause before this cell for the page's manual step, a browser action or a wait (the README's Manual action). Type done to continue, or stop and rerun later. The cell then runs as the page gives it, unless another adaptation here says otherwise.

Expected shape, not a promised result:

```text
https://documind-admin-NUMBER.asia-south1.run.app   <- open in your browser, then the DLP tab
```

### demo_02_guarded_candidate.py

Inspect Model Armor and compare plain, injected and PAN-bearing requests on a candidate.

**`step_01_example(session)` — Model Armor: the template, the guard, and a candidate with ARMOR=on / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (a revision with ARMOR=on and no traffic).

Expected shape, not a promised result:

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=on|..."
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

**`step_02_four_questions_to_the_candidate_plain_two(session)` — Four questions to the candidate: plain, two injections, a PAN / Four questions to the candidate: plain, two injections, a PAN**

Each status beside the first characters of its body, then the candidate's tag removed. The cell asks acme four questions as you. The plain question must be answered. The English injection is a textbook attempt, and it must come back 400 prompt_blocked. The Hinglish one asks for the same thing the way people here actually type it, and it is the reason the template's floor is MEDIUM. The last question contains a synthetic PAN, and it tests the template's sensitive-data filter.

Operation: bash — run in the operator shell, in the kit (four questions to the candidate).

Expected shape, not a promised result:

```text
a plain question             200  {"answer":"A confirmed employee at grade E3 or above serve
  an injection, in English     400  {"detail":"prompt_blocked"}
  an injection, in Hinglish    400  {"detail":"prompt_blocked"}
  a synthetic PAN, asked       200  {"answer":"Invoice INV-2026-0412 carries that PAN [1].","c
```

**`step_03_clean_up_the_candidate_s_tag(session)` — Four questions to the candidate: plain, two injections, a PAN / Clean up: the candidate's tag**

Clean up: the candidate's tag

Operation: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed).

Expected shape, not a promised result:

```text
Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-000MM-xxx      (the live revision, as before; no candidate tag)
```

### demo_03_audit_records.py

Inspect immutable audit objects and the records used by the admin console.

**`step_01_example(session)` — The audit trail: the events in the retention bucket / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse).

Expected shape, not a promised result:

```text
YYYY/MM/DD/acme/doc.upload-UUID1.json
  YYYY/MM/DD/acme/dlp.finding-UUID2.json
  YYYY/MM/DD/acme/doc.upload-UUID3.json
    id: "UUID"
    ts: "YYYY-MM-DDTHH:MM:SS.ssssss+00:00"
    action: "dlp.finding"
    actor: {"tenant_id": "acme", "email": "system:ingest"}
    target: {"type": "document", "id": "acme_SHA", "tenant_id": "acme"}
    meta: {"types": ["INDIA_AADHAAR_INDIVIDUAL", "INDIA_GST_INDIVIDUAL", "INDIA_PAN_INDIVIDUAL", "PERSON_NAME", "PHONE_NUMBER"], "count": 5}
retention 157680000 s (5 years), locked False
delete refused: 403 Forbidden
```

**`step_02_example(session)` — The audit tab: what the admin console reads, and what it misses / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only).

Expected shape, not a promised result:

```text
{'tenant.create': 1} | doc.upload in it: 0
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_clean_up_withdraw_the_note(session)` — The audit tab: what the admin console reads, and what it misses / Clean up: withdraw the note**

The note came from you, and it should not stay in acme's corpus. make retire flags its chunks, which leave retrieval, and marks its ledger row WITHDRAWN; the object stays in the uploads bucket. Look at what stays. The findings record stays in dlp_findings until someone deletes it. The two audit events stay for five years, whatever anyone wants, which is what retention means. The withdrawal writes no audit event of its own: doc.delete is a registered action, and nothing in the kit emits it.

Operation: bash — run in the operator shell, in the kit (the note withdrawn from the index).

Expected shape, not a promised result:

```text
{"event": "reconcile_retired", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md", ...}
```

**`step_02_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html`. All 32 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `0f79843e15e5d20e67a5ce3f41943aca173c2e5d`.
