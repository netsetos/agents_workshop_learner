# Lesson 5.1: Apply query embeddings and authorized filters

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_query_vector_and_identity.py](demo_01_query_vector_and_identity.py) | Search the verified deployment directly, then compare authorized tenant requests. |
| 3 | [demo_02_filters_and_backend_selection.py](demo_02_filters_and_backend_selection.py) | Exercise the filter contract and inspect per-request backend stages. |
| 4 | [demo_03_current_version_evidence.py](demo_03_current_version_evidence.py) | Compare the question answered by successive document versions. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The intended Terraform state/index deployment; preflight rejects empty or mismatched endpoint IDs.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Conditional recovery

- [recovery/repair_deployed_index_id.py](recovery/repair_deployed_index_id.py) — Explicit recovery: repair deployed index id

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

Prepare this lesson's saved settings and dependencies before its live experiments.

**`step_01_run_first_check_the_serving_revision_and_s(session)` — Before the demo: verify the index, then select the tenant backend / Run first: check the serving revision and save the original pin**

Run in $DEMO_ROOT. This reads the single revision receiving traffic, checks that its deployed ID exists, saves only the relevant settings under operator-evidence/lesson51/, and then selects vector for Acme. Empty optional settings take their code defaults. It stops before any embedding or tenant change if the deployment is invalid. A split-traffic service needs a chosen revision before this single-revision demonstration can proceed.

Operation: bash — run before step 3; reads configuration and saves/sets the Acme pin.

### demo_01_query_vector_and_identity.py

Search the verified deployment directly, then compare authorized tenant requests.

**`step_01_embed_search_compare(session)` — The question's vector: direct candidates and API citations / Do it: embed, search, compare**

Run the preflight first. This cell uses its verified settings, checks the endpoint and Acme pin again before paying for an embedding, searches with the same tenant/current restricts, then compares candidate IDs with the API citations. Overlap and first-citation order are observations, not pass/fail assertions. Hybrid retrieval, graph candidates, current-version checks and reranking can change the final selection.

Operation: bash — run in the operator shell (a Python cell, then one question; a paid embedding of a few hundred characters).

Expected shape, not a promised result:

```text
Actual deployed ID: the ID verified during preflight
Direct dense candidates: non-empty for the loaded handbook
stages.retrieval_backend: vector
vector_chunks: greater than 0
PASS: the direct search worked and Vector Search contributed to the API pool.
```

**`step_02_one_identity_two_tenants_one_outsider(session)` — Authorized: the tenant comes from identity, and one index serves three / Do it: one identity, two tenants, one outsider**

The UI's service account, which your tok() impersonates, sits on all three rosters. The first two calls send it the same question against acme and zeta; the third sends the outsider's token; the fourth sends the UI's token with a header that claims to be someone else. Each line shows the HTTP status. A request turned away for a reason that passes, a model quota hit, a Cloud Run scale-up or a dropped connection, is asked once more after five seconds; anything else prints the reason the service gave instead of a traceback.

Operation: bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise).

Expected shape, not a promised result:

```text
acme: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 40,000. | ['hr_policy_2026.md']
zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 25,000 against | ['hr_policy_zeta_2026.md']
outsider on acme: HTTP 403 | not a member of this tenant
ui-sa with a false header on zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement | the header changed nothing
```

### demo_02_filters_and_backend_selection.py

Exercise the filter contract and inspect per-request backend stages.

**`step_01_four_filters_four_verdicts(session)` — Filters: two keys, a 400 for everything else / Do it: four filters, four verdicts**

Do it: four filters, four verdicts

Operation: bash — run in the operator shell (two 400s cost nothing; two questions, paise).

Expected shape, not a promised result:

```text
400 | unknown filter key(s) tenant_id; allowed: doc_type, kind
400 | filter doc_type must be a non-empty string
200 | answerable False pool 0 | The corpus holds nothing near this question: no passage of this
200 | answerable True pool 20 | A confirmed employee at grade E3 or above serves a notice period
```

**`step_02_the_tenant_s_pin_and_policy_then_a_full_st(session)` — The restricts, the per-request backend, and the stages block / Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question**

Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question

Operation: bash — run in the operator shell, in $DEMO_ROOT (two reads, one question).

Expected shape, not a promised result:

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

### demo_03_current_version_evidence.py

Compare the question answered by successive document versions.

**`step_01_the_question_the_revisions_answered_differ(session)` — Current is the ledger's filter, never the caller's / Do it: the question the revisions answered differently**

Do it: the question the revisions answered differently

Operation: bash — run in the operator shell (one question, then the cited row read off Firestore).

Expected shape, not a promised result:

```text
A confirmed employee at grade E3 or above serves a notice period of 60 days ... [Source 1]
cited acme:497809ffbaa6...#1
the cited row: NP-03 | current: True | doc_key: acme_497809ff... | text starts: NP-03 — Notice period A confirmed employee at grade E3 or above
NP-03 rows on the lane: 3 | current: 1 | saying 90 days: 2 (retired, never cited)
```

### recovery/repair_deployed_index_id.py

Explicit recovery: repair deployed index id

**`step_01_run_first_check_the_serving_revision_and_s(session)` — Before the demo: verify the index, then select the tenant backend / Run first: check the serving revision and save the original pin**

Continue only after PASS. Keep Acme on vector through steps 3–9. The API environment's RETRIEVAL_BACKEND is a default; the tenant pin overrides it. If step 3 still reports the old backend, wait for that one-minute cache to expire, then retry. This is a configuration repair for an existing index, not an index-creation step. Read the ID from the intended Terraform state and prove that it is deployed on the same endpoint. The following block refuses an endpoint mismatch or missing deployment. It creates a corrected API revision and routes 100% of the demo service's traffic to it. Other environment variables are retained; do not rerun the full infrastructure deployment to fix this one setting.

Operation: bash — optional repair; updates the API revision and its traffic.

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_finish_restore_the_saved_tenant_pin(session)` — Finish: restore the saved tenant pin / Finish: restore the saved tenant pin**

Run only after steps 3–9. Restore the value saved before the demo, which may be rag_engine, another backend or default. The last option removes the explicit pin. Do not assume every lane originally used RAG Engine, and do not place this command beside the setup command.

Operation: bash — end of lesson only; restore the original Acme pin.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html`. All 29 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `71dc43310c171099ca29431ddb48a29c6af8965e`.
