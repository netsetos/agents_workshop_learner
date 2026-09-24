# Lesson 10.3: source reading guide

Read this beside the section-numbered demo files. The prose below follows the main HTML;
its terminal setup is replaced by the documented Python setup. Read-only code
and sample output are not executable steps. Sample values are not live results.

Source: the lesson's main page, `Netsetos_GCP_Capstone_10.3_Tool_Failures_WIX.html`, reviewed at blob `8c8650c57c7da57795b534e5c7b86462f1357233`. Learners read that page on the course site; this guide keeps its prose.

A tool call can fail in more places than it can succeed. Some failures stop a request at the door, and some reach the model as an error. Some reach it as ordinary data that happens to say something went wrong. Some are noted in a log line that nobody reads. You force five failures through the kit's own LangChain brain: a blocked name, a wrong argument, a tool that does not exist, a retrieval that times out, and a call over its budget. Then you meet three identities at the chat service's door, and a filter argument the corpus cannot honour. For each one you find where it surfaced and who was told.

- Every failure has a place, and a reader

- The words: refusal, error result, payload, budget, client timeout, door, empty pool

- Before you run anything: set up the shell

- Five failures through the kit's LangChain brain

- Access failures at the chat service's door

- An argument the corpus cannot honour

- Reading a failure on the lane

- Why failures are handled this way, what it costs, and what the kit does not do yet

- Verify it yourself: the checklist

You will learn the three places a failure can surface (the HTTP status, the tool result, the log) and which failures land in `refusals`. You will also learn why a timed-out retrieval does not land there, and why the kit's time budgets stop nothing. Then you will prove it: a non-empty `refusals`, a timed-out tool reported to the model rather than left hanging, a 401 and a 403 from the door, and a filter that empties the pool.

### Every failure has a place, and a reader

Before a turn, inside a turn, and in a log line.

Before a turn, the caller is told. Cloud Run's IAM admits or refuses the token. The chat service then asks who the token names: a token that names nobody is a 401. It asks whether the roster lists them: an account on no roster is a 403. No brain runs and no model is called. The caller gets a status and a sentence, and the request log keeps the status. The tenant is decided here, from the roster, and it never becomes an argument a model could fill. So "search another tenant's documents" is not a failure the tool layer has to catch. It cannot be asked at all.

Inside a turn, the model is told, in two different ways. Some failures produce an error result: a tool message marked `error`, and `_summary()` puts its name in `refusals`. A blocked name is one, refused by the guard before the tool runs. An argument of the wrong type is another, rejected by LangChain's check. So is a tool the model named that does not exist. Other failures produce an ordinary result that carries bad news. When rag-api does not answer within `RAG_TIMEOUT_S`, the one `retrieve()` returns `{"error": ...}` as data, and a filter that matches nothing returns an empty list. The model reads both, but `refusals` counts only the first kind.

Some failures only reach a log. The LangChain brain's guard times every tool call against a budget in `TIMEOUTS`: 30 seconds for `retrieve`, 10 for the cost tool. It checks the clock after the call has returned. Over budget, it writes a warning; under, a note. It never stops a call. A tool that takes too long therefore holds the turn until its own client gives up, and for `retrieve` that is `RAG_TIMEOUT_S`, 90 seconds on the chat service.

A bank branch clearing cheques. The guard stops a stranger at the door, and the teller refuses a cheque on an account that is not yours. Both are told to your face, before anything is processed. A cheque made out for a prohibited purpose goes to the manager and comes back marked "needs approval". One whose amount in words does not match the figures comes back marked "returned". A cheque that cannot be cleared in time comes back too: "unpaid, present again", which is an answer, not a rejection. And the branch's service-time target is written in a register at closing, but it never stopped the queue.

#### Where a failure surfaces

Choose a failure to see which layer catches it, what the caller and the model are told, what the three keys say, what the logs keep, and whether the turn waits.

The texts are the kit's own. The five failures inside a turn come from step 3's cell, run at build time on the kit's `brains.py`. The door's texts are read from `agent.py` and `shared/iap.py`, and the empty pool from `main.py`.

