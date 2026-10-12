# ---------- Release (the v5 course's Module 11): the keyless pipeline's variables and the key check, lesson 11.1 ----------
# Included by the Makefile (`include mk/*.mk`); every variable it uses is declared there. Each recipe is a subcommand of
# commands/release.py and runs the same way without make: python commands/release.py ci-vars --project <id> --region
# <region>, python commands/release.py keys --project <id>. Both only read.

# The four repository variables .github/workflows/documind-cd.yml reads, as the gh variable set lines to run against
# the repository wif.tf trusts: GCP_PROJECT and GCP_REGION from the lane's confirmed inputs, which make plan saved in
# terraform/runbook-project.auto.tfvars.json, and WIF_PROVIDER and CICD_SERVICE_ACCOUNT from terraform output. A REGION
# the lane was not planned in is refused: the Makefile's REGION defaults to us-central1, and a workflow told the wrong
# region builds into a repository that does not exist. With gh installed it reads the repository's production
# environment and warns when there is none, or no required reviewer: GitHub creates a missing environment, unprotected,
# the first time a job names it, and promote would then move traffic with nobody approving.
ci-vars: guard-project
	@$(PY) commands/release.py ci-vars --project $(PROJECT) --region $(REGION) --terraform-dir $(TF_DIR)

# Every service account in the project with its user-managed keys, and the project's parent: org_policy.tf's
# enforce_no_sa_keys needs an organization, so on a personal account's project this check is the control. Exit 1 when
# any key exists, 2 when the check could not finish.
keys-check: guard-project
	@$(PY) commands/release.py keys --project $(PROJECT)
