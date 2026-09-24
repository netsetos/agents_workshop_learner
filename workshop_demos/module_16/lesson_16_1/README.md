# Lesson 16.1: Query a video clip and validate media citations

**Summary:** the clip at its second; `make smoke-media` green. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html); Git blob `6580ee3d4f24d9fb786f5672f22d54789f8a197a`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the contract and the UI's pill, run; no network) |
| s4 · window 10 | [demo_04_01_definition.py](demo_04_01_definition.py) | bash — run in the operator shell, in the kit (the town hall synthesised: a minute or two) |
| s4 · window 13 | [demo_04_02_definition.py](demo_04_02_definition.py) | bash — run in the operator shell, in the kit (the transcript withdrawn from acme) |
| s4 · window 16 | [demo_04_03_definition.py](demo_04_03_definition.py) | bash — run in the operator shell, in the kit (the video uploaded; waits for the worker) |
| s4 · window 18 | [demo_04_04_definition.py](demo_04_04_definition.py) | bash — run in the operator shell, in the kit (reads only) |
| s5 · window 23 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (golden row mm-03's question, as the UI asks it) |
| s6 · window 25 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the gate: a minute or two) |

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

**HTML: From a segment to a pill, run / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the contract and the UI's pill, run; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. resolve(): 2 draft citations in, 1 out ([Source 7] was not in the context):
   {'chunk_id': 'acme:77e0...#1', 'source_uri': 'gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4', 'page': None, 'score': 0.88, 'kind': 'segment', 'media_url': 'gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4', 'start': 200.7, 'end': 238.0}
2. the answer as the UI draws it: Revenue in EMEA fell 5.2 per cent, from 96 crore to 91 crore [Clip 3, 03:20].
   under Sources: the video from second 200, captioned 03:20 – 03:58 of townhall_2026_q1.mp4
3. the pills for the three sources: [1] [Fig 2] [Clip 3, 03:20] | a segment with no start: [Clip 3, ?]
4. the usage row's modality: video | the same answer from the table and the figure: image
5. mm-03, citing [Source 3]: kinds ['segment'] -> counts
5. mm-03, citing [Source 1]: kinds ['text'] -> cited no segment
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_definition.py

**HTML: The clip built, the transcript withdrawn, the video heard / Definition**

make media MEDIA_ARGS=--video runs evals/build_media.py:

Run instruction: bash — run in the operator shell, in the kit (the town hall synthesised: a minute or two).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python evals/build_media.py --video
  keep annual_report_2026_fig3.png (43 KB) - exists; --force re-renders
  keep inv_2026_0412.png (123 KB) - exists; --force re-renders
  keep payment_of_bonus_act_1965_p30.png (151 KB) - exists; --force re-renders
  voices: {'Meera': 'en-IN-Chirp3-HD-Aoede', 'Arjun': 'en-IN-Chirp3-HD-Charon'}
  Meera    0.0-  21.5s  Good morning, everyone, and welcome to the FY2026 town hall....
  Arjun   22.2-  57.7s  Thanks, Meera. Let me start with the table you all have on s...
  Meera   58.4-  69.6s  On people, headcount closed at 4,180, up from 3,742, and att...
  Arjun   70.3-  93.1s  On capital expenditure we invested 78 crore during the year....
  Meera   93.8- 104.8s  Thank you, Arjun. Questions are open on the portal until Fri...
  corpus/acme/townhall_2026_q1.mp4: 1.5 MB, 106 s, 5 utterances; ground truth beside it in townhall_2026_q1.segments.json
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_definition.py

**HTML: The clip built, the transcript withdrawn, the video heard / Definition**

Next, the transcript goes. upload.sh keeps a transcript home once its video exists, as it keeps a PDF's text mirror home, but it removes nothing already sent: make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back.

Run instruction: bash — run in the operator shell, in the kit (the transcript withdrawn from acme).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.md", "fingerprint": "1a19e8a7d490616d", "retired_doc_keys": ["acme_b0d7702de2bf5a7d0770de433916af821b4a83f13ca321e074293ef99f4d75c1"], "retired_ids": ["acme:b0d7702de2bf5a7d0770de433916af821b4a83f13ca321e074293ef99f4d75c1#0"], "retired_chunks": 1, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_03_definition.py