It shows the LangChain brain, the chat service's default. The LangGraph brain refuses a blocked name with its refuse node (lesson 10.2) and has no timing guard at all. The ADK brain, in lesson 10.4, has a callback of its own.

### The words: refusal, error result, payload, budget, client timeout, door, empty pool

Ten rows, each with the value it takes on your lane.

One distinction to hold: an error result says the call did not happen, and a payload error says it happened and could not help. Only the first lands in `refusals`.

### Before you run anything: set up the shell

You need three things open: the DocuMind UI at `https://documind-ui-NUMBER.REGION.run.app` signed in as a roster member, the operator shell you set up in Module 1 (the `rag-shell-venv` environment, the kit at `$DEMO_ROOT` as a clone of the public learner repository, and the restart helper), and a Python cell in that same shell or in Colab with `google-cloud-firestore` installed and Application Default Credentials. Every command on this page is one you run; every output shown is what the lane prints. Where a value belongs to your lane (a project number, a hash), it is written as `NUMBER` or shortened with `...`.

Set up the shell once per session. The block below works on any machine with `git` and `gcloud` signed in. The first time, it clones the kit from the public learner repository, `netsetos/agents_workshop_learner`, into `~/deploy_module_rag`; every session after, it pulls the latest kit. Then it reads your project from the gcloud configuration (so there is nothing to type), moves into the kit, builds the API URL from the project number, and defines two small functions that mint identity tokens. The last line proves the API answers.

`PROJECT=` empty means gcloud has no default project on this machine: run `gcloud config set project YOUR-PROJECT-ID` with your real id, then the block again. `ME=` empty means gcloud is not signed in: `gcloud auth login` first. A `ModuleNotFoundError: No module named 'google'` from any `make` target or Python cell, or an `externally-managed-environment` error from the pip line, means this shell is not inside the venv: the prompt should start with `(rag-shell-venv)`, so run the `source` line of the block again. If that line says the file is missing, the environment was never made on this machine: Module 1's install is `python -m pip install -r shared/requirements.txt -r services/ingest/requirements.txt -r services/rag-api/requirements.txt -r services/mcp/requirements.txt`, run inside `rag-shell-venv`; the setup block installs the one package this lesson needs. `adc NOT ok` means Python's own sign-in, Application Default Credentials, cannot read Firestore. The Python cells and every `make` target that reads Firestore use it, and gcloud's sign-in does not cover it. `Reauthentication is needed` in the message means the credentials file is there but your organisation's session rules have expired it; a `make` target reports the same as `RetryError: Timeout of 60.0s exceeded` after a minute of retries. `insufficient authentication scopes` or `credentials were not found` means there is no file, and Python fell back to the machine's own service-account token, which covers the bucket but not Firestore. Either way, run `gcloud auth application-default login --no-launch-browser`, open the link it prints, sign in as the account you use on this lane, paste the code back, and run the block again. A fresh workstation instance (the hostname changes) needs this again, as it needs the venv again. If `gcloud` itself asks you to reauthenticate, run `gcloud auth login`: the two sign-ins are separate, and each can expire on its own. `git clone` failing means this machine cannot reach GitHub. `git pull` refusing with Your local changes would be overwritten means a kit file was edited on this machine: `git -C "$DEMO_ROOT" status` names it, and `git -C "$DEMO_ROOT" stash` sets the edit aside. On a machine where Module 1 copied the kit file by file, the first run keeps that copy as `~/deploy_module_rag-before-git.tgz` and turns the folder into a clone; untracked files, `.terraform` and saved `.tfvars` stay where they are. If your kit lives somewhere else, set `DEMO_ROOT` before the block. A `403` from `print-identity-token` means your account lacks the Service Account Token Creator role on the two accounts; Module 2 granted it to the operator. If your machine has the restart helper from Module 1 (`commands/session-restart.sh` in the kit), `source` it and run `rag_resume` in place of the `export PROJECT` and `export ME` lines: it restores the same values from your saved session and also sets `API_URL`, which you then copy into `API`.

