# Lesson 16.2: Exercise implemented Studio and voice features

**Summary:** a generated image and its usage row; an answer read aloud. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.2-studio-voice/Netsetos_GCP_Capstone_16.2_Studio_Voice_WIX.html); Git blob `f90dc609bf1dfc9befdb00d185c8e8f4286c122d`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the rules, run; no network) |
| s4 · window 13 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (one image, then a DEMO_MODE hit) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (two refusals, then lesson 16.1's video through the door) |
| s6 · window 18 | [demo_06_01_definition.py](demo_06_01_definition.py) | bash — run in the operator shell, in the kit (one answer, read aloud twice) |
| s6 · window 21 | [demo_06_02_definition.py](demo_06_02_definition.py) | bash — run in the operator shell, in the kit (the answer's audio, transcribed twice) |

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

**HTML: The Studio's and the voice's rules, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the rules, run; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. a generation: {'event': 'media', 'modality': 'image', 'model': 'gemini-3.1-flash-image', 'tokens_in': 0, 'cost_usd': 0.039, 'cached': False}
1. a DEMO_MODE hit: {'event': 'media', 'modality': 'image', 'model': 'gemini-3.1-flash-image', 'tokens_in': 0, 'cost_usd': 0.0, 'cached': True}
2. event=chat    copied       by the sink, never read by tenant_daily
2. event=media   never copied by the sink, read by tenant_daily
2. event=query   copied       by the sink, read by tenant_daily
2. event=stream  copied       by the sink, read by tenant_daily
3. read aloud 1, en-IN-Chirp3-HD-Kore: synthesised, then cached (1 object in the bucket)
3. read aloud 2, en-IN-Chirp3-HD-Kore: read back from the cache (1 object in the bucket)
3. read aloud 3, hi-IN-Chirp3-HD-Kore: synthesised, then cached (2 objects in the bucket)
   the first object: tts/171aae62fa1f4b3a....ogg, the SHA-256 of 'en-IN-Chirp3-HD-Kore|1.0|ogg|' and the text
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: A generated image, and its usage row / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (one image, then a DEMO_MODE hit).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
generate 1: {'blob': 'acme/gen/9b79e5785c446f20e956772bbe9e2781.png', 'bucket': 'documind-ai-YOUR-ID-media', 'cached': False}
generate 2: {'blob': 'acme/gen/9b79e5785c446f20e956772bbe9e2781.png', 'bucket': 'documind-ai-YOUR-ID-media', 'cached': True}
the usage rows since 2026-09-24T08:10:00Z (Cloud Logging, oldest first):
  tenant acme, modality image, model gemini-3.1-flash-image, cost_usd 0.039, cached False, user documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
  tenant acme, modality image, model gemini-3.1-flash-image, cost_usd 0.0, cached True, user documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
the audit events since then, in documind-ai-YOUR-ID-audit (kept five years): 1
  media.generate by documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com: acme/gen/9b79e5785c446f20e956772bbe9e2781.png, meta {'model': 'gemini-3.1-flash-image', 'synthid': True, 'prompt_sha': '9b79e5785c446f20e956772bbe9e2781'}
the image, for 15 minutes, as documind-ui-sa (the Studio's own signer):
  https://storage.googleapis.com/documind-ai-YOUR-ID-media/acme/gen/9b79e5785c446f20e956772bbe9e2781.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=documind-ui-sa%40documind-ai-YOUR-ID.iam.gserviceaccount.com%2F20260924%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260924T083000Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The upload door / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (two refusals, then lesson 16.1's video through the door).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
upload-url townhall.zip as application/zip: (400, "content_type must be one of ['application/pdf', 'audio/mpeg', 'image/jpeg', 'image/png', 'text/markdown', 'text/plain', 'video/mp4']")
upload-url ../globex/townhall_2026_q1.mp4 as video/mp4: (400, 'filename must be a bare name')
upload-url townhall_2026_q1.mp4 as video/mp4: 200, a PUT into gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4, signed for 15 minutes
PUT 1,474,032 bytes straight to the bucket: HTTP 200
the worker: {"event": "ingest_duplicate", "doc_key": "acme_2b7f0b3acad009d5e38d869a87861150807d598e862de6d72a5349bafaee97d8"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_definition.py

**HTML: An answer read aloud, and a question nobody hears / Definition**

The first cell asks the town hall question as documind-ui-sa. It reads the answer aloud with the UI's own cached_tts, twice, and saves the audio as ~/answer.ogg. The text is the answer's first 1,500 characters, as the chat's toggle reads it.

Run instruction: bash — run in the operator shell, in the kit (one answer, read aloud twice).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the answer: The CFO said EMEA was the one region that shrank: revenue fell 5.2 per cent, from 96 crore to 91 crore, because two large renewals in Germany slipped into the first quarter of FY2027 [3].
read aloud 1: a miss, synthesised by Chirp 3 HD and written to gs://documind-ai-YOUR-ID-tts-cache/tts/d28fac84987c....ogg (36,799 bytes of Ogg Opus)
read aloud 2: a hit, read back from gs://documind-ai-YOUR-ID-tts-cache/tts/d28fac84987c....ogg (36,799 bytes of Ogg Opus)
saved ~/answer.ogg: in Cloud Shell, cloudshell download ~/answer.ogg hands it to your browser to play
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_definition.py

**HTML: An answer read aloud, and a question nobody hears / Definition**

Play it: in Cloud Shell, cloudshell download ~/answer.ogg hands the file to your browser. That is the second proof: an answer read aloud. The second cell gives that audio to the UI's own transcribe, first where the UI runs it, then in eu. eu is a location Google lists chirp_3 in, for Hindi and English (India). The audio leaves India for that one call: a synthetic voice reading an answer about acme, whose policy is any (lesson 15.3). This is the function:

Run instruction: bash — run in the operator shell, in the kit (the answer's audio, transcribed twice).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
transcribe() where the UI runs it, asia-south1: ''
transcribe() in eu: 'The CFO said EMEA was the one region that shrank: revenue fell 5.2 per cent, from 96 crore to 91 crore, because two large renewals in Germany slipped into the first quarter of FY2027.'
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

22 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 14 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