**HTML: The clip built, the transcript withdrawn, the video heard / Definition**

make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back. Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call:

Run instruction: bash — run in the operator shell, in the kit (the video uploaded; waits for the worker).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
>> gs://documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4 - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	acme_a85a89590f9a2b8b7ffc8588e11578297c5bc1fe5181482b0ef75d22d00881d3	5	0	5	0	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=townhall_2026_q1.mp4 API=<candidate url>
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_04_definition.py

**HTML: The clip built, the transcript withdrawn, the video heard / Definition**

Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call: Last, read the video's rows from acme's index, and hold them against the ground truth:

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
5 segments of townhall_2026_q1.mp4 in acme's index, against the ground truth's 5 turns:
  segment t0-22     00:00-00:22   22 s  over Meera 00:00
      Meera, the CEO, opens the FY2026 town hall over a first slide saying the video is synthetic, welcoming s...
  segment t22-58    00:22-00:58   36 s  over Arjun 00:22
      Arjun, the CFO, walks through the revenue table on slide two: India grew from 412 to 508 crore, up 23.3 ...
  segment t58-70    00:58-01:10   12 s  over Meera 00:58
      Meera says headcount closed at 4,180, up from 3,742, and attrition came down to 11.4 per cent from 14.9 ...
  segment t70-93    01:10-01:33   23 s  over Arjun 01:10
      Arjun says capital expenditure was 78 crore for the year: 31 crore went into the Hyderabad plant expansi...
  segment t93-105   01:33-01:45   12 s  over Meera 01:33
      Meera thanks Arjun and says questions are open on the portal until Friday, over a closing slide. The rec...
checks: longest 36 s (the prompt asks for at most 60) -> PASS; start before end in every row -> PASS; last end 01:45 against the speech's end 01:44
the EMEA line: Arjun says '5.2 per cent' in the turn at 00:22-00:57; the segment that quotes it: t22-58
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The clip at its second / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (golden row mm-03's question, as the UI asks it).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
5 sources packed: [1] segment [2] figure [3] text [4] segment [5] text
the UI shows: The CFO said EMEA was the one region that shrank: revenue fell 5.2 per cent, from 96 crore to 91 crore, because two large renewals in Germany slipped into the first quarter of FY2027 [Clip 4, 00:22].
run_eval's rule for mm-03: cited kinds ['segment'], a segment asked for -> PASS
the ground truth: Arjun says '5.2 per cent' in the turn 00:22-00:57
[Clip 4]: the player opens townhall_2026_q1.mp4 at 00:22, the clip runs to 00:58; it holds the turn -> PASS
  open it at that second, for 15 minutes, as documind-ui-sa:
  https://storage.googleapis.com/documind-ai-YOUR-ID-uploads/acme/townhall_2026_q1.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=documind-ui-sa%40documind-ai-YOUR-ID.iam.gserviceaccount.com%2F20260924%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260924T083000Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=...#t=22
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: make smoke-media, green / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the gate: a minute or two).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
DocuMind Module 9 - live smoke test
  api: https://documind-api-NUMBER.asia-south1.run.app
  mcp: https://documind-mcp-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] generate  blob=acme/gen/cd18d3eb6f6dd202ce999de17eb66160.png cached=False
  [PASS] outsider refused  status=403
  [PASS] figure citation  kinds=['figure'] media_url=gs://documind-ai-YOUR-ID-uploads/acme/annual_report_2026_fig  "EMEA's revenue declined, from Rs 96 crore in FY2025 to Rs 91"
  [PASS] media documents  4 of 21 indexed documents are media: ['annual_report_2026_fig3.png', 'inv_2026_0412.png', 'payment_of_bonus_act_1965_p30.png', 'townhall_2026_q1.mp4']
  [PASS] signed PUT  gs://documind-ai-YOUR-ID-uploads/acme/smoke_media_probe.png
  [PASS] worker indexed the PUT  chunks=1 at 2026-09-24T08:14:00.300000+00:00
  --------------------------------------------------------
  6 passed, 0 failed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

26 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 16 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
