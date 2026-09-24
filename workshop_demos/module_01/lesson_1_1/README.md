# Lesson 1.1: Reproduce the local environment and read the master diagram

**Summary:** the Rs 0 lane answers the notice-period question with citations.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_inspect_the_workstation_and_corpus.py

[Inspect the workstation and corpus](demo_01_inspect_the_workstation_and_corpus.py) — required

Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

Expected observation: The IDE interpreter and tool paths are visible; the ACME handbook exists.

### demo_02_start_the_local_chat_lane.py

[Start the local chat lane](demo_02_start_the_local_chat_lane.py) — required

Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

Expected observation: The local chat server listens on port 8081. Ollama and the model must already be available; inspect the actual service output.

### demo_03_ask_the_local_notice_period_question.py

[Ask the local notice-period question](demo_03_ask_the_local_notice_period_question.py) — required

Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

Expected observation: A local answer with citations. Starting the server is a prerequisite even though it runs in another console.

### finish_04_stop_this_local_chat_service.py

[Stop this local chat service](finish_04_stop_this_local_chat_service.py) — cleanup

Stop only the background process group started by this lesson, after checking its PID, command and working directory. Preserve its log and lesson evidence.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
