# Lesson 4.1: Follow upload events, retries, dead-letter handling and the batch lane

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_trace_upload_delivery.py](demo_01_trace_upload_delivery.py) | Read upload notification, push identity and the previous upload's request/event records. |
| 3 | [demo_02_poison_retries.py](demo_02_poison_retries.py) | Start the poison drill and observe retries without mistaking a delayed dead letter for success. |
| 4 | [demo_03_batch_lane_and_dead_letters.py](demo_03_batch_lane_and_dead_letters.py) | Inspect/build the batch example, then inspect the drill's dead letter when it arrives. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

Lesson 3.4's upload evidence; batch-job availability determines whether a large PDF remains queued.

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

**`step_02_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. Whether the batch job is declared on your lane is a fact the worker carries in its environment as BATCH_JOB. Read it once; step 6 uses it.

Operation: bash — run in the operator shell, once per shell.

Expected shape, not a promised result:

```text
batch job declared: no (BATCH_JOB is empty)
```

### demo_01_trace_upload_delivery.py

Read upload notification, push identity and the previous upload's request/event records.

**`step_01_off_the_platform(session)` — The plumbing: read the notification, the topic and the subscription off your lane / Read it off the platform**

Read it off the platform

Operation: bash — run in the operator shell (all read-only).

Expected shape, not a promised result:

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

**`step_02_read_the_two_records_your_3_4_upload_left(session)` — The verdicts: the HTTP-code rule, and your last upload's request log / Read the two records your 3.4 upload left**

Every delivery writes a request log entry (Cloud Run's, with the status the worker answered and how long it took) and, from the worker, a JSON line with the verdict. The first read below lists the last few POSTs the subscription made to the worker; the second lists the worker's own verdicts for the same window. Your note from lesson 3.4 should be there twice: once as the duplicate the unchanged bytes produced, once as the indexed version.

Operation: bash — run in the operator shell (both read-only).

Expected shape, not a promised result:

```text
TIMESTAMP                 REQUEST_METHOD  STATUS  LATENCY
2026-09-22T12:06:41.118Z  POST            200     7.412s
2026-09-22T11:58:07.902Z  POST            200     0.611s
TIMESTAMP                 EVENT             DOC_KEY                 CHUNKS  LANE
2026-09-22T12:06:41.001Z  ingest_ok         acme_9c41d0e2b7f5...    3       push
2026-09-22T11:58:07.844Z  ingest_duplicate  acme_111510fcf0a6...
```

### demo_02_poison_retries.py

Start the poison drill and observe retries without mistaking a delayed dead letter for success.

**`step_01_start_the_drill_then_watch_the_first_retri(session)` — Poison: a message that can never succeed, and the retries you can watch / Do it: start the drill, then watch the first retries**

The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

Operation: bash — run in the operator shell, in $DEMO_ROOT (Rs 0).

IDE adaptation: Use a unique saved empty-object name and generation; inspect/acknowledge only its exact dead letter and delete only its owned object. Time-window retry logs alone cannot identify that object.

Expected shape, not a promised result:

```text
>> zero-byte object in: poison-1758542871.pdf
>> the worker refused it (400): 1 validation error for IngestMessage
size
  Input should be greater than or equal to 1 [type=greater_than_equal, input_value='0', input_type=str]
