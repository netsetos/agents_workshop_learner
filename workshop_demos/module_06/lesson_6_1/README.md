# Lesson 6.1: Pack evidence within the context budget

**Summary:** the packed set for one question and its tokens. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html); Git blob `fd0703c559853dc14669ad353f31423ca6ccef55`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, in $DEMO_ROOT, once per shell |
| s3 · window 14 | [demo_03_01_do_it_the_lines_then_two_pools_twice_then_a_coun.py](demo_03_01_do_it_the_lines_then_two_pools_twice_then_a_coun.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine) |
| s4 · window 17 | [demo_04_01_do_it_three_texts_two_counters_one_pool_twice.py](demo_04_01_do_it_three_texts_two_counters_one_pool_twice.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; a handful of count_tokens calls) |
| s5 · window 21 | [demo_05_01_do_it_one_question_its_tokens_its_price_and_the.py](demo_05_01_do_it_one_question_its_tokens_its_price_and_the.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question, a rupee) |
| s6 · window 27 | [demo_06_01_do_it_the_dated_revision_in_the_stream_read_revi.py](demo_06_01_do_it_the_dated_revision_in_the_stream_read_revi.py) | bash — run in the operator shell, in $DEMO_ROOT (one upload, one streamed question, one upload; paise) |
| s7 · window 32 | [demo_07_01_do_it_the_day_s_tokens_and_the_retries_there_wer.py](demo_07_01_do_it_the_day_s_tokens_and_the_retries_there_wer.py) | bash — run in the operator shell, in $DEMO_ROOT (Rs 0: two log reads) |
| s8 · window 34 | [demo_08_01_the_knob_a_budget_too_small_on_a_candidate_that.py](demo_08_01_the_knob_a_budget_too_small_on_a_candidate_that.py) | bash — run in the operator shell (one new revision, no traffic; one question; one log read; then the undo) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The budget's total, the answer's reserve, the model and the rupee rate live in the API's environment, each with a default the page names; a name the service does not set is unset rather than exported empty, because steps 4 and 5 import the kit and its settings class reads an empty variable as a value.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
context: 8000 (default)  answer: 2048 (default)  model: gemini-3.6-flash (default)  prompt: v3 (default)  usd_inr: 85 (default)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_the_lines_then_two_pools_twice_then_a_coun.py

**HTML: The budget's lines and the packer, offline on the kit's own documents / Do it: the lines, then two pools twice, then a counter**

Do it: the lines, then two pools twice, then a counter

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
4.5's teaching split: system 1500 | tenant_pack 40000 | chunks 6000 | history 2000 | answer 2000 | input_total 49500
the API's, this question: system 168 (the fixed prompt, 672 characters) | chunks 7832 | tenant_pack 0 | history 0 | answer 2048 | input_total 8000

handbook sections, top_k 5: packed 5, dropped 0, context 301 tokens | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] hr_policy_2026.md, p.1  (32 tokens)

handbook sections, top_k 20: packed 20, dropped 0, context 2009 tokens | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] hr_policy_2026.md, p.1  (32 tokens)

full Act pages, top_k 5: packed 5, dropped 0, context 1667 tokens | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] cgst_act_2017.md, p.116  (508 tokens)

full Act pages, top_k 20: packed 17, dropped 3, context 7774 tokens | log: context_budget_drop packed=17 dropped=3 | the dated rule is added
   [Source 1] hr_policy_2026.md, p.1, NP-03 — Notice period  (72 tokens)
   [Source 2] smoke_note.md, p.1, effective from 2026-10-01  (66 tokens)
   [Source 3] cgst_act_2017.md, p.116  (508 tokens)

full Act pages, top_k 20, with a counter injected that reads 60 percent more: packed 11, dropped 9, trimmed from the tail after the estimate had packed them
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_three_texts_two_counters_one_pool_twice.py

**HTML: The model's counter beside the estimate: English, Hindi, and a pool trimmed by the exact count / Do it: three texts, two counters, one pool twice**

Do it: three texts, two counters, one pool twice

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; a handful of count_tokens calls).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
NP-03, English     chars   234  estimate  58  counted  1xx  ratio x.xx  (near one)
a clause in Hindi  chars    72  estimate   18  counted   xx  ratio x.xx  (well above one)
one Act page       chars  2000  estimate  500  counted  4xx  ratio x.xx  (near one)
twenty Act pages under the estimate     : packed 15, dropped 5, context 7633 tokens by that counter
twenty Act pages under the model's count: packed 1x, dropped x, context 7xxx tokens by that counter
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_one_question_its_tokens_its_price_and_the.py

**HTML: One answer's tokens: the packed set's estimate, the model's count, and the price / Do it: one question, its tokens, its price, and the estimate beside it**

Do it: one question, its tokens, its price, and the estimate beside it

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question, a rupee).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the answer: tokens_in 1xxx | cached_tokens 0 | tokens_out 4xx | cost_usd 0.00xxxx | citations 3 | model gemini-3.6-flash
cost.price(): $0.00xxxx = Rs 0.xxxx at 85.0 | in 1xxx out 4xx cached 0
the estimate for the same packed set: fixed 168 + context 8xx = 1xxx | the model counted 1xxx | ratio 0.9x
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_dated_revision_in_the_stream_read_revi.py

**HTML: A dated document on the lane: the header's date, the rule in the prompt, the citation event / Do it: the dated revision in, the stream read, revision 1 back**

Do it: the dated revision in, the stream read, revision 1 back

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one upload, one streamed question, one upload; paise).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> event chunks embedded effective_from: ingest_reactivated	3	0	2026-10-01
citation 1 smoke_note.md | effective_from 2026-10-01 | quote 'The smoke lantern is kept in bay 7 of the Pune wa'
done: tokens_in 1xxx | tokens_out 3xx | latency_ms 2xxx | the price is on the row, not in the event
answer: The smoke lantern is kept in bay 7 of the Pune warehouse [1], effective from 1 October 2026 ...
>> event chunks embedded effective_from: ingest_reactivated	3	0	None
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_the_day_s_tokens_and_the_retries_there_wer.py

**HTML: The answer's reserve, the retry, and the tokens on the rows / Do it: the day's tokens, and the retries there were not**

Do it: the day's tokens, and the retries there were not

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: two log reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
acme                        NN     xxxxx     xxxx    0.0xxx      x.xx    4xxx   0.0x
2026-09-2xT1x:xx:xx.xxxxxxZ	context_budget_drop		1x	x
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_the_knob_a_budget_too_small_on_a_candidate_that.py

**HTML: What the budget costs, the knob on a candidate, and the lines this lesson leaves empty / The knob: a budget too small, on a candidate that takes no traffic**

max_context_tokens is a setting, so the way to see the drop on the live corpus without touching the live service is a candidate revision, as in lessons 5.2 to 5.4: a budget of 600 tokens leaves room for about three handbook sections after the fixed prompt, so the same question at top_k 5 packs three, drops two, logs the drop, and answers from what it packed. The variable is not set on the live service, so the undo removes it and the default returns.

Run instruction: bash — run in the operator shell (one new revision, no traffic; one question; one log read; then the undo).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
candidate: tokens_in 6xx | citations 2 | answerable True | pool 20
2026-09-2xT1x:xx:xx.xxxxxxZ	3	2
template now:
(empty means unset: the default, 8000)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

35 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 25 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
