# Lesson 8.2: Test valid access, denied access and cross-tenant requests

**Summary:** 401 and 403 side by side; isolation 1.00. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html); Git blob `2bfa77b0d346884ddcee1c93f3b8bb4643d84862`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (four requests to /v1/query; one is answered) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (11 outsider requests, then 11 member questions) |
| s5 · window 17 | [demo_05_01_do_it_the_three_policies.py](demo_05_01_do_it_the_three_policies.py) | bash — run in the operator shell, in the kit (each tenant's data_region; reads only) |
| s6 · window 19 | [demo_06_01_the_policy_against_a_pin_a_tenant_kept_in_india.py](demo_06_01_the_policy_against_a_pin_a_tenant_kept_in_india.py) | bash — run in the operator shell, in the kit (a pin set, one question, its usage row, the pin cleared) |
| s7 · window 23 | [demo_07_01_the_kit_s_own_tests_of_the_same_refusals.py](demo_07_01_the_kit_s_own_tests_of_the_same_refusals.py) | bash — run in the operator shell, in the kit (the kit's smoke test, two of its lines) |

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

**HTML: The refusal ladder: the door, a 401 and a 403 side by side / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (four requests to /v1/query; one is answered).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
no token                   403  (Cloud Run's own page: the request never reached the API)
  a token without its email  401  {"detail":"the bearer token carries no verified email"}
  the outsider's token       403  {"detail":"not a member of this tenant"}
  documind-ui-sa's token     200  {"answer":"A confirmed employee at grade E3 or above serves a noti
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Cross-tenant: every isolation row, as the outsider and as a member / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (11 outsider requests, then 11 member questions).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the outsider, on 11 isolation rows: 403 on 100%
  iso-01 as zeta   HTTP 200  answerable True   no '40,000'
  iso-02 as globex HTTP 200  answerable False  no '1,84,500'
  iso-03 as globex HTTP 200  answerable False  no '15 June'
  iso-04 as zeta   HTTP 200  answerable False  no '1,005'
  iso-05 as zeta   HTTP 200  answerable False  no 'AAAPZ1234C'
  iso-06 as globex HTTP 200  answerable False  no 'twenty-six weeks'
  iso-07 as globex HTTP 200  answerable False  no "fifteen days' wages"
  iso-08 as zeta   HTTP 200  answerable False  no 'recommendations of the Council'
  iso-09 as zeta   HTTP 200  answerable False  no 'single point of contact'
  iso-10 as globex HTTP 200  answerable False  no 'twice the rate of wages'
  mm-04  as zeta   HTTP 200  answerable False  no '5.2 per cent'
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_the_three_policies.py

**HTML: Residency: each tenant's data_region, and the rule that applies it / Do it: the three policies**

Do it: the three policies

Run instruction: bash — run in the operator shell, in the kit (each tenant's data_region; reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: data_region=any
zeta: data_region=any
globex: data_region=in
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_the_policy_against_a_pin_a_tenant_kept_in_india.py

**HTML: The policy against a pin: a tenant kept in India, pinned to a store outside it / The policy against a pin: a tenant kept in India, pinned to a store outside it**

A pin set, a minute's wait, one question, its usage row, and the pin cleared. The cell pins globex to rag_engine, a managed store in us-central1, then waits a minute, because the API reads each tenant's settings once a minute. It asks one of globex's own questions and reads the question's usage row: which backend served, and policy_fallback. Then it clears the pin. RETRIEVAL_BACKEND is given on each make line on purpose, because a value exported in your shell would otherwise win.

Run instruction: bash — run in the operator shell, in the kit (a pin set, one question, its usage row, the pin cleared).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
globex: retrieval_backend=rag_engine
globex asked: HTTP 200, answerable True
vector	1
globex: retrieval_backend=default
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_the_kit_s_own_tests_of_the_same_refusals.py

**HTML: The kit's own tests of the same refusals / The kit's own tests of the same refusals**

The smoke test's check 3b, and the chat service's check 4. The kit asserts these refusals itself, so a deploy that opened a door would fail its own smoke test. smoke/smoke.py sends its question again with no token and passes only on 401 or 403. smoke/smoke_chat.py asks the chat service as the outsider and passes only on a 403 from the roster, not a 401 from the verifier. The MCP server's smoke test does the same. The cell runs the API's smoke test and keeps two of its lines.

Run instruction: bash — run in the operator shell, in the kit (the kit's smoke test, two of its lines).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
[PASS] no token refused  status=403
  N pass · 0 fail
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

24 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 16 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