#### Three kinds of code window on this page

Every window has a label. A label that starts with bash is a block to paste into the operator shell, whole, and press Enter; the Python cells are wrapped in `python - expected or log, is text to read: it is the kit's own code or the output you should see, and it has no copy button.

#### make, or the command it runs

Every `make` target on these pages is a one-line entry in the kit's `mk/ingestion.mk` or `mk/lifecycle.mk`. The entry runs a script under `commands/` or the kit's own Python, and you can run that directly: the same code, the same output, no make. `PROJECT` comes from the setup block above.

#### Which store answers acme? Pin it to the kit's own index for this lesson

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. `make up` pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like `acme:acme_497809ff...#rag-532341da71fe`, a `page` of `null` even for a PDF, and `stages.retrieval_backend: rag_engine`. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

How to tell which store answered any call: read `stages.retrieval_backend` on the response and `stages.vector_chunks` beside it. With the pin on `vector`, the backend says `vector` and `vector_chunks` equals the pool. The stamp behind that count, `found_by`, sits on each chunk inside the API and is not a field of a citation; lesson 5.3 shows how to join it to one. The chunk ids are the kit's `tenant:sha256#position` form with the page on every PDF citation.

Calls from the shell impersonate `documind-ui-sa`, the UI's own account, which `make roster` put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. `otok` mints a token for `documind-outsider-sa`, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible.

The shell, in the kit's folder, with `PROJECT`, `REGION`, `NUMBER`, `API` and `tok`. You need `~/graph-venv` from lesson 10.2, and the step 3 cell makes it if it is missing. The chat service must be running in your region, from lesson 10.1's step 3. Step 4 sends three requests to the chat service, and step 5 makes two retrievals. Nothing changes on your lane.

### Five failures through the kit's LangChain brain

A scripted model asks for five things that go wrong. The kit's guard, LangChain and the tool layer answer.

#### Definition

The cell builds the kit's `LangChainBrain`, the chat service's default, with a scripted model and an in-memory saver. It starts a rag-api on your machine that takes two seconds to answer, points the one `retrieve()` at it with a client timeout of half a second, and stands in its ID token. It captures the log lines of the guard, the adapter and `retrieve()`. Then it runs five turns. Each asks for one tool call and prints how long the turn took, `refusals`, and the result the model read, with its status. The five are:

- blocked: `delete_document`, a blocked name;

- bad args: the cost tool with `total_pages="many"`;

- no such: `summon_rain`, a tool that does not exist;

- timed out: `retrieve` against the slow rag-api;

- over budget: the cost tool, with its budget set to zero seconds.

#### The code

#### Do it: the venv

#### Do it: five failures

Three turns ended with a non-empty `refusals`: the blocked name, the bad argument and the unknown tool. That is half of this lesson's proof. Each was an error result, and the model read why. The three look alike in `refusals`. Only the result's text tells a policy refusal from a mistake. The timed-out retrieval took half a second, the client timeout, and was not left hanging. The model read `document search is unavailable` as ordinary data, so `refusals` stayed empty. That is the other half: a timed-out tool reported. The log shows three layers each saying so, in their own words: the one `retrieve()`, the adapter and the guard. The call over budget returned normally. Its only trace is the warning at the bottom, written after the fact.

### Access failures at the chat service's door

The outsider, a token that names nobody, and a roster member, each asking the same question.

#### Definition

IAM admits all three accounts to the chat service: `documind-ui-sa` and `documind-outsider-sa` both hold the invoker role on it. The service then asks `shared/iap.identity()` who is calling. A bearer token minted without `--include-email` names nobody, which is a 401. The outsider is somebody, and `tenant_for()` finds them on no roster, which is a 403. The member reaches the default brain and gets an answer. The first two never reach a brain, a tool or a model.

#### The code

#### Do it

Three statuses, three layers. The 403 came from the roster: the outsider's token was fine, and no tenant lists it. The 401 came from the identity check: the token was genuine, but carried no email to look up. The 200 came from a member, whose tenant the roster supplied. None of the requests could have named a tenant, because the chat request has no field for one. These two refusals cost nothing, because they are decided before a model is called.

