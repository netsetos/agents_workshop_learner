# Lesson 4.1: Follow upload events, retries, dead-letter handling and the batch lane

**Summary:** `ingest_poison`, then the message in the DLQ; a queued claim drained. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html); Git blob `4e0b9d5eec2e3600a742e7ea82678d360613d541`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once per shell |
| s3 · window 10 | [demo_03_01_read_it_off_the_platform.py](demo_03_01_read_it_off_the_platform.py) | bash — run in the operator shell (all read-only) |
| s4 · window 16 | [demo_04_01_read_the_two_records_your_3_4_upload_left.py](demo_04_01_read_the_two_records_your_3_4_upload_left.py) | bash — run in the operator shell (both read-only) |
| s5 · window 19 | [demo_05_01_do_it_start_the_drill_then_watch_the_first_retri.py](demo_05_01_do_it_start_the_drill_then_watch_the_first_retri.py) | bash — run in the operator shell, in $DEMO_ROOT (Rs 0) |
| s5 · window 21 | [demo_05_02_do_it_start_the_drill_then_watch_the_first_retri.py](demo_05_02_do_it_start_the_drill_then_watch_the_first_retri.py) | bash — run in the operator shell, a few minutes later (read-only) |
| s6 · window 27 | [demo_06_01_read_the_lane_rs_0.py](demo_06_01_read_the_lane_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (read-only) |
| s6 · window 30 | [demo_06_02_read_the_lane_rs_0.py](demo_06_02_read_the_lane_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (the join is free; the upload starts the paid parse if the job is declared) |
| s7 · window 34 | [demo_07_01_read_it_when_it_has_landed.py](demo_07_01_read_it_when_it_has_landed.py) | bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged) |
| s7 · window 36 | [demo_07_02_decide_then_clean_up.py](demo_07_02_decide_then_clean_up.py) | bash — run in the operator shell (removes the dead letter and the empty object; nothing else) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. Whether the batch job is declared on your lane is a fact the worker carries in its environment as BATCH_JOB. Read it once; step 6 uses it.

Run instruction: bash — run in the operator shell, once per shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
batch job declared: no (BATCH_JOB is empty)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_read_it_off_the_platform.py

**HTML: The plumbing: read the notification, the topic and the subscription off your lane / Read it off the platform**

Read it off the platform

Run instruction: bash — run in the operator shell (all read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
---
event_types:
- OBJECT_FINALIZE
id: '1'
payload_format: JSON_API_V1
topic: //pubsub.googleapis.com/projects/documind-ai-YOUR-ID/topics/documind-ingest
ackDeadlineSeconds: 600
deadLetterPolicy:
  deadLetterTopic: projects/documind-ai-YOUR-ID/topics/documind-ingest-dlq
  maxDeliveryAttempts: 12
pushConfig:
  oidcToken:
    serviceAccountEmail: documind-ingest-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
  pushEndpoint: https://documind-ingest-NUMBER.asia-south1.run.app
retryPolicy:
  maximumBackoff: 600s
  minimumBackoff: 10s
projects/documind-ai-YOUR-ID/topics/documind-ingest-dlq
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: '30'
        run.googleapis.com/execution-environment: gen2
    spec:
      containerConcurrency: 1
      timeoutSeconds: 600
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_read_the_two_records_your_3_4_upload_left.py

**HTML: The verdicts: the HTTP-code rule, and your last upload's request log / Read the two records your 3.4 upload left**

Every delivery writes a request log entry (Cloud Run's, with the status the worker answered and how long it took) and, from the worker, a JSON line with the verdict. The first read below lists the last few POSTs the subscription made to the worker; the second lists the worker's own verdicts for the same window. Your note from lesson 3.4 should be there twice: once as the duplicate the unchanged bytes produced, once as the indexed version.

Run instruction: bash — run in the operator shell (both read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
TIMESTAMP                 REQUEST_METHOD  STATUS  LATENCY
2026-09-22T12:06:41.118Z  POST            200     7.412s
2026-09-22T11:58:07.902Z  POST            200     0.611s
TIMESTAMP                 EVENT             DOC_KEY                 CHUNKS  LANE
2026-09-22T12:06:41.001Z  ingest_ok         acme_9c41d0e2b7f5...    3       push
2026-09-22T11:58:07.844Z  ingest_duplicate  acme_111510fcf0a6...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_start_the_drill_then_watch_the_first_retri.py

**HTML: Poison: a message that can never succeed, and the retries you can watch / Do it: start the drill, then watch the first retries**

The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> zero-byte object in: poison-1758542871.pdf
>> the worker refused it (400): 1 validation error for IngestMessage
size
  Input should be greater than or equal to 1 [type=greater_than_equal, input_value='0', input_type=str]
>> Pub/Sub retries a non-2xx with backoff (10 s to 600 s, twelve attempts: eventarc.tf), then ingest-dlq: make dlq about an hour after this line
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_start_the_drill_then_watch_the_first_retri.py

**HTML: Poison: a message that can never succeed, and the retries you can watch / Do it: start the drill, then watch the first retries**

The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

Run instruction: bash — run in the operator shell, a few minutes later (read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_read_the_lane_rs_0.py

**HTML: The batch lane: the 250-page decision, the queued claim, the job / Read the lane, Rs 0**

The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
0 queued document(s)
no batch job on this lane: a queued claim waits until make batch-job declares it (BATCH_JOB=true, a Terraform apply)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_read_the_lane_rs_0.py

**HTML: The batch lane: the 250-page decision, the queued claim, the job / Read the lane, Rs 0**

The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker. The corpus has no PDF over 250 pages, so the drill makes one: the CGST Act (236 pages) and the IT Act (34) joined with pypdf on your machine, at no cost. Uploading it costs nothing either, and that is the point of the first half: the worker counts 270 pages, writes the queued claim, answers 200, and no page has been sent to Document AI. The second half is where the money goes. When the job is declared, the worker starts it at once and it parses all 270 pages: about Rs 34 on the OCR processor, about Rs 230 on the Layout Parser (at the list prices lesson 3.2 quoted and Rs 85 to the dollar), plus a few rupees of embeddings for roughly six hundred windows. When the job is not declared, the claim simply waits, and make queued shows it. Decide before you upload.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the join is free; the upload starts the paid parse if the job is declared).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
bundle pages: 270
>> queued: pages, consumer: 270	documind-ingest-batch started (run requested); the hourly schedule backstops it
1 queued document(s)
  acme_3ff3f2ac3237...  gs://documind-ai-YOUR-ID-uploads/acme/cgst_it_bundle.pdf  pages=270  generation=1758543112345678
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_read_it_when_it_has_landed.py

**HTML: Dead letters: reading the queue, deciding, cleaning up / Read it, when it has landed**

The poison message from step 5 reaches the queue about an hour after its first refusal. Run the first line then; an empty listing earlier is the retries still running, not a fault. The second read decodes the message's own record, the same JSON the worker refused, to see the size of zero with your own eyes.

Run instruction: bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
MESSAGE_ID         OBJECT_ID                    EVENT_TIME                DELIVERY_ATTEMPT
12345678901234567  acme/poison-1758542871.pdf   2026-09-22T12:17:52.318Z  1
{'name': 'acme/poison-1758542871.pdf', 'size': '0', 'contentType': 'application/pdf', 'generation': '1758542872123456', 'timeCreated': '2026-09-22T12:17:52.101Z'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_decide_then_clean_up.py

**HTML: Dead letters: reading the queue, deciding, cleaning up / Decide, then clean up**

This dead letter deserves the second choice: the object was never meant to be indexed. Acknowledge the message to remove it from the queue, and delete the empty object from the bucket, because an object with no ledger row is exactly what the nightly walk of lesson 4.4 looks for, and it would rewrite the object onto itself and send the same poison round again every night. Both commands change your lane; both act only on the drill's own artefacts.

Run instruction: bash — run in the operator shell (removes the dead letter and the empty object; nothing else).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme/poison-1758542871.pdf
Removing gs://documind-ai-YOUR-ID-uploads/acme/poison-1758542871.pdf...
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
