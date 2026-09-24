# Lesson 6.4: Complete the Streamlit upload-to-answer journey

**Summary:** upload, the version listed, a cited answer streams. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html); Git blob `1434ee937aa77b8465276e8080c069b3d951e632`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once per shell |
| s3 · window 11 | [demo_03_01_do_it_the_service_s_account_iap_s_flag_who_may_s.py](demo_03_01_do_it_the_service_s_account_iap_s_flag_who_may_s.py) | bash — run in the operator shell (four reads) |
| s4 · window 16 | [demo_04_01_do_it_write_the_note_upload_it_in_the_browser_fo.py](demo_04_01_do_it_write_the_note_upload_it_in_the_browser_fo.py) | bash — run in the operator shell (writes one small file in your home directory) |
| s4 · window 17 | [demo_04_02_do_it_write_the_note_upload_it_in_the_browser_fo.py](demo_04_02_do_it_write_the_note_upload_it_in_the_browser_fo.py) | bash — run in the operator shell (the object, the worker's line, your hash, the ledger row) |
| s5 · window 23 | [demo_05_01_do_it_ask_in_the_browser_ask_from_the_shell_read.py](demo_05_01_do_it_ask_in_the_browser_ask_from_the_shell_read.py) | bash — run in the operator shell (one question, a rupee; one log read) |
| s6 · window 28 | [demo_06_01_do_it_open_the_source_then_render_your_own_trans.py](demo_06_01_do_it_open_the_source_then_render_your_own_trans.py) | bash — run in the operator shell (one stream, a rupee) |
| s7 · window 33 | [demo_07_01_do_it_read_the_account_s_grants_rs_0.py](demo_07_01_do_it_read_the_account_s_grants_rs_0.py) | bash — run in the operator shell (reads only) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The UI's own environment says how it signs people in, where it uploads and which API it calls. The block prints the five names that matter and exports the UI's address for the steps below. An empty CHAT_URL means the chat service is not deployed on this lane, and then Chat has no brain picker. The page streams from the API directly, which is the journey this lesson follows.

Run instruction: bash — run in the operator shell, once per shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
AUTH_MODE      iap
RAG_API_URL    https://documind-api-NUMBER.asia-south1.run.app
UPLOAD_BUCKET  documind-ai-YOUR-ID-uploads
IAP_AUDIENCE   /projects/NUMBER/locations/asia-south1/services/documind-ui
CHAT_URL       https://documind-chat-NUMBER.asia-south1.run.app
UI=https://documind-ui-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_the_service_s_account_iap_s_flag_who_may_s.py

**HTML: The front door: IAP, the UI's settings, and who may sign in / Do it: the service's account, IAP's flag, who may sign in, and a request without one**

Do it: the service's account, IAP's flag, who may sign in, and a request without one

Run instruction: bash — run in the operator shell (four reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    run.googleapis.com/iap-enabled: 'true'
roles/iap.httpsResourceAccessor	user:you@example.com
without a sign-in: HTTP 302 -> https://accounts.google.com/o/oauth2/v2/auth?client_id=...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_write_the_note_upload_it_in_the_browser_fo.py

**HTML: The upload: a note you write, uploaded in the browser, followed to the ledger / Do it: write the note, upload it in the browser, follow it**

First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault.

Run instruction: bash — run in the operator shell (writes one small file in your home directory).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_write_the_note_upload_it_in_the_browser_fo.py

**HTML: The upload: a note you write, uploaded in the browser, followed to the ledger / Do it: write the note, upload it in the browser, follow it**

First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault. In the browser, open Documents, choose the file, and click Index documents. The page reports the object it wrote and its generation, then says the upload is complete and indexing is still in progress. Wait half a minute and click Refresh indexing status until the note appears in Versions. Then follow it from the shell:

Run instruction: bash — run in the operator shell (the object, the worker's line, your hash, the ledger row).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
text/plain	4xx	17586xxxxxxxxxxx
2026-09-2xT1x:xx:xx.xxxxxxZ	acme_3f9c2b7e1a04...	3	0	3
your file's hash begins: 3f9c2b7e1a04
acme/pune_visitor_rules.md indexed chunks 3 reused 0 embedded 3
versions NN | last event ingest_ok
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_ask_in_the_browser_ask_from_the_shell_read.py

**HTML: The answer: asked in Chat, streamed, and the row that names you / Do it: ask in the browser, ask from the shell, read both rows**

In the browser, open Chat and ask: What colour badge do visitors wear at the Pune warehouse? The sources arrive first and the answer streams after them. The answer ends with a pill. Hover over it to see the note's clause, and open Sources under the answer. Then ask the same question from the shell and read the two newest rows:

Run instruction: bash — run in the operator shell (one question, a rupee; one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
from the shell: Every visitor to the Pune warehouse wears an amber badge, issued at gate | ['pune_visitor_rules.md']
2026-09-2xT1x:xx:xx.xxxxxxZ	query	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	ui	acme	20
2026-09-2xT1x:xx:xx.xxxxxxZ	stream	you@example.com	ui	acme	20
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_open_the_source_then_render_your_own_trans.py

**HTML: Citations: the pills, the sources, and the link signed through IAM / Do it: open the source, then render your own transcript**

In the browser, under the answer from step 5, open Sources and click Open source on the note. A new tab shows the note's text from the bucket, through a link that stops working in 15 minutes. Then capture the same answer as a transcript and paste it into the renderer in step 1:

Run instruction: bash — run in the operator shell (one stream, a rupee).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
citation events: 5 | tokens: NN | done: 1
first citation: pune_visitor_rules.md | kind text | page None | quote 'VR-01 - Badges\nEvery visitor to the Pune warehou'
...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_read_the_account_s_grants_rs_0.py

**HTML: The UI's account: what it may do, and the checks the page makes first / Do it: read the account's grants, Rs 0**

Do it: read the account's grants, Rs 0

Run instruction: bash — run in the operator shell (reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
project roles:
roles/aiplatform.user
roles/datastore.user
roles/documentai.apiUser
roles/secretmanager.secretAccessor
roles/speech.editor
uploads bucket: ['roles/storage.objectAdmin']
may invoke documind-api: ['roles/run.invoker']
may invoke documind-chat: ['roles/run.invoker']
may invoke documind-ingest: none
on itself: ['roles/iam.serviceAccountTokenCreator']
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
