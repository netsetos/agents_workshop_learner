# ---------- Evaluation (the v5 course's Module 4): the LLM judge checked against people, lesson 4.5 ----------
# Included by the Makefile (`include mk/*.mk`); every variable it uses is declared there, and each target's own inputs
# take their defaults in the recipe. Each recipe is one line of the kit's own Python, which runs the same way without
# make: evals/build_judge_set.py and evals/judge_agree.py (standard library only, Rs 0) and evals/judge.py.

# The judge set (lesson 4.5): about twenty of a lane's answers, frozen with the full text of the chunks they cite
# (evals/judge_set.json), so every reader - you, the author, a peer and the judge - reads the same rows. A blank label
# sheet for one person: groundedness and answers_the_question, yes or no, on every row, with the question, the answer
# and the context to read by. It never overwrites a sheet. LABELS= the file (default evals/reports/judge_labels.csv);
# READER= the pseudonymous id on it (default you). Check a filled one: python evals/build_judge_set.py --check FILE.
label-sheet:
	$(PY) evals/build_judge_set.py --emit $(or $(LABELS),evals/reports/judge_labels.csv) --reader $(or $(READER),you)

# Agreement on the judge set, Rs 0. PEOPLE=1: your sheet (LABELS=) against the author's labels of the same rows, or
# AGAINST= another reader's - Cohen's kappa per rubric, the 2x2, the rows you differ on. Without PEOPLE: the judge's
# ratings of the same rows (RUN=, default the author's capture evals/judge_set.ratings.jsonl; make judge-frozen writes
# your own) against your sheet - the true-pass and false-pass rates with Wilson intervals, and kappa. The judge's 1-5
# metric passes at CUT or more (default 4); SWEEP=1 prints every cut.
judge-agree:
	$(PY) evals/judge_agree.py $(if $(PEOPLE),people $(or $(LABELS),evals/reports/judge_labels.csv) $(or $(AGAINST),evals/judge_labels.L1.csv),judge $(or $(RUN),evals/judge_set.ratings.jsonl) $(or $(LABELS),evals/reports/judge_labels.csv) --cut $(or $(CUT),4) $(if $(SWEEP),--sweep,))

# Your lane's judge on the frozen rows (lesson 4.5): judge.py rates evals/judge_set.json as it stands (--reuse, and
# --no-enrich so the context is the one people labelled), two Vertex AI Evaluation requests a row in us-central1, and
# nothing asked of the API. The per-row ratings go to RUN= (default evals/reports/judge_set.ratings.jsonl). In the
# judge's venv, as make judge: PY="$HOME/judge-venv/bin/python". JUDGE_ARGS passes more (--judge-model ...).
judge-frozen: guard-project
	@test -f evals/judge_set.json || { echo "evals/judge_set.json is not in this kit yet: lesson 4.5's frozen rows arrive with the author's capture" >&2; exit 2; }
	$(PY) evals/judge.py --api-url frozen:evals/judge_set.json --project $(PROJECT) --reuse evals/judge_set.json --no-enrich --label frozen --save-rows $(or $(RUN),evals/reports/judge_set.ratings.jsonl) $(JUDGE_ARGS)
