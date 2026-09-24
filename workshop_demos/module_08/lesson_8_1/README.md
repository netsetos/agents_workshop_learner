# Lesson 8.1: Trace authenticated identity into tenant membership

**Summary:** the identity and tenant on a usage row. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html); Git blob `4a2c528ee001991a66c0c2fdde1d412dbe008472`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it_the_api_s_audiences_and_who_may_invoke_it.py](demo_03_01_do_it_the_api_s_audiences_and_who_may_invoke_it.py) | bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only) |
| s3 · window 12 | [demo_03_02_do_it_what_your_token_says_about_itself.py](demo_03_02_do_it_what_your_token_says_about_itself.py) | bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent) |
| s4 · window 17 | [demo_04_01_do_it_the_three_rosters_as_firestore_holds_them.py](demo_04_01_do_it_the_three_rosters_as_firestore_holds_them.py) | bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only) |
| s4 · window 19 | [demo_04_02_do_it_the_plan_make_roster_would_write_for_you.py](demo_04_02_do_it_the_plan_make_roster_would_write_for_you.py) | bash — run in the operator shell, in the kit (make roster's plan; --dry-run writes nothing) |
| s5 · window 24 | [demo_05_01_do_it_which_services_call_the_shared_verifier.py](demo_05_01_do_it_which_services_call_the_shared_verifier.py) | bash — run in the operator shell, in the kit (which services call the shared verifier) |
| s6 · window 27 | [demo_06_01_one_request_end_to_end_a_forged_header_and_the_r.py](demo_06_01_one_request_end_to_end_a_forged_header_and_the_r.py) | bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows) |
| s7 · window 29 | [demo_07_01_the_person_s_leg_how_a_signed_in_person_reaches.py](demo_07_01_the_person_s_leg_how_a_signed_in_person_reaches.py) | bash — run in the operator shell, in the kit (every caller the API recorded in the last day) |

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

### demo_03_01_do_it_the_api_s_audiences_and_who_may_invoke_it.py

**HTML: The door and the verifier: who may knock, and what makes a token count / Do it: the API's audiences, and who may invoke it**

Do it: the API's audiences, and who may invoke it

Run instruction: bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
IAP_AUDIENCE  /projects/NUMBER/locations/asia-south1/services/documind-ui
              /projects/NUMBER/locations/asia-south1/services/documind-chat
SELF_URL      https://documind-api-NUMBER.asia-south1.run.app
run.invoker   serviceAccount:documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-outsider-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_what_your_token_says_about_itself.py

**HTML: The door and the verifier: who may knock, and what makes a token count / Do it: what your token says about itself**

The cell mints two tokens for the API as documind-ui-sa: one the way tok does, and one without --include-email. It reads their claims without verifying them; the API does the verifying. Nothing is sent.

Run instruction: bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
TOKEN: aud https://documind-api-NUMBER.asia-south1.run.app
       email documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com, email_verified True, iss https://accounts.google.com, 59 minutes left
BARE: aud https://documind-api-NUMBER.asia-south1.run.app
       email (none), email_verified (none), iss https://accounts.google.com, 59 minutes left
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_three_rosters_as_firestore_holds_them.py

**HTML: The roster: one document per member, two ways to read it, one writer / Do it: the three rosters, as Firestore holds them**

Do it: the three rosters, as Firestore holds them

Run instruction: bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme    5 member(s)
    documind-agent-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    you@example.com
zeta    3 member(s)
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
globex  3 member(s)
    documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_plan_make_roster_would_write_for_you.py

**HTML: The roster: one document per member, two ways to read it, one writer / Do it: the plan make roster would write for you**

make roster runs this command without --dry-run. The dry run prints the memberships and the data-region policies it would set, and writes nothing.

Run instruction: bash — run in the operator shell, in the kit (make roster's plan; --dry-run writes nothing).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
would put you@example.com on acme
would put documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on acme
would put documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on zeta
would put documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on globex
would put documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on acme
would put documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on zeta
would put documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on globex
would put documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on acme
would put documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on zeta
would put documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on globex
would put documind-agent-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com on acme
would set acme: data_region=any
would set zeta: data_region=any
would set globex: data_region=in
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_which_services_call_the_shared_verifier.py

**HTML: The surfaces: who calls the shared verifier, and who still keeps a copy / Do it: which services call the shared verifier**

Do it: which services call the shared verifier

Run instruction: bash — run in the operator shell, in the kit (which services call the shared verifier).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
services/chat/agent.py
services/mcp/server.py
services/rag-api/auth.py
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_one_request_end_to_end_a_forged_header_and_the_r.py

**HTML: One request, end to end: a forged header, and the row that ignores it / One request, end to end: a forged header, and the row that ignores it**

Two questions to acme, one claiming to be the CEO, and the two usage rows they leave. The cell asks the same question twice with run_eval.py's own ask(), which sets an x-user-email header on every request. The first names the eval account; the second claims to be ceo@acme.example. Both carry your token and no assertion, so the bearer leg names the caller. After twenty seconds for the logs to land, the cell reads the two newest query rows for acme.

Run instruction: bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
x-user-email eval@documind.in   HTTP 200, answerable True
x-user-email ceo@acme.example   HTTP 200, answerable True
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_the_person_s_leg_how_a_signed_in_person_reaches.py

**HTML: The person's leg: how a signed-in person reaches the API through the UI / The person's leg: how a signed-in person reaches the API through the UI**

IAP in front of the UI, the assertion forwarded beside the UI's token, and every caller the API recorded in a day. A person never calls the API directly. They sign in at IAP in front of the UI, which admits only accounts granted the sign-in role. IAP hands the UI a signed assertion with every request. When the UI calls the API, it sends two credentials, as its _headers() shows in step 5: its own token, which gets past the door, and the person's assertion, forwarded unchanged. The API's verifier sees the assertion first and takes the person's email from it. The roster check and the usage row are then about the person, which is what lesson 6.4 saw in Chat. The cell counts every caller the API recorded in the last day.

Run instruction: bash — run in the operator shell, in the kit (every caller the API recorded in the last day).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
NN documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
      N you@example.com
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

30 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 20 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
