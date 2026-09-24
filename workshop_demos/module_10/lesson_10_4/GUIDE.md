# Lesson 10.4: source reading guide

Read this beside the three demo files. The prose below follows the main HTML;
its terminal setup is replaced by the documented Python setup. Read-only code
and sample output are not executable steps. Sample values are not live results.

Source: the lesson's main page, `Netsetos_GCP_Capstone_10.4_Adapters_WIX.html`, reviewed at blob `4d85e128644454856f18a930ac9e3dfcec8d55e1`. Learners read that page on the course site; this guide keeps its prose.

The chat service can answer with four brains, and all four reach the same `retrieve()`. What differs is the adapter between each framework and that one tool. It decides what the model is shown, what is filled in behind its back, what the model reads back and what happens when a call fails. It also decides where the conversation is kept and what gets counted. You put the LangChain adapter beside the ADK adapter offline, on the kit's own code. Then you ask one question through all four brains on your lane and read the four cost lines that rag-api's rows give. Last, you measure the half of each line those rows cannot see.

- One tool, four harnesses

- The words: adapter, harness, ToolRuntime, FunctionTool, callback, session, cost line

- Before you run anything: set up the shell

- Two adapters over one tool, side by side

- Four brains on /health, and the module's gate

- Four cost lines, as rag-api's rows draw them

- The half the rows cannot see

- Why the adapters differ, what it costs, and what the kit does not do yet

- Verify it yourself: the checklist

You will learn the six things an adapter decides, and how the LangChain adapter and the ADK adapter decide each one differently. You will also see why the cost comparison the kit draws from rag-api's rows leaves out the part where the brains differ. Then you will prove it: four brains on `/health`, one answer from each through the module's gate, four cost lines from the rows, and each agent brain's own model calls, measured.

### One tool, four harnesses

What an adapter decides, and why two frameworks decide it differently.

The tool is one. `shared/documind_tools.retrieve()` is the only code that talks to rag-api. A brain decides when to call it and what to do with the result, and nothing more. Between each framework and that function sits an adapter. The adapter decides six things: what the model is shown, what is filled in behind it, what the model reads back, what happens when a call fails, where the conversation is kept, and what gets counted.

The LangChain adapter wraps. The LangChain and LangGraph brains use `services/chat/tools.py`: three `@tool` functions around the shared ones. The tenant, the person's assertion and the brain's name arrive through `ToolRuntime`, which the framework injects and leaves out of the schema. So the model is shown `query`, `doc_type` and `top_k`, and nothing else. The adapter drops rag-api's own answer from the result and rewords a failure. The framework turns a bad argument or an unknown name into an error result, which the model reads and explains.

The ADK adapter passes through. The ADK brain wraps the shared functions directly in `FunctionTool`, which builds the declaration from the Python signature and docstring. So the model is shown `tenant_id` as a required argument, with `assertion` and `brain` beside it and the whole docstring. A callback, `before_tool_callback`, overwrites the tenant and the brain before each call. The model cannot choose the tenant, but it must still write one. The result comes back unchanged, rag-api's answer included. A failure is not turned into data: a call that raises, a bad argument or a name ADK does not hold fails the whole turn.

The cost line counts the shared part. The direct brain has no loop: one `retrieve()`, and rag-api's grounded answer is the answer. Every `retrieve()`, from any brain, leaves a row in rag-api's log with the brain's name, the tokens and the cost. That gives the kit's comparison: four lines, one per brain. No row records the agent's own model calls, at least two a turn for each agent brain. So the four lines look alike, because they count the one thing the brains share.

A sub-registrar's record room, and four ways to get a certified copy. The record room is one. Every request goes through its counter, and its register notes the fee and the name of the clerk who asked. One clerk follows the office manual, with a supervisor checking each slip. One follows a flowchart you drew yourself. The third comes from an agency whose request form has a box for "whose file?". The supervisor strikes out whatever that clerk wrote there and fills in the right name. When a slip is rejected, this clerk walks out rather than coming back to explain. The fourth window simply hands you the copy. The register shows four nearly equal fees. The clerks' own time, which is where they differ, appears on no register.

#### Two brains, side by side

Choose two brains to see how each decides the 14 things below. The rows where they differ are shaded.

Each value is read from the kit's code at build time. The arguments, the character counts, what each model reads and the failures come from step 3's cell, run on the kit's `brains.py` and `tools.py` with google-adk 2.8.0.

It compares the adapters as the kit builds them, not the quality of their answers. Lesson 7.2's judge scores answers. With `CHAT_URL` set, `make judge` also checks each agent brain's tool calls against the one call the kit expects, a single `retrieve`.

