# Lesson 6.2: Generate structured answers, citations and refusals

**Summary:** resolved citations; a refusal on an unanswerable question. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html); Git blob `c8fdaf018887ed16c078e2078289794f62ff081b`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, in $DEMO_ROOT, once per shell |
| s3 · window 12 | [demo_03_01_do_it_six_drafts_one_resolution_two_refusals.py](demo_03_01_do_it_six_drafts_one_resolution_two_refusals.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine) |
| s4 · window 16 | [demo_04_01_do_it_one_question_two_halves_three_rows.py](demo_04_01_do_it_one_question_two_halves_three_rows.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question and three Firestore reads, a rupee) |
| s5 · window 21 | [demo_05_01_do_it_three_questions_three_envelopes_three_rows.py](demo_05_01_do_it_three_questions_three_envelopes_three_rows.py) | bash — run in the operator shell (three questions, two of them model calls: a rupee; one log read) |
| s6 · window 26 | [demo_06_01_do_it_the_same_call_from_the_shell.py](demo_06_01_do_it_the_same_call_from_the_shell.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one model call at the generator's rate, a few paise) |
| s7 · window 32 | [demo_07_01_read_the_lane_rs_0.py](demo_07_01_read_the_lane_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (three reads) |
| s8 · window 36 | [demo_08_01_the_code.py](demo_08_01_the_code.py) | bash — run in the operator shell (one new revision, no traffic; one question that fails on purpose; one log read; the undo) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The model, its location, the tuned base, the router, the backend, the prompt version and the answer's reserve live in the API's environment, each with a default the page names; a name the service does not set is unset rather than exported empty, because steps 3 and 6 import the kit. /version says what is actually serving.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
model: gemini-3.6-flash (default)  location: from the model: global for a name  base: none, no tuned endpoint
routing: off (default)  backend: vertex (default)  prompt: v3 (default)  answer: 2,048 (default)
version: gemini-3.6-flash | documind-rag@v3 | vertex
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_six_drafts_one_resolution_two_refusals.py

**HTML: The contract offline: drafts that pass, drafts that fail, and the resolver on the kit's chunks / Do it: six drafts, one resolution, two refusals**

Do it: six drafts, one resolution, two refusals

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
resolved: 2 of 3 citations kept: source 7 was out of range and dropped, not raised
   acme:hr_policy_2026#NP-03      page 1 score 0.0 kind text quote 'NP-03 — Notice period A confirmed employee a'
   acme:hr_policy_2026#PB-02      page 1 score 0.0 kind text quote 'PB-02 — Probation New joiners serve six mont'
RAGAnswer: {"answer": "A confirmed employee in grade E3 serves the notice period in NP-03 [1]; probation is different [2].", "citations": [{" ...
refused (source 0, [Source N] is 1-based): citations.0.source: Input should be greater than or equal to 1
refused (confidence outside high|medium|low): confidence: Input should be 'high', 'medium' or 'low'
refused (a quote over the draft's limit): citations.0.quote: String should have at most 200 characters
the model's refusal, resolved: {'answer': 'The context does not contain the answer.', 'citations': [], 'confidence': 'low', 'answerable': False}
the empty pool's, written by the API without a model: The corpus holds nothing near this question: no passage of this tenant's current documents was r ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_one_question_two_halves_three_rows.py

**HTML: One answer from the lane, field by field, with every quote checked against its row / Do it: one question, two halves, three rows**

Do it: one question, two halves, three rows

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question and three Firestore reads, a rupee).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the contract: {"answer": "A confirmed employee in grade E3 must serve a notice period of ... [1]...", "citations": "3 citations", "confidence": "high", "answerable": true}
the envelope: {'model': 'gemini-3.6-flash', 'backend': 'vertex', 'tokens_in': 1xxx, 'tokens_out': 4xx, 'cached_tokens': 0, 'cost_usd': 0.00xxxx, 'latency_ms': 2xxx, 'cache_hit': 'none'}
[N] marks in the answer: ['1', '2', '3'] | citations returned: 3
   [1] #  1 hr_policy_2026.md        page None score 0.9xxx kind text | row found True | quote in the row True | 1x words
   [2] #  4 hr_policy_2026.md        page None score 0.8xxx kind text | row found True | quote in the row True | 1x words
   [3] #  2 hr_policy_2026.md        page None score 0.6xxx kind text | row found True | quote in the row True | 1x words
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_three_questions_three_envelopes_three_rows.py

**HTML: Three refusals: the model's twice, the API's once, and how their envelopes differ / Do it: three questions, three envelopes, three rows**

Do it: three questions, three envelopes, three rows

Run instruction: bash — run in the operator shell (three questions, two of them model calls: a rupee; one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
answerable False | confidence low | citations 0 | backend vertex | tokens 1xxx + 1xx | cost_usd 0.00xxxx | pool 20 | The provided context does not contain information about Globex's not
answerable False | confidence low | citations 0 | backend vertex | tokens 1xxx + 1xx | cost_usd 0.00xxxx | pool 20 | The context covers FY2025 and FY2026; it does not state the revenue f
answerable False | confidence low | citations 0 | backend none | tokens 0 + 0 | cost_usd 0.0 | pool 0 | The corpus holds nothing near this question: no passage of this tena
acme	False	none	0	0.0
acme	False	vertex	1xxx	0.00xxxx
globex	False	vertex	1xxx	0.00xxxx
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_same_call_from_the_shell.py

**HTML: The model call by hand: the schema, the thinking, the usage, the price / Do it: the same call, from the shell**

Do it: the same call, from the shell

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one model call at the generator's rate, a few paise).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
finish: STOP | the draft: {"answer": "A confirmed employee in grade E3 ... [1]", "citations": [{"source": 1, "quote": "..."}], "confidence": "high", "answerable": true} ...
resolved: [('acme:hr_policy_2026#NP-03', 1, 0.0)] | answerable True | confidence high
usage: prompt 4xx | candidates 1xx | thoughts xxx | cached 0
priced as the API would: $0.00xxxx = Rs 0.xxxx at 85.0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_read_the_lane_rs_0.py

**HTML: The model as a setting: the global client, a tuned endpoint, a pin and a router / Read the lane, Rs 0**

Read the lane, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (three reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=vector
acme's tenant_settings: {'generator_model': None, 'model_backend': None, 'retrieval_backend': 'vector', 'data_region': 'any'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_the_code.py

**HTML: What an answer costs, and the failure that is not a refusal / The code**

The code

Run instruction: bash — run in the operator shell (one new revision, no traffic; one question that fails on purpose; one log read; the undo).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
HTTP 502
{"detail":"generation produced no parseable answer (MAX_TOKENS)"}
2026-09-2xT1x:xx:xx.xxxxxxZ	generation_unparsed			MAX_TOKENS
2026-09-2xT1x:xx:xx.xxxxxxZ	generation_truncated	16	1x
template now:
(empty means unset: the default, 2048)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

37 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 27 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