### An argument the corpus cannot honour

One question with and without a `doc_type` filter, then what rag-api's rows say about it.

#### Definition

The chat service's `retrieve` tool tells the model it may filter by `doc_type`: policy, contract, invoice, form or research_paper. The worker stamps every text upload `unknown`, as lesson 5.1 found, so each of those values filters out every text document. The filter is a valid argument, so nothing refuses it. The pool simply comes back empty, and rag-api answers with its fixed empty-pool text, at no model cost. The cell asks about the April invoice with no filter, then with `doc_type` `invoice`, through the one `retrieve()`. It then reads rag-api's rows for both calls.

#### Do it

Without the filter, five citations and the invoice's total. With `doc_type` `invoice`, nothing: no citations, `answerable` false, and the empty-pool text, which reads exactly like a corpus that holds no invoice. Asked by a model, this turn ends with `tool_calls ['retrieve']` and `refusals []`. The only trace of the bad argument is rag-api's row: `pool 0`, beside a question the corpus can answer. The filter itself appears on no row and in no log.

### Reading a failure on the lane

Where each signal lives, in the order to look.

When a chat turn goes wrong in production, the evidence is spread across three services and several stores. Look in this order.

Two patterns cover most cases. `refusals` non-empty means the model asked for something it could not have: read the log line for the name. `refusals` empty with an answer that says it found nothing means either the corpus lacks it or the model narrowed the search. rag-api's row tells those apart: `pool 0` on a question you know the corpus answers points to an argument.

### Why failures are handled this way, what it costs, and what the kit does not do yet

The design choices, from the kit's own comments, then the bill and the gaps.

- 401 is not 403. A 401 means the service does not know who is asking; a 403 means it knows and will not serve them. The difference is what you need when reading logs at three in the morning, and the kit keeps it deliberately.

- Errors as data. An exception inside a tool would end the turn with nothing to say. A payload lets the model tell the person what failed, in their own words, and keeps the turn alive.

- Refuse before dispatch. The guard checks the name before the tool runs, so a blocked tool never reaches its handler, not even to fail.

- The tenant is not an argument. A model cannot be talked into another tenant's corpus, because no argument exists to carry it. The runtime supplies the tenant from the roster.

- Budgets beside the tools. `BLOCKED` and `TIMEOUTS` sit next to the tool definitions, so adding a tool without a budget or a block decision shows up in review.

#### What it costs

Each point is checked in the kit's code, and the build asserts it, so this box changes when the kit does.

- The budgets are logged, never enforced. `TIMEOUTS` is read once, by the LangChain brain's guard, after each call has returned. No brain interrupts a slow tool. `retrieve` is bounded by its client's 90 seconds, and the other two tools by nothing.

- `refusals` mixes policy and mistakes. A blocked name, a bad argument and an unknown tool all land in the same list, and nothing in the three keys says which is which.

- The arguments are logged nowhere. The guard logs names and times. The chat row keeps names. rag-api's row has no filters. A bad `doc_type` shows only as `pool 0`.

- The tool invites filters the corpus cannot honour. `retrieve`'s docstring offers policy, contract, invoice, form and research_paper, and the worker stamps every text upload `unknown`.

- The token is minted outside the `try`. In the one `retrieve()`, a failure to mint the ID token raises instead of returning data. An agent then gets an error result, and the direct brain fails the whole turn.

### Verify it yourself: the checklist

Eight checks, each one block above, each with the value that proves it on your lane.

Nothing. There are three requests in the chat service's log: a 403, a 401 and one answered turn in session `lesson103`. There are three rag-api rows: the member's turn, and step 5's two retrievals, one of them an empty pool. Lesson 10.4 puts the same question through all four brains and compares their costs and traces.

Netsetos GenAI on GCP · Module 10 Agents · Lesson 10.3 Diagnose tool arguments, access failures and timeouts · v5.0

Next: Lesson 10.4 Compare the LangChain and ADK adapters.
