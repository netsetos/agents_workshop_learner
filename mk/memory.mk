# ---------- Memory (the v5 course's Module 6): a conversation's checkpoints read back, and a turn replayed and forked ----------
# Included by the Makefile (`include mk/*.mk`): PROJECT, REGION, TENANT and PY are its variables, and EMAIL, SESSION, AT,
# EXPORT, FILE, OFFLINE, FORK and DB are given on the command line. Both targets run a script under commands/ in
# ~/graph-venv with the chat image's pins (commands/graph-venv.sh), so they run the same way without make.

# A person's chat threads read back from the lane's Cloud SQL, step by step (workshop lesson 6.8), as the operator, the
# way lesson 6.6's cells reach it: the DSN from Secret Manager into memory, the Cloud SQL Python Connector and pg8000,
# and a session made read only before its first query. EMAIL (default documind-ui-sa, the account the lessons' chat
# cells ask as) lists that person's threads, one row per session; SESSION= decodes one, a row per step: when it was
# written, its source, the brain that wrote it, its next and its messages. AT= prints the messages saved at that step;
# EXPORT=<file> writes the thread for make replay; TENANT=, given on the command line, picks the tenant when a session
# is in two. Reads only, no model call. See commands/thread_read.py.
thread: guard-project
	@PY=$(PY) bash commands/graph-venv.sh --connector commands/thread_read.py --project $(PROJECT) \
	  --email "$(or $(EMAIL),documind-ui-sa@$(PROJECT).iam.gserviceaccount.com)" $(if $(SESSION),--session "$(SESSION)",) \
	  $(if $(AT),--at="$(AT)",) $(if $(EXPORT),--export "$(EXPORT)",) $(if $(filter command line,$(origin TENANT)),--tenant "$(TENANT)",)

# One turn of an exported thread replayed, then forked, on your machine and never on the lane (workshop lesson 6.8): the
# thread copied into a local saver step for step with update_state; the turn re-run from AT (by default where it
# stopped, or its last turn's question) through the kit's LangGraph brain with graph.invoke(None, ...); a fork from the
# turn's input with another question (FORK=); and every branch listed by get_state_history. OFFLINE=1: a script for the
# model, the thread's own searches answered as recorded and any other by the Rs 0 lane over evals/corpus; no network, no
# credential, Rs 0; FILE defaults to evals/threads/cut_off_turn.json, a thread cut off mid-turn. Without it: Gemini on
# location global and your lane's rag-api as documind-ui-sa, on FILE= from make thread EXPORT=: a few model calls,
# priced and printed. DB=<a new file> keeps the copy in SQLite (requirements-local.txt's pin). See commands/thread_replay.py.
replay: $(if $(OFFLINE),,guard-project)
	@if [ -z "$(OFFLINE)" ]; then NUMBER=$$(gcloud projects describe $(PROJECT) --format='value(projectNumber)') || exit 1; \
	  export GOOGLE_CLOUD_PROJECT=$(PROJECT) RAG_API_URL=https://documind-api-$$NUMBER.$(REGION).run.app \
	    DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$(PROJECT).iam.gserviceaccount.com; fi; \
	  PY=$(PY) bash commands/graph-venv.sh commands/thread_replay.py $(if $(OFFLINE),--offline,) $(if $(FILE),--file "$(FILE)",) \
	  $(if $(AT),--at="$(AT)",) $(if $(FORK),--fork "$(FORK)",) $(if $(DB),--db "$(DB)",)
