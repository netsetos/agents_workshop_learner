# Lesson 18.3: Inspect the vLLM service and the GKE alternative

**Summary:** the manifest read; the duty-cycle sum. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.3-vllm-gke/Netsetos_GCP_Capstone_18.3_VLLM_GKE_WIX.html); Git blob `21dd5be3863147eb2597fe93610d080fce9979d1`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (reads the service's files; no network) |
| s4 · window 14 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (reads the manifest and the image it runs; no network) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (read-only: describes the lane's cluster, looks for the vLLM service and image) |
| s5 · window 19 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit (it stops before changing anything on a Standard lab) |
| s6 · window 22 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell (arithmetic only; no network) |

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

**HTML: The vLLM service, read / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the service's files; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the image: FROM vllm/vllm-openai:v0.28.0, then python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1 --timeout-keep-alive 120
  weights in the image: none - no step fetches them, and the HF_TOKEN build-arg cloudbuild.yaml passes has no ARG to land in
  so the engine downloads google/gemma-3-4b-it when it starts, from Hugging Face
  the environment make deploy-vllm gives it: GOOGLE_CLOUD_PROJECT - no Hugging Face token
the service: 1 nvidia-l4, 8 vCPU, 32Gi; 0 to 1 instance; 32 requests at a time; startup probe 120 s + 5 x 30 s = 270 s
its door: every chat completion needs an X-API-Key header, hashed and looked up in Firestore (api_keys then tenants)
  what the gateway's token proxy sends: its own ID token as Authorization, and no X-API-Key
  code elsewhere in the kit that writes an api_keys document: none
  roles Terraform grants documind-vllm-sa, the account it runs as: none
its request log: BigQuery table 'project.dataset.inference_logs'
the gateway's route to it: documind-inference, http://127.0.0.1:8090/vllm/v1, falling back to documind-slm, documind-general
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The manifest, read / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the manifest and the image it runs; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Deployment documind-vllm: 1 replica, and no autoscaler
  its node: nodeSelector cloud.google.com/gke-accelerator=nvidia-l4, so Autopilot provisions an L4 node for the pod
  image: ${IMAGE}, which make gke-up fills in: asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/gemma-vllm:latest
  limits: 1 GPU, 6 vCPU, 24Gi (requests default to the limits)
  env: HF_HUB_OFFLINE=1
  startup probe: GET /health every 10 s, 60 failures allowed: 600 s to load
  args: --model=google/gemma-3-4b-it --dtype=bfloat16 --gpu-memory-utilization=0.90 --max-model-len=4096 --port=8080
Service documind-vllm: ClusterIP (no type named, so the default), port 80 to 8080: no address outside the cluster
the image it runs: ENTRYPOINT [], CMD python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1 --timeout-keep-alive 120
  the manifest sets args and no command, and the ENTRYPOINT is empty: the container runs '--model=google/gemma-3-4b-it' as its program
  main.py takes its model from the environment (MODEL_NAME), and reads none of those args
  the image holds no weights (step 3), and HF_HUB_OFFLINE=1 forbids the download
verdict: as written, this pod cannot start
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The lane's cluster, inspected / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (read-only: describes the lane's cluster, looks for the vLLM service and image).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-autopilot: STANDARD, a regional control plane in asia-south1, on documind-vpc, RUNNING
  node pool documind-lab: 1 x e2-standard-2 in asia-south1-a, 30 GB pd-standard, GPU: none
  what it bills while it exists: $0.10 an hour for the control plane (the free tier covers only zonal and Autopilot clusters) + $0.0805 for the node = $0.1805 an hour, Rs 15.34; Rs 11,199 for a 730-hour month, plus the disk
documind-vllm on Cloud Run (us-central1): not deployed
the gemma-vllm image in asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind: not built
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: The lane's cluster, inspected / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (it stops before changing anything on a Standard lab).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
STOP: the Standard CPU lab cannot run the L4 GPU lesson. Set gke_autopilot=true in Terraform, review cluster replacement and quota, and apply before make gke-up.
make: *** [Makefile:695: gke-up] Error 1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The duty-cycle sum / Do it**

Do it

Run instruction: bash — run in the operator shell (arithmetic only; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
your pattern: 8 bursts a day of 30 minutes, on 22 days a month
Cloud Run, on demand: each burst, then up to 10 idle minutes - an instance lives 320 minutes a day
  the duty-cycle sum: 320 min x 22 days = 117.3 hours of 730 (16.1%) x $1.4209 = $166.72, Rs 14,171 a month
GKE Autopilot, always on, for all 730 hours:
  us-central1  $0.9558 an hour (node 0.8536 + L4 0.0670 + 8 vCPU 0.0240 + 32 GiB 0.0112): Rs 59,309; with the $0.10 cluster fee, Rs 65,514
               cheaper than Cloud Run above 67.3% of the month (74.3% with the fee)
  asia-south1  $1.0113 an hour (node 0.8886 + L4 0.0805 + 8 vCPU 0.0288 + 32 GiB 0.0134): Rs 62,753; with the $0.10 cluster fee, Rs 68,958
               cheaper than Cloud Run above 71.2% of the month (78.2% with the fee)
at 16.1%: Cloud Run is cheaper - Rs 14,171 against Rs 59,309 for the cheapest GKE line
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

23 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 15 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
