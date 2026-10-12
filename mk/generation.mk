# ---------- Generation (the v5 course's Module 3): the generator's prompt, its knobs and its version ----------
# Included by the Makefile (`include mk/*.mk`); every variable it uses is declared there. Each target runs one script,
# and the script runs the same way without make.

# The prompt bench (evals/prompt_bench.py, lessons 3.1, 3.2 and 3.3): each golden row's pool read once from your lane's
# /v1/passages, as documind-ui-sa, then held fixed while the kit's own generate() (services/rag-api/generator.py,
# imported in your shell: pip install -r services/rag-api/requirements.txt once) answers it at each thinking level, with
# or without a temperature, with SYSTEM's rules edited in memory; generator.py is never written. Every answer is judged
# by the eval gate's rule. BENCH_ARGS names the rows and the arms: "--rows lk-06 --runs 5 --levels LOW,HIGH",
# "--shape join --levels LOW,MEDIUM,HIGH", "--from-report evals/reports/live.json --failing --shape refusal
# --add-rule '...'", "--temperature 2.0", "--drop-rule 5", "--model gemini-3.1-flash-lite", "--show", "--report FILE".
# One Gemini call an answer (two when one is cut off and asked again), billed to your lane; it prints the rupees.
bench: guard-project
	@AUD=https://documind-api-$$(gcloud projects describe $(PROJECT) --format='value(projectNumber)').$(REGION).run.app; \
	API=$${API:-$$AUD}; \
	TOKEN=$${DOCUMIND_ID_TOKEN:-$$(gcloud auth print-identity-token --include-email \
	  --impersonate-service-account=documind-ui-sa@$(PROJECT).iam.gserviceaccount.com --audiences=$$AUD)}; \
	echo ">> $$API"; DOCUMIND_ID_TOKEN=$$TOKEN GOOGLE_CLOUD_PROJECT=$(PROJECT) \
	  $(PY) evals/prompt_bench.py --api-url $$API $(BENCH_ARGS)

# The prompt bound to its version (lesson 3.6): the label the rag-api answers under (config.py's prompt_id@prompt_version,
# what /version reports), the sha256 of generator.py's SYSTEM followed by DATED_RULE, and whether
# services/rag-api/prompt_versions.json registers that label with that sha256. Exit 1 when the text changed and the
# version did not: a changed prompt needs a new version, registered beside the old ones. Offline: no project, no
# credential, Rs 0.
prompt-version:
	$(PY) commands/prompt_pin.py