### The words: adapter, harness, ToolRuntime, FunctionTool, callback, session, cost line

Ten rows, each with the value it takes on your lane.

One distinction to hold: an adapter decides what crosses the boundary, and a harness decides how many times it is crossed. Both show up in the cost line.

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

The shell, in the kit's folder, with `PROJECT`, `REGION`, `NUMBER`, `API` and `tok`. You need `~/graph-venv` from lesson 10.2. Step 3 adds google-adk and the Gemini client to it, and makes it if it is missing. The chat service must be running in your region, from lesson 10.1's step 3. Step 4 asks one question through each brain, and step 6 asks it three more times from your machine. Run steps 4 to 6 in the same shell, in order. Nothing changes on your lane.

### Two adapters over one tool, side by side

The kit's LangChain brain and the kit's ADK brain, each with a model that says what it is told, against a rag-api on your machine that notes what it is sent.

#### Definition

The cell builds the kit's `LangChainBrain` and `AdkBrain`, each with a scripted model. A stand-in rag-api on your machine notes the tenant, the brain and the assertion header of every request, and answers. The cell prints four things:

- What each model is shown for `retrieve`: the arguments, the required ones starred, and the declaration's size. Then each brain's tools.

- One `retrieve()` through each adapter. The ADK model writes `tenant_id` "globex" and `assertion` "anything". The cell prints what rag-api received, and which keys the model read back.

- Three calls that go wrong: a blocked name, an argument of the wrong type, and a tier the tool does not know.

- Where ADK keeps sessions when no database is configured, and its cap on model calls.

The LangGraph brain uses the same `tools.py` as the LangChain brain, so its schema, its results and its failures are the same. Its guard is the refuse node from lesson 10.2.

#### The code

#### Do it: the venv

#### Do it: side by side

The LangChain model was shown three arguments in 465 characters. The ADK model was shown six, two of them required, in 2,572 characters, and every model call carries that declaration. Both requests reached rag-api for acme. `ToolRuntime` never let the LangChain model near the tenant, and the callback struck out the ADK model's globex. The assertion is different. The callback replaces it only when the request carried one, and this one did not, so the model's string went out as the assertion header. rag-api would verify it, refuse it with a 401, and the model would read that retrieval is unavailable. The ADK model also read rag-api's own answer, which the LangChain adapter drops.

Then the three failures. The LangChain brain turned the first two into error results, which the model read, and `refusals` named both. The ADK brain raised on all three. On your lane a raise is a 500, with no answer and no row. The unknown tier shows the other side of the LangChain adapter: it priced `express` as standard, and said nothing.

### Four brains on /health, and the module's gate

The list the service promises, then one answer from each brain, then the outsider refused.

#### Definition

`/health` returns the four names in `BRAINS`, a constant in `brains.py`. It builds no brain and imports no framework. Each brain is built on its first turn, and a framework the image lacks is a 501 then. `make smoke-chat` is Module 10's gate. It reads `/health` and asks one question through each brain as `documind-ui-sa`, a member of acme. For each answer it checks that `retrieve` was among the tool calls and that the answer does not say retrieval was unavailable. From the direct brain it also wants citations. Then it asks as the outsider and expects the roster's 403. The cell first saves the time, for step 5.

#### The code

#### Do it

`/health` listed four brains: the first half of the proof. That list is a promise. The four answers are the check: each brain was built, called `retrieve()` and answered from the corpus. The first turn of each agent brain was the slow one, because it imported its framework. The outsider was refused by the roster before any brain ran.

If `brain adk` fails with an answer that asks which tenant, account or corpus to search, you have met step 3's declaration. `tenant_id` is a required argument, and the model has nothing to fill it with. Running the gate again continues the three agent brains' conversations, and their turns grow with the history.

### Four cost lines, as rag-api's rows draw them

One row per retrieval, added up by brain.

#### Definition

Each `retrieve()` leaves one row in rag-api's log. The row holds the brain that asked, the tokens rag-api spent, and the cost at its model's rate. The cell reads the rows since step 4 and adds them up by brain. `make usage` draws the same by-brain table over whole hours. The cell saves the four lines to `~/lesson104_lines.json`, for step 6.

#### Do it

Four lines, one `retrieve()` each, within a few paise of each other. That is the second half of the proof, and it is also the trap. Every brain asked rag-api the same question, and rag-api did the same work each time: it retrieved, reranked and wrote a grounded answer. The direct brain returned that answer. The agent brains paid for it too: LangChain and LangGraph dropped it, and ADK read it. Nothing in these lines comes from the loops themselves.

