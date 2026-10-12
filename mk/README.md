# mk/ - the Makefile, one file per lane

The kit's `Makefile` keeps what every target shares: the variables (`PROJECT`, `REGION`, the Terraform variable
list, the service list), `guard-project`, `.PHONY`, and the core lifecycle of a lane (`plan`, `up`, `build`,
`deploy-services`, `down`, the smokes, the release). Everything a course module teaches as its own operations lives
here, one file per lane, pulled in by `include mk/*.mk`:

| File | Targets | Course module |
|---|---|---|
| `ingestion.mk` | `roster`, `tenant-policy`, `tenant-backend`, `vector-status`, `wait-vectors`, `backfill-vectors`, `ingest-one`, `poison`, `dlq` | 3 Ingestion |
| `lifecycle.mk` | `reindex`, `retire`, `restore`, `reconcile`, `backfill-current`, `reconcile-job`, `sources`, `purge`, `smoke-reindex`, `batch-job`, `batch`, `queued` | 4 Lifecycle |
| `retrieval.mk` | `decide` | 2 Retrieval (the answer-or-refuse eval, lesson 2.6: `evals/decide.py`, with Jev behind `JEV_MODE`) |
| `generation.mk` | `bench`, `prompt-version` | 3 Generation (the prompt bench, lessons 3.1-3.3: `evals/prompt_bench.py`, each row's pool held fixed while the kit's own `generate()` answers at each thinking level, temperature or rule edit; the prompt bound to its version, lesson 3.6: `commands/prompt_pin.py` against `services/rag-api/prompt_versions.json`) |
| `agents.mk` | `desk-check`, `route-probe`, `route-index`, `route-calibrate`, `doc-types`, `limits`, `limits-check`, `limits-drill`, `desk`, `roles`, `desk-queues`, `cases`, `cases-overdue`, `smoke-cases`, `smoke-desk`, `route-eval`, `desk-views`, `desk-job`, `desk-operators`, `deploy-gchat`, `smoke-gchat`, `agent-turn`, `agent-eval`, `agent-tests`, `approval-check`, `exemplars` | 10 Agents (a chat turn's limits, lesson 5.5; the DocuMind Desk, lessons 5.6 and 10.4, and its Google Chat door; the agent bench, lessons 10.1-10.3 and 10.5, and a person in the loop, offline, lesson 5.8, appended below the Desk's targets; the router's prompt examples on and off, lesson 3.2, last in the file) |
| `evaluation.mk` | `label-sheet`, `judge-agree`, `judge-frozen` | 4 Evals and safety (the LLM judge checked against people, lesson 4.5: `evals/build_judge_set.py`, `evals/judge_agree.py`, and `evals/judge.py` on the frozen rows); lesson 4.9's triage and attack targets join it |
| `memory.mk` | `thread`, `replay` | 6 Context and memory (a conversation's checkpoints read back from the lane, and one turn replayed and forked locally, lesson 6.8: `commands/thread_read.py` and `commands/thread_replay.py`, run in `~/graph-venv` by `commands/graph-venv.sh`) |
| `release.mk` | `ci-vars`, `keys-check` | 11 Project (the keyless pipeline's repository variables and the key check, lesson 11.1) |

The Makefile pins the default goal to `dryrun` (Tier A: offline, free), so a bare `make` never depends on which file
here sorts first. Still, always name the target. Two files add variables of their own: `agents.mk` declares `DESK_JOB`,
`CHAT_IMAGE`, `DESK_EVAL_SAS`, `DESK_ROUTER_ALERTS`, `DESK_GATE_ALERTS` and `GCHAT_DOOR`, and appends all but
`DESK_EVAL_SAS` to the Makefile's Terraform variable list (`TF_EXTRA_VARS +=`, which works because that list is a
recursive variable and the `include` comes after it); `retrieval.mk` declares `JEV_MODE` (`off`, `recorded` or
`live`; `off` by default) and passes it to `evals/decide.py` alone.

Three rules keep the files small:

1. **A target is a one-line entry.** A recipe longer than a few lines is a script under `commands/` (`ingest-one.sh`,
   `poison.sh`, `reindex.sh`, `wait-vectors.sh`, `vector-status.sh`, `limits-check.sh`, `limits-drill.sh`, `desk-check.sh`,
   `agent-turn.sh`, `approval-check.sh`, `graph-venv.sh` with `thread_read.py` and `thread_replay.py`) or a
   subcommand of `commands/lane.py` (`sources`, `queued`, `vector-status`, `backfill-vectors`, `roster`,
   `tenant-backend`, `tenant-policy`, `limits`), or of `commands/desk_ops.py` for the DocuMind Desk's targets
   (`doc-types`, `desk`, `roles`, `desk-queues`, `cases`, `route-index`), or of `commands/release.py` for the release's
   (`ci-vars`, and `keys` for `keys-check`). The make target and the direct call run the same code, so a learner without `make` -
   Windows, Colab - runs `PROJECT=<id> TENANT=acme FILE=... bash commands/ingest-one.sh` or
   `python commands/lane.py sources`.
2. **The comment travels with the target.** The design notes that explained a target in the Makefile sit above it
   here, unchanged.
3. **A new module is a new file.** Add `mk/<lane>.mk`, list its targets in the Makefile's `.PHONY`, and give any
   long recipe a script, a `lane.py` subcommand or, for the Desk, a `desk_ops.py` subcommand first. Nothing else
   changes: `tools/check_*.py` read the Makefile and `mk/*.mk` as one text, and the publish (`tools/publish_learner.py`
   in the authoring repository) copies every tracked file under the kit.

Moved on 22 September 2026, with every target's name, comment and recipe kept byte for byte except the six that
became scripts and one comment that still said five delivery attempts (eventarc.tf says twelve); the scripts also fix a latent slip in the old recipes, where a `FILE=` or golden-set check that
failed inside `( ...; exit 1 )` did not stop the recipe.