>> Pub/Sub retries a non-2xx with backoff (10 s to 600 s, twelve attempts: eventarc.tf), then ingest-dlq: make dlq about an hour after this line
```

**`step_02_start_the_drill_then_watch_the_first_retri(session)` — Poison: a message that can never succeed, and the retries you can watch / Do it: start the drill, then watch the first retries**

The first block uploads the empty PDF and waits for the worker's first refusal; it prints the validation error the worker logged. Leave a few minutes, then the second block lists every POST the subscription made and every refusal the worker logged since. Note the gaps between the timestamps.

Operation: bash — run in the operator shell, a few minutes later (read-only).

Manual action: The poison retries are asynchronous. Wait a few minutes after the drill, then type done to read its retry records. This does not prove a dead letter has arrived.

### demo_03_batch_lane_and_dead_letters.py

Inspect/build the batch example, then inspect the drill's dead letter when it arrives.

**`step_01_read_the_lane_rs_0(session)` — The batch lane: the 250-page decision, the queued claim, the job / Read the lane, Rs 0**

The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker.

Operation: bash — run in the operator shell, in $DEMO_ROOT (read-only).

Expected shape, not a promised result:

```text
0 queued document(s)
no batch job on this lane: a queued claim waits until make batch-job declares it (BATCH_JOB=true, a Terraform apply)
```

**`step_02_read_the_lane_rs_0(session)` — The batch lane: the 250-page decision, the queued claim, the job / Read the lane, Rs 0**

The queue is a Firestore query the kit prints for you. The job and its schedule exist only if BATCH_JOB was set when the lane was deployed; the box above the setup read it off the worker. The corpus has no PDF over 250 pages, so the drill makes one: the CGST Act (236 pages) and the IT Act (34) joined with pypdf on your machine, at no cost. Uploading it costs nothing either, and that is the point of the first half: the worker counts 270 pages, writes the queued claim, answers 200, and no page has been sent to Document AI. The second half is where the money goes. When the job is declared, the worker starts it at once and it parses all 270 pages: about Rs 34 on the OCR processor, about Rs 230 on the Layout Parser (at the list prices lesson 3.2 quoted and Rs 85 to the dollar), plus a few rupees of embeddings for roughly six hundred windows. When the job is not declared, the claim simply waits, and make queued shows it. Decide before you upload.

Operation: bash — run in the operator shell, in $DEMO_ROOT (the join is free; the upload starts the paid parse if the job is declared).

Expected shape, not a promised result:

```text
bundle pages: 270
>> queued: pages, consumer: 270	documind-ingest-batch started (run requested); the hourly schedule backstops it
1 queued document(s)
  acme_3ff3f2ac3237...  gs://documind-ai-YOUR-ID-uploads/acme/cgst_it_bundle.pdf  pages=270  generation=1758543112345678
```

**`step_03_when_it_has_landed(session)` — Dead letters: reading the queue, deciding, cleaning up / Read it, when it has landed**

The poison message from step 5 reaches the queue about an hour after its first refusal. Run the first line then; an empty listing earlier is the retries still running, not a fault. The second read decodes the message's own record, the same JSON the worker refused, to see the size of zero with your own eyes.

Operation: bash — run in the operator shell, about an hour after step 5 (both peek; nothing is acknowledged).

Manual action: Dead-letter delivery can take about an hour. Inspect the drill's dead letter only once it has landed. Stop here and rerun this demo later to resume without repeating the completed batch upload.

IDE adaptation: Use a unique saved empty-object name and generation; inspect/acknowledge only its exact dead letter and delete only its owned object. Time-window retry logs alone cannot identify that object.

Expected shape, not a promised result:

```text
MESSAGE_ID         OBJECT_ID                    EVENT_TIME                DELIVERY_ATTEMPT
12345678901234567  acme/poison-1758542871.pdf   2026-09-22T12:17:52.318Z  1
{'name': 'acme/poison-1758542871.pdf', 'size': '0', 'contentType': 'application/pdf', 'generation': '1758542872123456', 'timeCreated': '2026-09-22T12:17:52.101Z'}
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_decide_then_clean_up(session)` — Dead letters: reading the queue, deciding, cleaning up / Decide, then clean up**

This dead letter deserves the second choice: the object was never meant to be indexed. Acknowledge the message to remove it from the queue, and delete the empty object from the bucket, because an object with no ledger row is exactly what the nightly walk of lesson 4.4 looks for, and it would rewrite the object onto itself and send the same poison round again every night. Both commands change your lane; both act only on the drill's own artefacts.

Operation: bash — run in the operator shell (removes the dead letter and the empty object; nothing else).

IDE adaptation: Use a unique saved empty-object name and generation; inspect/acknowledge only its exact dead letter and delete only its owned object. Time-window retry logs alone cannot identify that object.

Expected shape, not a promised result:

```text
acme/poison-1758542871.pdf
Removing gs://documind-ai-YOUR-ID-uploads/acme/poison-1758542871.pdf...
```

**`step_02_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html). All 40 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `4e0b9d5eec2e3600a742e7ea82678d360613d541`.
