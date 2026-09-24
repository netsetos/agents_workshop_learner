# Lesson 13.3: Exercise model routing, budgets and shutdown controls

**Summary:** the tier changes at 85 percent; zero instances after `make off`. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html); Git blob `98282e525bfaa2998c591ba8f3312851781f0218`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the controls as the kit writes them down; no network) |
| s4 · window 11 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (reads only) |
| s5 · window 13 | [demo_05_01_do_it_routing_on_the_month_as_it_is.py](demo_05_01_do_it_routing_on_the_month_as_it_is.py) | bash — run in the operator shell, in the kit (a candidate revision, no traffic, ROUTING on; three questions) |
| s5 · window 15 | [demo_05_02_do_it_the_same_three_at_85_percent.py](demo_05_02_do_it_the_same_three_at_85_percent.py) | bash — run in the operator shell, in the kit (the same candidate at 85 percent; the same three questions) |
| s5 · window 17 | [demo_05_03_do_it_undo_the_candidate.py](demo_05_03_do_it_undo_the_candidate.py) | bash — run in the operator shell, in the kit (the variables off the template, the tag dropped) |
| s6 · window 20 | [demo_06_01_do_it_the_floor_then_the_switch.py](demo_06_01_do_it_the_floor_then_the_switch.py) | bash — run in the operator shell, in the kit (a floor, then the switch, then the nightly job's entry) |
| s6 · window 22 | [demo_06_02_do_it_the_instances_after_fifteen_minutes.py](demo_06_02_do_it_the_instances_after_fifteen_minutes.py) | bash — run in the operator shell, in the kit (after 15 minutes; reads only) |
| s6 · window 24 | [demo_06_03_do_it_the_ceiling.py](demo_06_03_do_it_the_ceiling.py) | bash — run in the operator shell, in the kit (lowers one quota; make gpu-cap-off takes it back) |

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

**HTML: The controls, as the kit writes them down / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the controls as the kit writes them down; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
per answer: ROUTING=off on the lane (lesson-12.2.sh). With it on, gemini-3.1-flash-lite labels each question SIMPLE, MEDIUM, COMPLEX, and breakers.choose_model() picks the model:
  spend   SIMPLE                  MEDIUM                  COMPLEX
  0%      gemini-3.1-flash-lite   gemini-3.6-flash        gemini-3.1-pro-preview
  79.9%   gemini-3.1-flash-lite   gemini-3.6-flash        gemini-3.1-pro-preview
  80%     gemini-3.1-flash-lite   gemini-3.1-flash-lite   gemini-3.6-flash
  85%     gemini-3.1-flash-lite   gemini-3.1-flash-lite   gemini-3.6-flash
  100%    gemini-3.1-flash-lite   gemini-3.1-flash-lite   gemini-3.6-flash
  120%    gemini-3.1-flash-lite   gemini-3.1-flash-lite   gemini-3.6-flash
  the spend: Firestore budget/<month, UTC>, USD added by every answer, over BUDGET_USD (100 on the lane); SPEND_PCT replaces it
  BUDGET_FLOOR_PCT = 100 (the comment's min-instances 0): read by nothing
per month: DocuMind monthly budget, BUDGET_AMOUNT 5000 in the billing account's currency; it emails at 50%, 80%, 100% and at a 120% forecast
per hour: documind-off runs 0 23 * * * Asia/Kolkata and floors documind-slm, documind-vllm, documind-gateway, documind-ui to min-instances 0; make off does the same by hand
  make gpu-cap: the GPU quota in us-central1 capped at 1; alerts.tf's gpu_left_warm pages when one stays up two hours
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The month so far / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-api: ROUTING=off, BUDGET_USD=100, SPEND_PCT=unset
the counter, budget/2026-09: USD 7.8412 of 100 = 7.84% - the breaker would read 'normal'
the billing budget: 5000 INR a month on the whole project; emails at 50%, 80%, 100%, 120% forecast
python services/slm/gpu_quota.py --project documind-ai-YOUR-ID --region us-central1

Total NVIDIA L4 GPU allocation without zonal redundancy
  run.googleapis.com/nvidia_l4_gpu_allocation_no_zonal_redundancy
  1/{project}/{region}         us-central1  effective 3 (default 3)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_routing_on_the_month_as_it_is.py

**HTML: The tier at 85 percent / Do it: routing on, the month as it is**

Do it: routing on, the month as it is

Run instruction: bash — run in the operator shell, in the kit (a candidate revision, no traffic, ROUTING on; three questions).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gemini-3.1-flash-lite    What is the notice period for a confirmed E3?
                           A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  gemini-3.6-flash         Explain what happens when a trip costs more than the per-trip travel cap.
                           Travel is capped at Rs 40,000 per trip [1]; a trip above the cap needs the function head's written approval before travel [1].
  gemini-3.1-pro-preview   Work out, step by step, the total reimbursed for three domestic trips costing Rs 38,000, Rs 45,000 and Rs 22,000.
                           Each trip is reimbursed up to the cap of Rs 40,000 [1]: Rs 38,000 + Rs 40,000 + Rs 22,000 = Rs 1,00,000; the Rs 5,000 above the cap ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_the_same_three_at_85_percent.py

**HTML: The tier at 85 percent / Do it: the same three at 85 percent**

Do it: the same three at 85 percent

Run instruction: bash — run in the operator shell, in the kit (the same candidate at 85 percent; the same three questions).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gemini-3.1-flash-lite    What is the notice period for a confirmed E3?
                           A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  gemini-3.1-flash-lite    Explain what happens when a trip costs more than the per-trip travel cap.
                           Travel is capped at Rs 40,000 per trip [1]; a trip above the cap needs the function head's written approval before travel [1].
  gemini-3.6-flash         Work out, step by step, the total reimbursed for three domestic trips costing Rs 38,000, Rs 45,000 and Rs 22,000.
                           Each trip is reimbursed up to the cap of Rs 40,000 [1]: Rs 38,000 + Rs 40,000 + Rs 22,000 = Rs 1,00,000; the Rs 5,000 above the cap ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_03_do_it_undo_the_candidate.py

**HTML: The tier at 85 percent / Do it: undo the candidate**

Do it: undo the candidate

Run instruction: bash — run in the operator shell, in the kit (the variables off the template, the tag dropped).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
100	documind-api-00031-kez
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_floor_then_the_switch.py

**HTML: Off at night, and the ceiling under it / Do it: the floor, then the switch**

Do it: the floor, then the switch

Run instruction: bash — run in the operator shell, in the kit (a floor, then the switch, then the nightly job's entry).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-slm --region us-central1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
ERROR: (gcloud.run.services.update) Service [documind-slm] could not be found.
make[1]: [Makefile:659: slm-off] Error 1 (ignored)
...
gcloud run services update documind-ui --region asia-south1 --project documind-ai-YOUR-ID --min-instances 0 --quiet
Deploying...
...
Done.
...
documind-slm: min-instances absent
documind-vllm: min-instances absent
documind-gateway: min-instances absent
documind-ui: min-instances 0
0 23 * * *	Asia/Kolkata	ENABLED	2026-09-23T17:30:03.184Z
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_the_instances_after_fifteen_minutes.py

**HTML: Off at night, and the ceiling under it / Do it: the instances, after fifteen minutes**

A floor of zero lets the service scale to zero, but an idle instance can stay up for up to fifteen minutes after its last request. The cell waits, then reads the UI's instance count from Cloud Monitoring for the last half hour, a sample a minute.

Run instruction: bash — run in the operator shell, in the kit (after 15 minutes; reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-ui, container instances (active and idle), a sample a minute, last 30 minutes:
  11:52 1  11:53 1  11:54 1  11:55 1  11:56 1  11:57 1  11:58 1  11:59 1  12:00 1  12:01 1
  12:02 1  12:03 1  12:04 1  12:05 1  12:06 1  12:07 1  12:08 1  12:09 0  12:10 0  12:11 0
  12:12 0  12:13 0  12:14 0  12:15 0  12:16 0  12:17 0  12:18 0  12:19 0  12:20 0  12:21 0
zero instances since 12:09 IST
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_do_it_the_ceiling.py

**HTML: Off at night, and the ceiling under it / Do it: the ceiling**

make gpu-cap writes a consumer quota override on the L4 quotas in us-central1, capping them at one card. --max-instances belongs to one service. The quota belongs to the project, so a second GPU service, a GPU candidate or a typo cannot allocate a second card. Lowering a quota needs no approval; raising it again does.

Run instruction: bash — run in the operator shell, in the kit (lowers one quota; make gpu-cap-off takes it back).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python services/slm/gpu_quota.py --project documind-ai-YOUR-ID --region us-central1 --cap 1

Total NVIDIA L4 GPU allocation without zonal redundancy
  run.googleapis.com/nvidia_l4_gpu_allocation_no_zonal_redundancy
  1/{project}/{region}         us-central1  effective 3 (default 3)
                               -> capped at 1

1 override(s) written. Read back:
  Total NVIDIA L4 GPU allocation without zonal red 1/{project}/{region}       effective 1 (default 3, override 1)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

25 code windows mapped: 10 IDE demo files, 1 shared setup blocks, 14 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
