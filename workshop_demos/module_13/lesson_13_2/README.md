# Lesson 13.2: Reconcile usage events, reports and alerts

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_usage_events_and_features.py](demo_01_usage_events_and_features.py) | Inspect emitted usage events and the feature/report inputs built from them. |
| 3 | [demo_02_reports_and_alert_policy.py](demo_02_reports_and_alert_policy.py) | Reconcile reported values and inspect the current paging policy. |
| 4 | [demo_03_alert_plan_and_drill.py](demo_03_alert_plan_and_drill.py) | Plan/apply the reviewed alert configuration, exercise the drill and inspect its message. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

A deployed usage/audit lane and the intended alert notification channel; inspect the alert plan before apply.

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

### demo_01_usage_events_and_features.py

Inspect emitted usage events and the feature/report inputs built from them.

**`step_01_example(session)` — The readers, as the kit writes them down / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the readers as the kit writes them down; no network).

Expected shape, not a promised result:

```text
reader                         services                     events                window
the sink, into BigQuery        documind-api, documind-chat  query, stream, chat   every row, as it is written
tenant_daily, the view         what the sink copied         query, stream, media  one row per India day and 7 dimensions
make usage                     documind-api                 query, stream, media  the last N hours (default 24), at most 2000 rows
documind/queries, for alerts   documind-api                 query, stream         counted as written
rupees: tenant_daily's cost_inr is cost_usd x 85; make usage's USD_INR is 85
  chat    read by: the sink, into BigQuery
  media   read by: tenant_daily, the view, make usage
  query   read by: the sink, into BigQuery, tenant_daily, the view, make usage, documind/queries, for alerts
  stream  read by: the sink, into BigQuery, tenant_daily, the view, make usage, documind/queries, for alerts
alert policies in terraform/alerts.tf: 7 - api_latency, unanswerable_rate, gpu_left_warm, ingest_failed, reconcile_drift, reconcile_failed, dlq_depth
the one that reads the dead-letter queue: dlq_depth
```

**`step_02_example(session)` — Four questions, four rows / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (four questions, then make usage).

Expected shape, not a promised result:

```text
acme  answered   839 in  46 out  cost_usd None  What is the per-trip cap on domestic travel reimbursement?
  acme  answered   399 in  44 out  cost_usd None  What is the notice period for a confirmed E3?
  acme  refused    915 in  39 out  cost_usd None  What is ACME's sabbatical policy?
  zeta  answered   843 in  46 out  cost_usd None  What is the per-trip cap on travel reimbursement?
python evals/usage_rows.py --project documind-ai-YOUR-ID --hours ${HOURS:-24}
4 answers from documind-api in the last 1 h; USD_INR=85

by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
acme                         3      2153      129    0.0042      0.36    2348   0.33
zeta                         1       843       46    0.0016      0.14    2506   0.00

by model and backend (what answered, through which door)
model                 model_backend          answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------------------------------
gemini-3.6-flash      vertex                       4      2996      175    0.0058      0.49    2506   0.25

by brain (8.7's question, from the row)
brain                  answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
ui                           4      2996      175    0.0058      0.49    2506   0.25

by surface
event                  answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
query                        4      2996      175    0.0058      0.49    2506   0.25

by retrieval backend (which store served the pool; 13 September 2026)
retrieval_backend      answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
vector                       3      2153      129    0.0042      0.36    2348   0.33
firestore                    1       843       46    0.0016      0.14    2506   0.00

where the time went (p95 per stage, by tenant)
tenant                 answers  p95 ms  retrieve  rerank  generate   pool
-------------------------------------------------------------------------
acme                         3    2348       248     151      1874   20.0
zeta                         1    2506       412     147      1851   20.0
```

### demo_02_reports_and_alert_policy.py

Reconcile reported values and inspect the current paging policy.

**`step_01_example(session)` — Reconcile the view with make usage / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (reads only: Cloud Logging and one small BigQuery query).

Expected shape, not a promised result:

```text
today since 00:00 IST: 4 usage rows in Cloud Logging, 2 tenant_daily rows
  group (the view GROUP BY)                    answers refused   tokens in          Rs
  acme query vertex v3 dense vector text           3/3     1/1   2153/2153   0.36/0.36  equal
  zeta query vertex v3 dense firestore text        1/1     0/0     843/843   0.14/0.14  equal
  (each pair is tenant_daily/make usage's grouping; p95 is left out: the view's APPROX_QUANTILES is not the tool's nearest rank)
acme: tenant_daily Rs 0.36, make usage's grouping Rs 0.36 - equal
zeta: tenant_daily Rs 0.14, make usage's grouping Rs 0.14 - equal
media rows today: 0
RECONCILED: every group equal in answers, refusals, tokens and rupees
```

