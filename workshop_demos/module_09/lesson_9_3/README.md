# Lesson 9.3: Measure latency, avoided calls and false cache hits

**Summary:** the threshold curve and the avoided calls in rupees. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html); Git blob `ab26cd1a53661cdbf477d3268f9e721275f57273`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (65 embeddings, about a minute; the report goes to your home folder) |
| s4 · window 12 | [demo_04_01_do_it_the_candidate.py](demo_04_01_do_it_the_candidate.py) | bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on at the kit's 0.95, and a start time) |
| s4 · window 14 | [demo_04_02_do_it_the_replay.py](demo_04_02_do_it_the_replay.py) | bash — run in the operator shell, in the kit (the 23 golden questions, then the 42 pairs, to the candidate; a few minutes) |
| s5 · window 18 | [demo_05_01_do_it_the_candidate_s_rows.py](demo_05_01_do_it_the_candidate_s_rows.py) | bash — run in the operator shell, in the kit (the candidate's rows since the start: hits, p95, rupees; reads only) |
| s5 · window 20 | [demo_05_02_do_it_the_kit_s_table.py](demo_05_02_do_it_the_kit_s_table.py) | bash — run in the operator shell, in the kit (the kit's own table of the last hour, by model and backend) |
| s6 · window 22 | [demo_06_01_choosing_the_threshold_and_the_clean_up.py](demo_06_01_choosing_the_threshold_and_the_clean_up.py) | bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed) |

## Conditional recovery

- [recover_04_01_do_it_the_replay.py](recover_04_01_do_it_the_replay.py) — bash — run in the operator shell, only if the replay listed questions with no answer (the API's last three tracebacks)

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

**HTML: The curve: every candidate threshold on the labelled pairs / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (65 embeddings, about a minute; the report goes to your home folder).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
42 pairs against 23 golden questions, text-embedding-005 @ us-central1

  threshold   hit rate (same)   false-hit rate (different)
       0.85      100% (24)          83% (15)
       0.88      100% (24)          67% (12)
       0.90       96% (23)          61% (11)
       0.92       62% (15)          50% ( 9)
       0.94       46% (11)          22% ( 4)
       0.95       33% ( 8)          11% ( 2)
       0.96       25% ( 6)           6% ( 1)
       0.97       17% ( 4)           0% ( 0)
       0.98        4% ( 1)           0% ( 0)

  lowest threshold with no false hit: 0.97
  nearest false pairs: pp-25 0.962, pp-31 0.955, pp-37 0.947, pp-35 0.941, pp-42 0.931, pp-41 0.929, pp-27 0.926, pp-30 0.926, pp-33 0.923, pp-40 0.914, pp-26 0.908, pp-36 0.885, pp-38 0.864, pp-39 0.858, pp-34 0.852, pp-29
  report: /home/you/cache93_curve.json
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_candidate.py

**HTML: The replay: the same pairs, asked live at 0.95 / Do it: the candidate**

Do it: the candidate

Run instruction: bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on at the kit's 0.95, and a start time).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=on|..."
...
>> candidate revision: documind-api-00046-wpk (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_replay.py

**HTML: The replay: the same pairs, asked live at 0.95 / Do it: the replay**

Do it: the replay

Run instruction: bash — run in the operator shell, in the kit (the 23 golden questions, then the 42 pairs, to the candidate; a few minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
pp-01 same right hit      211 ms  How much can I claim per trip for domestic travel?
  pp-15 same right hit      188 ms  Gratuity is paid at what rate per completed year?
  pp-16 same right hit      221 ms  What is the minimum bonus payable under the Bonus Ac
  pp-17 same right hit      209 ms  Under the Code on Wages, what is the rate for overti
  pp-18 same right hit      208 ms  Under the Code on Wages, what is the deadline for pa
  pp-19 same right hit      217 ms  The standing orders chapter of the IR Code applies f
  pp-20 same right hit      194 ms  Under the OSH Code, how many days of work earn a day
  pp-21 same right hit      153 ms  Under the DPDP Act, what is a Consent Manager?
  pp-25 diff FALSE HIT      230 ms  What is the notice period for a confirmed E2?
  pp-31 diff FALSE HIT      236 ms  Who approves a purchase of Rs 30,000?
  same-fact pairs served from the cache: 8 of 24
  different pairs served from the cache: 2 of 18
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_04_01_do_it_the_replay.py

**HTML: The replay: the same pairs, asked live at 0.95 / Do it: the replay**

Each question gets a second try, two seconds after a 5xx or a timeout, as the kit's own run_eval.py gives it: one retry separates a blip from an outage. A blip, such as the first request to a fresh revision failing once, shows as a line saying how many questions were answered on a second try. A question that fails twice is listed with its HTTP status, and the replay carries on without it. The status is all the client sees. The reason is in the API's own log, and this reads the last three tracebacks, with the revision that threw each one:

Run instruction: bash — run in the operator shell, only if the replay listed questions with no answer (the API's last three tracebacks).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_the_candidate_s_rows.py

**HTML: Avoided calls in rupees, and the latency of a hit / Do it: the candidate's rows**

Do it: the candidate's rows

Run instruction: bash — run in the operator shell, in the kit (the candidate's rows since the start: hits, p95, rupees; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
65 answers on the candidate: 10 from the answer cache, 55 from the model
  p95 latency: 236 ms for a hit, 3187 ms for a model answer
  a model answer cost Rs 0.4673 on average: the hits avoided 10 calls, about Rs 4.67
  of those hits, 2 served a wrong answer: pp-25, pp-31
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_the_kit_s_table.py

**HTML: Avoided calls in rupees, and the latency of a hit / Do it: the kit's table**

Do it: the kit's table

Run instruction: bash — run in the operator shell, in the kit (the kit's own table of the last hour, by model and backend).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
by model and backend (what answered, through which door)
model                 model_backend          answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------------------------------
gemini-3.6-flash      vertex                      55     97661    20783    0.3024     25.70    3187   0.00
gemini-3.6-flash      cache                       10         0        0    0.0000      0.00     236   0.00
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_choosing_the_threshold_and_the_clean_up.py

**HTML: Choosing the threshold, and the clean-up / Choosing the threshold, and the clean-up**

What the numbers allow, where the threshold lives, and the candidate put away. The kit's rule is the lowest candidate with no false hit on the set, and your curve names it. Before moving the switch, weigh three things. First, the rule of three: 18 different pairs with no false hit still allow a true rate of about 17%. The honest next step is more different pairs, written from real questions one word away, not a lower threshold. Second, the saving at that threshold: if it hits only a few same-fact pairs, the exact rung (the same words, no threshold at all) may be most of what the cache is worth. Third, the replay's hit from lines, which the curve cannot see. The threshold is an environment variable, SEMANTIC_CACHE_THRESHOLD, read once when a revision starts. No make target passes it, so trying 0.97 on a candidate takes gcloud run services update documind-api --no-traffic --tag candidate --update-env-vars SEMANTIC_CACHE_THRESHOLD=0.97, with your region and project, and then the replay again.

Run instruction: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed).

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

## Source coverage

23 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 13 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