The chat service logs a row per turn as well, with the brain, the latency and the tool calls, but it has no tokens and no cost to add. A line with 0 means that brain made no `retrieve()`. A line with 2 means its model searched twice. With the answer cache on (Module 9), a repeated question is a hit: cost 0, and backend `cache`.

### The half the rows cannot see

The kit's three agent brains on your machine, asking the same question, their own model calls counted.

#### Definition

The chat service keeps no count of its own model calls, so the cell makes one. It builds the kit's three agent brains on your machine from the same `brains.py` the image runs: the same model, system prompt and tools. It asks the same question once through each brain, through your rag-api, as `documind-ui-sa`. Then it reads the usage each framework keeps: LangChain on every `AIMessage`, ADK on the session's events. It prices input at 1.50 and output at 7.50 dollars per million tokens, `cost.py`'s rate for gemini-3.6-flash. Thinking is counted as output, as Vertex AI bills it. Last, it adds step 5's lines.

#### Do it

Each agent brain made two model calls: one to ask for `retrieve`, one to answer from what came back. The second call carries everything the first did, plus the tool result, so it is the larger. The ADK brain's calls are larger than LangChain's for two reasons you saw in step 3. Its declaration is 2,572 characters against 465, and its tool result includes rag-api's answer. Your run can show a third reason: the ADK brain sets no thinking level, and the LangChain brains set it to low.

The whole lines show what the rows hid. Each agent brain costs its retrieval plus its own loop, and the direct brain costs its retrieval alone. The loop is the price of the harness, and it is paid on every turn.

### Why the adapters differ, what it costs, and what the kit does not do yet

The design choices, from the kit's own comments, then the bill and the gaps.

- The tenant is not an argument. If it were an ordinary parameter, the model would choose the tenant, as `agent.py`'s docstring puts it. `tools.py` keeps it out of the schema with `ToolRuntime`. The ADK brain holds the same line another way: the callback overwrites whatever the model wrote. Both keep the boundary. Only one keeps it out of the model's sight.

- One retrieval, adapted per brain. `documind_tools.py` allows no second implementation. ADK wraps the function as it is, and LangChain reshapes it. The less an adapter does, the more of the function's own docstring and result the model sees.

- The brain is a switch, not a fork. Brains are built lazily and cached, and a missing framework is a 501, not a failed start. That is why `/health` can list four names without importing anything, and why the gate has to ask each brain.

- Errors as data. The shared `retrieve()` returns a failure as data, so the model can explain it rather than the turn dying. The LangChain framework does the same for bad arguments and unknown names. ADK does it only when an `on_tool_error_callback` says so.

- The direct brain is the floor. `brains.py` calls it the one the other three have to beat to justify their harness. Step 6 measures what they have to beat.

#### What it costs

Each point is checked in the kit's code, and the build asserts it, so this box changes when the kit does.

- No row counts an agent's own model calls. The chat row carries the brain, the latency and the tool calls, and no tokens or cost. rag-api's rows count only `retrieve()`. So the by-brain table in `evals/usage_rows.py` compares the one thing the brains share.

- The ADK model is shown what it should not choose. `tenant_id` is a required argument, and `assertion` and `brain` are there too. The callback overwrites `tenant_id` and `brain`. It replaces `assertion` only when the request carried one. On the bearer leg, a string the model writes goes out as the assertion header. rag-api then verifies it, rather than falling back to the token.

- ADK failures are not data. A name ADK does not hold, a bad argument or a tool that raises fails the turn: a 500, no answer and no row. `LlmAgent` has `on_tool_error_callback`, whose returned dict google-adk 2.8.0 uses as the result, even for a missing tool. The kit does not set it.

- ADK's `refusals` is always empty. It counts calls to blocked names, and a blocked name raises before the answer is returned.

- The brains are not configured alike. The LangChain brains set `thinking_level` low, and the ADK brain sets none. A cost comparison of the harnesses is also a comparison of their settings.

- `/health` lists a constant. It builds no brain, so a framework missing from the image still shows on `/health`, and answers 501 on its first turn.

### Verify it yourself: the checklist

Eight checks, each one block above, each with the value that proves it on your lane.

Nothing is configured. The three agent brains each keep the gate's conversation, `smoke-langchain`, `smoke-langgraph` or `smoke-adk`, new or one turn longer. The direct brain keeps none. rag-api's log has seven more rows, four from the gate and three from step 6. Your home folder has `~/lesson104_lines.json`, and `~/graph-venv` has google-adk. Module 11 starts from those conversations: where each one lives, and what else an agent remembers.

Netsetos GenAI on GCP · Module 10 Agents · Lesson 10.4 Compare the LangChain and ADK adapters · v5.0

Next: Lesson 11.1 Distinguish agent state, conversation history and knowledge.
