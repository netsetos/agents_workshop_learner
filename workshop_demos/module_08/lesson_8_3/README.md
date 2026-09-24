# Lesson 8.3: Exercise DLP, guardrails and audit behavior

**Summary:** the PAN in the DLP tab; `prompt_blocked`; the upload in the audit tab. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.3-dlp-guard-audit/Netsetos_GCP_Capstone_8.3_DLP_Guard_Audit_WIX.html); Git blob `0f79843e15e5d20e67a5ce3f41943aca173c2e5d`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (a small note with the kit's synthetic identifiers, uploaded to acme) |
| s4 · window 10 | [demo_04_01_do_it_the_records.py](demo_04_01_do_it_the_records.py) | bash — run in the operator shell, in the kit (acme's newest findings records; reads only) |
| s4 · window 12 | [demo_04_02_do_it_the_dlp_tab.py](demo_04_02_do_it_the_dlp_tab.py) | bash — run in the operator shell, in the kit (the admin console's address) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (a revision with ARMOR=on and no traffic) |
| s6 · window 19 | [demo_06_01_four_questions_to_the_candidate_plain_two_inject.py](demo_06_01_four_questions_to_the_candidate_plain_two_inject.py) | bash — run in the operator shell, in the kit (four questions to the candidate) |
| s6 · window 21 | [demo_06_02_clean_up_the_candidate_s_tag.py](demo_06_02_clean_up_the_candidate_s_tag.py) | bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed) |
| s7 · window 25 | [demo_07_01_do_it.py](demo_07_01_do_it.py) | bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse) |
| s8 · window 29 | [demo_08_01_do_it.py](demo_08_01_do_it.py) | bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only) |
| s8 · window 31 | [demo_08_02_clean_up_withdraw_the_note.py](demo_08_02_clean_up_withdraw_the_note.py) | bash — run in the operator shell, in the kit (the note withdrawn from the index) |

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

**HTML: The PII scan: one list, and a note that trips it / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a small note with the kit's synthetic identifiers, uploaded to acme).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Copying file:///home/you/lesson83_vendor_note.md to gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md
  Completed files 1/1 | 303.0B/303.0B
>> gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md - waiting for the worker (up to 5 min)
>> indexed: acme_...	1	1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_records.py

**HTML: The findings: types and offsets, in Firestore and in the DLP tab / Do it: the records**

Do it: the records

Run instruction: bash — run in the operator shell, in the kit (acme's newest findings records; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme/lesson83_vendor_note.md: 5 finding(s), INDIA_AADHAAR_INDIVIDUAL, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PERSON_NAME, PHONE_NUMBER
  acme/inv_2026_0412.md: 4 finding(s), EMAIL_ADDRESS, INDIA_GST_INDIVIDUAL, INDIA_PAN_INDIVIDUAL, PHONE_NUMBER
one finding, whole: {'info_type': 'PERSON_NAME', 'likelihood': 'LIKELY', 'offset': 159, 'chunk_id': 'acme:SHA#0'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_dlp_tab.py

**HTML: The findings: types and offsets, in Firestore and in the DLP tab / Do it: the DLP tab**

The console sits behind IAP and admits only the addresses the lane was deployed with as ADMIN_EMAILS. If it answers 403 - Admins only, your address is not among them; the cell above has already read the records the tab draws.

Run instruction: bash — run in the operator shell, in the kit (the admin console's address).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
https://documind-admin-NUMBER.asia-south1.run.app   <- open in your browser, then the DLP tab
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Model Armor: the template, the guard, and a candidate with ARMOR=on / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a revision with ARMOR=on and no traffic).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=on|..."
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_four_questions_to_the_candidate_plain_two_inject.py

**HTML: Four questions to the candidate: plain, two injections, a PAN / Four questions to the candidate: plain, two injections, a PAN**

Each status beside the first characters of its body, then the candidate's tag removed. The cell asks acme four questions as you. The plain question must be answered. The English injection is a textbook attempt, and it must come back 400 prompt_blocked. The Hinglish one asks for the same thing the way people here actually type it, and it is the reason the template's floor is MEDIUM. The last question contains a synthetic PAN, and it tests the template's sensitive-data filter.

Run instruction: bash — run in the operator shell, in the kit (four questions to the candidate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
a plain question             200  {"answer":"A confirmed employee at grade E3 or above serve
  an injection, in English     400  {"detail":"prompt_blocked"}
  an injection, in Hinglish    400  {"detail":"prompt_blocked"}
  a synthetic PAN, asked       200  {"answer":"Invoice INV-2026-0412 carries that PAN [1].","c
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_clean_up_the_candidate_s_tag.py

**HTML: Four questions to the candidate: plain, two injections, a PAN / Clean up: the candidate's tag**

Clean up: the candidate's tag

Run instruction: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-000MM-xxx      (the live revision, as before; no candidate tag)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it.py

**HTML: The audit trail: the events in the retention bucket / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_do_it.py

**HTML: The audit tab: what the admin console reads, and what it misses / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{'tenant.create': 1} | doc.upload in it: 0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_02_clean_up_withdraw_the_note.py

**HTML: The audit tab: what the admin console reads, and what it misses / Clean up: withdraw the note**

The note came from you, and it should not stay in acme's corpus. make retire flags its chunks, which leave retrieval, and marks its ledger row WITHDRAWN; the object stays in the uploads bucket. Look at what stays. The findings record stays in dlp_findings until someone deletes it. The two audit events stay for five years, whatever anyone wants, which is what retention means. The withdrawal writes no audit event of its own: doc.delete is a registered action, and nothing in the kit emits it.

Run instruction: bash — run in the operator shell, in the kit (the note withdrawn from the index).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_retired", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/lesson83_vendor_note.md", ...}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

32 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 20 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
