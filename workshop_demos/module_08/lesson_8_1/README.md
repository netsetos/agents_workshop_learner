# Lesson 8.1: Trace authenticated identity into tenant membership

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_token_and_roster.py](demo_01_token_and_roster.py) | Inspect audiences, token claims and both membership lookup directions. |
| 3 | [demo_02_surface_identity_and_forged_header.py](demo_02_surface_identity_and_forged_header.py) | Trace shared verification across services and test a forged user header. |
| 4 | [demo_03_signed_in_person.py](demo_03_signed_in_person.py) | Follow the UI's assertion path from a signed-in person to the API. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

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

### demo_01_token_and_roster.py

Inspect audiences, token claims and both membership lookup directions.

**`step_01_the_api_s_audiences_and_who_may_invoke_it(session)` — The door and the verifier: who may knock, and what makes a token count / Do it: the API's audiences, and who may invoke it**

Do it: the API's audiences, and who may invoke it

Operation: bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only).

Expected shape, not a promised result:

```text
IAP_AUDIENCE  /projects/NUMBER/locations/asia-south1/services/documind-ui
              /projects/NUMBER/locations/asia-south1/services/documind-chat
SELF_URL      https://documind-api-NUMBER.asia-south1.run.app
run.invoker   serviceAccount:documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-outsider-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
```

**`step_02_what_your_token_says_about_itself(session)` — The door and the verifier: who may knock, and what makes a token count / Do it: what your token says about itself**

The cell mints two tokens for the API as documind-ui-sa: one the way tok does, and one without --include-email. It reads their claims without verifying them; the API does the verifying. Nothing is sent.

Operation: bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent).

Expected shape, not a promised result:

```text
TOKEN: aud https://documind-api-NUMBER.asia-south1.run.app
       email documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com, email_verified True, iss https://accounts.google.com, 59 minutes left
BARE: aud https://documind-api-NUMBER.asia-south1.run.app
       email (none), email_verified (none), iss https://accounts.google.com, 59 minutes left
```

**`step_03_the_three_rosters_as_firestore_holds_them(session)` — The roster: one document per member, two ways to read it, one writer / Do it: the three rosters, as Firestore holds them**

Do it: the three rosters, as Firestore holds them

Operation: bash — run in the operator shell, in the kit (the three rosters in Firestore; reads only).

Expected shape, not a promised result:

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

**`step_04_the_plan_make_roster_would_write_for_you(session)` — The roster: one document per member, two ways to read it, one writer / Do it: the plan make roster would write for you**

make roster runs this command without --dry-run. The dry run prints the memberships and the data-region policies it would set, and writes nothing.

Operation: bash — run in the operator shell, in the kit (make roster's plan; --dry-run writes nothing).

Expected shape, not a promised result:

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

### demo_02_surface_identity_and_forged_header.py

Trace shared verification across services and test a forged user header.

**`step_01_which_services_call_the_shared_verifier(session)` — The surfaces: who calls the shared verifier, and who still keeps a copy / Do it: which services call the shared verifier**

Do it: which services call the shared verifier

Operation: bash — run in the operator shell, in the kit (which services call the shared verifier).

Expected shape, not a promised result:

```text
services/chat/agent.py
services/mcp/server.py
services/rag-api/auth.py
```

**`step_02_one_request_end_to_end_a_forged_header_and(session)` — One request, end to end: a forged header, and the row that ignores it / One request, end to end: a forged header, and the row that ignores it**

Two questions to acme, one claiming to be the CEO, and the two usage rows they leave. The cell asks the same question twice with run_eval.py's own ask(), which sets an x-user-email header on every request. The first names the eval account; the second claims to be ceo@acme.example. Both carry your token and no assertion, so the bearer leg names the caller. After twenty seconds for the logs to land, the cell reads the two newest query rows for acme.

Operation: bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows).

Expected shape, not a promised result:

```text
x-user-email eval@documind.in   HTTP 200, answerable True
x-user-email ceo@acme.example   HTTP 200, answerable True
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme
```

### demo_03_signed_in_person.py

Follow the UI's assertion path from a signed-in person to the API.

**`step_01_the_person_s_leg_how_a_signed_in_person_re(session)` — The person's leg: how a signed-in person reaches the API through the UI / The person's leg: how a signed-in person reaches the API through the UI**

IAP in front of the UI, the assertion forwarded beside the UI's token, and every caller the API recorded in a day. A person never calls the API directly. They sign in at IAP in front of the UI, which admits only accounts granted the sign-in role. IAP hands the UI a signed assertion with every request. When the UI calls the API, it sends two credentials, as its _headers() shows in step 5: its own token, which gets past the door, and the person's assertion, forwarded unchanged. The API's verifier sees the assertion first and takes the person's email from it. The roster check and the usage row are then about the person, which is what lesson 6.4 saw in Chat. The cell counts every caller the API recorded in the last day.

Operation: bash — run in the operator shell, in the kit (every caller the API recorded in the last day).

Manual action: Sign in through the deployed UI as the lesson's rostered person and submit the example question. Type done before inspecting the person's assertion path.

Expected shape, not a promised result:

```text
NN documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
      N you@example.com
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html). All 30 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `4a2c528ee001991a66c0c2fdde1d412dbe008472`.
