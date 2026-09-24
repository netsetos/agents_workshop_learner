# Lesson 5.1: Apply query embeddings and authorized filters

**Summary:** an unknown filter key answered 400; `stages.retrieval_backend` on the answer. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html); Git blob `71dc43310c171099ca29431ddb48a29c6af8965e`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 4 | [demo_02_01_run_first_check_the_serving_revision_and_save_th.py](demo_02_01_run_first_check_the_serving_revision_and_save_th.py) | bash — run before step 3; reads configuration and saves/sets the Acme pin |
| s3 · window 8 | [demo_03_01_do_it_embed_search_compare.py](demo_03_01_do_it_embed_search_compare.py) | bash — run in the operator shell (a Python cell, then one question; a paid embedding of a few hundred characters) |
| s4 · window 13 | [demo_04_01_do_it_one_identity_two_tenants_one_outsider.py](demo_04_01_do_it_one_identity_two_tenants_one_outsider.py) | bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise) |
| s5 · window 16 | [demo_05_01_do_it_four_filters_four_verdicts.py](demo_05_01_do_it_four_filters_four_verdicts.py) | bash — run in the operator shell (two 400s cost nothing; two questions, paise) |
| s6 · window 21 | [demo_06_01_do_it_the_tenant_s_pin_and_policy_then_a_full_st.py](demo_06_01_do_it_the_tenant_s_pin_and_policy_then_a_full_st.py) | bash — run in the operator shell, in $DEMO_ROOT (two reads, one question) |
| s7 · window 25 | [demo_07_01_do_it_the_question_the_revisions_answered_differ.py](demo_07_01_do_it_the_question_the_revisions_answered_differ.py) | bash — run in the operator shell (one question, then the cited row read off Firestore) |
| s9 · window 29 | [demo_09_01_finish_restore_the_saved_tenant_pin.py](demo_09_01_finish_restore_the_saved_tenant_pin.py) | bash — end of lesson only; restore the original Acme pin |

## Conditional recovery

- [recover_02_01_run_first_check_the_serving_revision_and_save_th.py](recover_02_01_run_first_check_the_serving_revision_and_save_th.py) — bash — optional repair; updates the API revision and its traffic

## Checkpoints and explanation

### demo_02_01_run_first_check_the_serving_revision_and_save_th.py

**HTML: Before the demo: verify the index, then select the tenant backend / Run first: check the serving revision and save the original pin**

Run in $DEMO_ROOT. This reads the single revision receiving traffic, checks that its deployed ID exists, saves only the relevant settings under operator-evidence/lesson51/, and then selects vector for Acme. Empty optional settings take their code defaults. It stops before any embedding or tenant change if the deployment is invalid. A split-traffic service needs a chosen revision before this single-revision demonstration can proceed.

Run instruction: bash — run before step 3; reads configuration and saves/sets the Acme pin.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_02_01_run_first_check_the_serving_revision_and_save_th.py

**HTML: Before the demo: verify the index, then select the tenant backend / Run first: check the serving revision and save the original pin**

Continue only after PASS. Keep Acme on vector through steps 3–9. The API environment's RETRIEVAL_BACKEND is a default; the tenant pin overrides it. If step 3 still reports the old backend, wait for that one-minute cache to expire, then retry. This is a configuration repair for an existing index, not an index-creation step. Read the ID from the intended Terraform state and prove that it is deployed on the same endpoint. The following block refuses an endpoint mismatch or missing deployment. It creates a corrected API revision and routes 100% of the demo service's traffic to it. Other environment variables are retained; do not rerun the full infrastructure deployment to fix this one setting.

Run instruction: bash — optional repair; updates the API revision and its traffic.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_embed_search_compare.py

**HTML: The question's vector: direct candidates and API citations / Do it: embed, search, compare**

Run the preflight first. This cell uses its verified settings, checks the endpoint and Acme pin again before paying for an embedding, searches with the same tenant/current restricts, then compares candidate IDs with the API citations. Overlap and first-citation order are observations, not pass/fail assertions. Hybrid retrieval, graph candidates, current-version checks and reranking can change the final selection.

Run instruction: bash — run in the operator shell (a Python cell, then one question; a paid embedding of a few hundred characters).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Actual deployed ID: the ID verified during preflight
Direct dense candidates: non-empty for the loaded handbook
stages.retrieval_backend: vector
vector_chunks: greater than 0
PASS: the direct search worked and Vector Search contributed to the API pool.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_one_identity_two_tenants_one_outsider.py

**HTML: Authorized: the tenant comes from identity, and one index serves three / Do it: one identity, two tenants, one outsider**

The UI's service account, which your tok() impersonates, sits on all three rosters. The first two calls send it the same question against acme and zeta; the third sends the outsider's token; the fourth sends the UI's token with a header that claims to be someone else. Each line shows the HTTP status. A request turned away for a reason that passes, a model quota hit, a Cloud Run scale-up or a dropped connection, is asked once more after five seconds; anything else prints the reason the service gave instead of a traceback.

Run instruction: bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 40,000. | ['hr_policy_2026.md']
zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 25,000 against | ['hr_policy_zeta_2026.md']
outsider on acme: HTTP 403 | not a member of this tenant
ui-sa with a false header on zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement | the header changed nothing
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_four_filters_four_verdicts.py

**HTML: Filters: two keys, a 400 for everything else / Do it: four filters, four verdicts**

Do it: four filters, four verdicts

Run instruction: bash — run in the operator shell (two 400s cost nothing; two questions, paise).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
400 | unknown filter key(s) tenant_id; allowed: doc_type, kind
400 | filter doc_type must be a non-empty string
200 | answerable False pool 0 | The corpus holds nothing near this question: no passage of this
200 | answerable True pool 20 | A confirmed employee at grade E3 or above serves a notice period
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_tenant_s_pin_and_policy_then_a_full_st.py

**HTML: The restricts, the per-request backend, and the stages block / Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question**

Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (two reads, one question).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=vector
acme: data_region=any
{
 "policy_fallback": 0,
 "retrieval_backend": "vector",
 "retrieve_ms": 612,
 "pool": 20,
 "graph_chunks": 0,
 "managed_chunks": 0,
 "vector_chunks": 20,
 "rerank_ms": 388,
 "generate_ms": 1742
}
citations 3 | cache_hit none | latency_ms 2760
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_the_question_the_revisions_answered_differ.py

**HTML: Current is the ledger's filter, never the caller's / Do it: the question the revisions answered differently**

Do it: the question the revisions answered differently

Run instruction: bash — run in the operator shell (one question, then the cited row read off Firestore).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
A confirmed employee at grade E3 or above serves a notice period of 60 days ... [Source 1]
cited acme:497809ffbaa6...#1
the cited row: NP-03 | current: True | doc_key: acme_497809ff... | text starts: NP-03 — Notice period A confirmed employee at grade E3 or above
NP-03 rows on the lane: 3 | current: 1 | saying 90 days: 2 (retired, never cited)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_09_01_finish_restore_the_saved_tenant_pin.py

**HTML: Finish: restore the saved tenant pin / Finish: restore the saved tenant pin**

Run only after steps 3–9. Restore the value saved before the demo, which may be rag_engine, another backend or default. The last option removes the explicit pin. Do not assume every lane originally used RAG Engine, and do not place this command beside the setup command.

Run instruction: bash — end of lesson only; restore the original Acme pin.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

29 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 20 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