**`step_02_what_pages_you_today(session)` — The alert the dead-letter queue never had / Do it: what pages you today**

Do it: what pages you today

Operation: bash — run in the operator shell, in the kit (reads only).

Expected shape, not a promised result:

```text
log-based metrics on the lane: documind/ingest_embedded, documind/ingest_events, documind/ingest_reused, documind/queries, documind/reconcile_drift, documind/unanswerable
alert policies on the lane: 5, and what each one reads
  API p95 latency > 3s                                 request_latencies on documind-api
  Ingest failed                                        ingest_events on any service
  Unanswerable rate > 20% for a tenant                 unanswerable on any service
  documind-slm left warm: instances > 0 for 2 hours    instance_count on documind-slm
  documind-vllm left warm: instances > 0 for 2 hours   instance_count on documind-vllm
reads the dead-letter queue (ingest-dlq-sub): NOTHING - an upload the worker refused twelve times pages nobody
```

### demo_03_alert_plan_and_drill.py

Plan/apply the reviewed alert configuration, exercise the drill and inspect its message.

**`step_01_plan_and_apply(session)` — The alert the dead-letter queue never had / Do it: plan and apply**

Do it: plan and apply

Operation: bash — run in the operator shell, in the checkout where make up ran (Terraform's state).

Expected shape, not a promised result:

```text
PASS: saved confirmed inputs to .../terraform/runbook-project.auto.tfvars.json
CI trust: OWNER/REPO (ID NUMBER) / refs/heads/main
...
Terraform will perform the following actions:

  # google_monitoring_alert_policy.dlq_depth will be created
  + resource "google_monitoring_alert_policy" "dlq_depth" {
      + combiner              = "OR"
      + display_name          = "Ingest dead-letter queue holds messages"
      + notification_channels = [
          + "projects/documind-ai-YOUR-ID/notificationChannels/NUMBER",
        ]
      ...
    }

Plan: 1 to add, 0 to change, 0 to destroy.
PASS: no deletes/replacements or existing CI trust changes. Reviewed plan: .../terraform/rag-20260924T060011Z-3f2a9c1d7e.tfplan
Review the displayed changes, then run this command with 'apply' instead of 'plan'.
PASS: selected plan, confirmed inputs, backend/workspace and state agree: .../terraform/rag-20260924T060011Z-3f2a9c1d7e.tfplan
PASS: selected plan, confirmed inputs, backend/workspace and state agree: .../terraform/rag-20260924T060011Z-3f2a9c1d7e.tfplan
google_monitoring_alert_policy.dlq_depth: Creating...
google_monitoring_alert_policy.dlq_depth: Creation complete after 1s [id=projects/documind-ai-YOUR-ID/alertPolicies/NUMBER]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

**`step_02_the_drill(session)` — The alert the dead-letter queue never had / Do it: the drill**

A drill proves the alert end to end without waiting an hour for a poison upload. The cell publishes one message straight to the dead-letter topic, labelled drill=13.2. After five minutes it reads the gauge the policy reads, a sample a minute, and the policy itself.

Operation: bash — run in the operator shell, in the kit (one drill message into the dead-letter queue, then the gauge).

Expected shape, not a promised result:

```text
messageIds:
- '17405836920431227'
ingest-dlq-sub, undelivered messages - the gauge the policy reads, a sample a minute:
  11:30 0  11:31 0  11:32 0  11:33 1  11:34 1  11:35 1  11:36 1  11:37 1
policy: Ingest dead-letter queue holds messages - above 0 for 60s, 1 notification channel(s)
above zero since 11:33 IST: the condition holds - Monitoring > Alerting shows the incident
```

**`step_03_drain_the_drill_message(session)` — The alert the dead-letter queue never had / Do it: drain the drill message**

The drill message must not stay in the queue, and a real message must not be thrown away with it. The cell pulls without acknowledging, acknowledges only the messages labelled drill=13.2, and leaves anything else for make dlq.

Operation: bash — run in the operator shell, in the kit (acknowledges the drill message only).

Expected shape, not a promised result:

```text
pulled 1; acknowledged 1 drill message(s); 0 other(s) left for make dlq
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_13.2_Usage_Reconcile_WIX.html`. All 23 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `22c11174ed320d7ad4355dfac348e510cefca82b`.
