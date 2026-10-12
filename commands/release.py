#!/usr/bin/env python3
"""The release's operator commands (the v5 course's Module 11): what mk/release.mk runs, without make.

    python commands/release.py ci-vars --project <id> --region <region>    make ci-vars     (lesson 11.1)
    python commands/release.py keys --project <id>                         make keys-check  (lesson 11.1)

Both subcommands only read: terraform output, the lane's confirmed inputs, gcloud's describe and list calls and, when gh
is installed, one GET of the repository's production environment. Neither writes to Google Cloud, to GitHub or to
this checkout, so neither has a switch. Every tool is found on PATH the way a shell finds it (gcloud is gcloud.cmd on
Windows), and gcloud never prompts: its one prompt here would offer to enable an API, which is a write.

ci-vars prints the `gh variable set` lines for the repository variables .github/workflows/documind-cd.yml reads, once
it has checked that the workflow reads exactly these four: GCP_PROJECT and GCP_REGION from the lane's confirmed inputs
(terraform/runbook-project.auto.tfvars.json, which infrastructure.py confirmed and saved when make plan ran),
WIF_PROVIDER and CICD_SERVICE_ACCOUNT from `terraform output -json` (wif.tf). A PROJECT or REGION the lane was not
planned with is refused: the Makefile's REGION defaults to us-central1, and a workflow told the wrong region builds its
image into a repository that does not exist. The lines name the repository wif.tf's condition trusts, and the dispatch
line names the one branch it trusts; any other repository or branch is refused at the workflow's auth step. GitHub
creates an environment the first time a job names it, with no protection rule, so a repository with no production
environment, or one with no required reviewer, would let promote move traffic with nobody approving: with gh
installed, ci-vars reads the environment and warns.

keys lists every service account in the project with its user-managed keys, and says where the project sits: under an
organization, org_policy.tf's enforce_no_sa_keys can forbid making keys; a personal account's project has no
organization, nothing can forbid them, and this check is the control.

Exit codes: 0 done (ci-vars may still warn); 1 keys found a user-managed key; 2 stopped: a tool, an input or a read
failed, and the message says which.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent                                   # the kit: deploy/ here, the repository root in the learner repo
WORKFLOW = KIT / ".github" / "workflows" / "documind-cd.yml"

# infrastructure.py owns the lane's confirmed inputs (the file, its reader, validate_trust): make plan wrote them, and
# ci-vars reads the same record rather than a second copy of the rules.
_spec = importlib.util.spec_from_file_location("infrastructure", HERE / "infrastructure.py")
infra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(infra)

# The repository variables documind-cd.yml reads, in the order ci-vars prints them.
CI_VARS = ("GCP_PROJECT", "GCP_REGION", "WIF_PROVIDER", "CICD_SERVICE_ACCOUNT")
# wif.tf's pool and provider ids, and sa.tf's pipeline account, as terraform output prints them.
WIF_PROVIDER = re.compile(r"projects/[0-9]+/locations/global/workloadIdentityPools/documind-github/providers/github-oidc")
CICD_ACCOUNT = re.compile(r"sa-documind-cicd@([a-z][a-z0-9-]{4,28}[a-z0-9])\.iam\.gserviceaccount\.com")
PROJECT_ID = re.compile(r"[a-z][a-z0-9-]{4,28}[a-z0-9]")
KEYS_FOUND, STOPPED = 1, 2
INSTALL = {"terraform": "install Terraform 1.9.0 or newer (lesson 0.2)",
           "gcloud": "install the Google Cloud CLI, or run this in Cloud Shell", "gh": "install the GitHub CLI"}
REVIEWERS = ("Settings > Environments > production > Required reviewers (on a private repository, required reviewers "
             "need a paid GitHub plan)")


class Stop(RuntimeError):
    """A precondition failed. The message says which, and the command exits 2."""


def count(n: int, thing: str) -> str:
    return f"{n} {thing}{'' if n == 1 else 's'}"


def cause(text: str) -> str:
    """The line of a tool's error output that names the cause: gcloud's ERROR line, terraform's Error line (out of its
    box), else the first line."""
    lines = [line.strip(" \t\u2502\u2577\u2575") for line in (text or "").splitlines()]
    lines = [line for line in lines if line]
    return next((line for line in lines if line.startswith(("ERROR:", "Error:", "error:"))),
                lines[0] if lines else "no error output")


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """One read-only call of terraform, gcloud or gh, with its output captured and never a prompt."""
    exe = shutil.which(argv[0])
    if not exe:
        raise Stop(f"{argv[0]} is not on PATH: {INSTALL.get(argv[0], 'install it')}")
    env = dict(os.environ, CLOUDSDK_CORE_DISABLE_PROMPTS="1", GH_PROMPT_DISABLED="1", GH_NO_UPDATE_NOTIFIER="1")
    try:
        return subprocess.run([exe, *argv[1:]], cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=300)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Stop(f"{argv[0]} {argv[1]} could not run: {e}") from e


def read_json(argv: list[str]):
    """A gcloud read as JSON, or a Stop naming the call and the line of gcloud's error that names the cause."""
    r = run(argv)
    what = " ".join(argv[:4]) if argv[1] == "iam" else " ".join(argv[:3])
    if r.returncode:
        raise Stop(f"{what} failed (exit {r.returncode}): {cause(r.stderr)}")
    try:
        return json.loads(r.stdout or "null")
    except ValueError:
        raise Stop(f"{what} did not return JSON") from None


# ---------------------------------------------------------------- ci-vars (lesson 11.1)

def workflow_vars(path: Path = WORKFLOW) -> list[str]:
    """Every repository variable the workflow reads: each vars.NAME inside a ${{ }} expression, sorted."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise Stop(f"cannot read the workflow {path}: {e}") from e
    return sorted({name for expr in re.findall(r"\$\{\{(.*?)\}\}", text)
                   for name in re.findall(r"\bvars\.([A-Za-z_][A-Za-z0-9_]*)", expr)})


def check_workflow(path: Path) -> None:
    found = workflow_vars(path)
    if found != sorted(CI_VARS):
        raise Stop(f"{path.name} reads {', '.join(found) or 'no repository variable'}, and ci-vars sets "
                   f"{', '.join(CI_VARS)}: change CI_VARS in commands/release.py with the workflow, and say where each "
                   "value comes from")


def lane_inputs(tf_dir: Path) -> dict:
    """The lane's confirmed inputs: its project and region, and the CI trust its WIF condition holds."""
    path = tf_dir / infra.INPUT_FILE
    if not path.is_file():
        raise Stop(f"no {infra.INPUT_FILE} in {tf_dir}. It is the lane's confirmed inputs, saved by make plan: run this "
                   "in the checkout that planned the lane, or first run python commands/infrastructure.py prepare "
                   "--project PROJECT --region REGION here, which reads the CI trust from the lane's state")
    saved = infra.read_json(path)
    trust = infra.validate_trust({key: str(saved.get(key, "")) for key in infra.TRUST})
    project, region = str(saved.get("project_id", "")), str(saved.get("region", ""))
    if not PROJECT_ID.fullmatch(project) or not region:
        raise Stop(f"{path} names no project or no region: run python commands/infrastructure.py prepare again")
    return {**trust, "project_id": project, "region": region}


def terraform_outputs(tf_dir: Path) -> dict:
    """name -> value of every output. -json prints sensitive outputs in clear (gateway_database_url), so its text is
    parsed here and never echoed, not even in an error."""
    r = run(["terraform", "output", "-json"], cwd=tf_dir)
    if r.returncode:
        raise Stop(f"terraform output failed in {tf_dir} (exit {r.returncode}): {cause(r.stderr)}. A checkout that "
                   "was never connected to the lane's state: make tf-backend PROJECT=<id> first")
    try:
        data = json.loads(r.stdout or "{}")
    except ValueError:
        raise Stop(f"terraform output -json in {tf_dir} did not return JSON") from None
    if not isinstance(data, dict):
        raise Stop(f"terraform output -json in {tf_dir} did not return an object")
    return {name: out.get("value") for name, out in data.items() if isinstance(out, dict)}


def ci_values(project: str, region: str, tf_dir: Path) -> tuple[dict, dict]:
    """(the four values by variable name, the lane's confirmed inputs), every source checked against the others."""
    lane = lane_inputs(tf_dir)
    if project and project != lane["project_id"]:
        raise Stop(f"PROJECT is {project}, but {tf_dir} is lane {lane['project_id']}'s ({infra.INPUT_FILE}): "
                   "run this in that lane's checkout, or with its project")
    if region and region != lane["region"]:
        raise Stop(f"REGION is {region}, but lane {lane['project_id']} was planned in {lane['region']} "
                   f"({infra.INPUT_FILE}), where its image repository and services are: make ci-vars "
                   f"PROJECT={lane['project_id']} REGION={lane['region']}")
    outputs = terraform_outputs(tf_dir)
    provider, account = outputs.get("wif_provider"), outputs.get("cicd_service_account")
    if not provider or not account:
        raise Stop("terraform output has no wif_provider or no cicd_service_account: the state this checkout reads "
                   "holds no CI pipeline. make up applies wif.tf and sa.tf; make tf-backend connects a checkout to "
                   "the lane's state")
    if not isinstance(provider, str) or not WIF_PROVIDER.fullmatch(provider):
        raise Stop(f"wif_provider is not wif.tf's provider (pool documind-github, provider github-oidc): {provider}")
    match = CICD_ACCOUNT.fullmatch(account) if isinstance(account, str) else None
    if not match:
        raise Stop(f"cicd_service_account is not sa.tf's sa-documind-cicd: {account}")
    if match[1] != lane["project_id"]:
        raise Stop(f"terraform output is project {match[1]}'s, but {infra.INPUT_FILE} is lane {lane['project_id']}'s: "
                   "this checkout's backend points at another lane's state")
    return {"GCP_PROJECT": lane["project_id"], "GCP_REGION": lane["region"], "WIF_PROVIDER": provider,
            "CICD_SERVICE_ACCOUNT": account}, lane


def production_environment(repo: str) -> tuple[str, str]:
    """('ok' | 'warn' | 'note', the line to print) for the repository's production environment, which promote names:
    one GET through gh, when gh is installed."""
    if not shutil.which("gh"):
        return "note", ("gh is not installed here, so the production environment was not read: check it has a "
                        "required reviewer, " + REVIEWERS)
    r = run(["gh", "api", f"repos/{repo}/environments/production"])
    if r.returncode:
        if "HTTP 404" in r.stderr or '"Not Found"' in r.stdout:
            return "warn", (f"{repo} has no production environment, or gh's account cannot see the repository. GitHub "
                            "creates the environment the first time a job names it, with no required reviewer, and "
                            "promote would then move traffic with nobody approving. Create it with a reviewer before "
                            "the first dispatch: " + REVIEWERS)
        return "warn", (f"could not read {repo}'s production environment ({cause(r.stderr)}): check by hand that it "
                        "has a required reviewer, " + REVIEWERS)
    try:
        rules = json.loads(r.stdout or "{}").get("protection_rules") or []
    except (ValueError, AttributeError):
        return "warn", f"gh did not return {repo}'s production environment as JSON: check it by hand, " + REVIEWERS
    reviewers = sum(len(rule.get("reviewers") or []) for rule in rules
                    if isinstance(rule, dict) and rule.get("type") == "required_reviewers")
    if not reviewers:
        return "warn", (f"{repo}'s production environment has no required reviewer, so promote would move traffic "
                        "with nobody approving. Add one: " + REVIEWERS)
    return "ok", f"production: {count(reviewers, 'required reviewer')}, so promote waits for a person"


def cmd_ci_vars(a) -> int:
    workflow = Path(a.workflow).expanduser().resolve()
    tf_dir = Path(a.terraform_dir).expanduser().resolve()
    check_workflow(workflow)
    values, lane = ci_values(a.project, a.region, tf_dir)
    repo, ref = lane["github_repository"], lane["deploy_ref"]
    q = shlex.quote
    print(f"# {workflow.name} reads {len(CI_VARS)} repository variables. Set them on {repo}, the repository wif.tf "
          "trusts:")
    for name in CI_VARS:
        print(f"gh variable set {name} --repo {q(repo)} --body {q(values[name])}")
    print(f"# The trust (wif.tf): {repo}, id {lane['github_repository_id']}, ref {ref}. A run from any other ref is "
          "refused at the auth step.")
    print("# Dispatch from that branch, on the candidate path - path=clouddeploy would replace documind-api's settings "
          "with run-service.yaml's:")
    print(f"#   gh workflow run {workflow.name} --repo {q(repo)} --ref {q(ref.removeprefix('refs/heads/'))} "
          "-f path=candidate")
    level, line = production_environment(repo)
    if level == "warn":
        sys.stdout.flush()
        print(f"WARNING: {line}", file=sys.stderr)
    else:
        print(f"# {line}")
    return 0


# ---------------------------------------------------------------- keys (lesson 11.1)

def parent_line(project: str, parent) -> str:
    if not isinstance(parent, dict) or not parent.get("type"):
        return (f"{project} has no parent: it is in no organization, so org_policy.tf's enforce_no_sa_keys cannot be "
                "applied and nothing stops a key being made; this check is the control")
    kind, ident = parent["type"], parent.get("id", "?")
    where = "" if kind == "organization" else ", inside an organization"
    return (f"{project} is in {kind} {ident}{where}: org_policy.tf's enforce_no_sa_keys can forbid making keys here, "
            "and an organization created on or after 3 May 2024 forbids it by default")


def user_keys(project: str, email: str) -> tuple[list | None, str]:
    """(the account's user-managed keys, '') or (None, why they could not be listed)."""
    try:
        r = run(["gcloud", "iam", "service-accounts", "keys", "list", f"--iam-account={email}", f"--project={project}",
                 "--managed-by=user", "--format=json"])
    except Stop as e:
        return None, str(e)
    if r.returncode:
        return None, cause(r.stderr)
    try:
        keys = json.loads(r.stdout or "[]")
    except ValueError:
        return None, "gcloud did not return JSON"
    return ([k for k in keys if isinstance(k, dict)], "") if isinstance(keys, list) else (None, "not a list")


def key_line(key: dict) -> str:
    expires = str(key.get("validBeforeTime") or "")
    when = "never expires" if not expires or expires.startswith("9999-") else f"expires {expires}"
    return (f"       key {str(key.get('name', '?')).rsplit('/', 1)[-1]}  created {key.get('validAfterTime', '?')}  "
            f"{when}" + ("  (disabled, not deleted)" if key.get("disabled") else ""))


def cmd_keys(a) -> int:
    project = a.project
    if not PROJECT_ID.fullmatch(project or ""):
        raise Stop("pass --project with the lane's project id (or PROJECT in the environment)")
    info = read_json(["gcloud", "projects", "describe", project, "--format=json"])
    if not isinstance(info, dict) or info.get("projectId") != project:
        raise Stop(f"gcloud projects describe did not return project {project}")
    print(parent_line(project, info.get("parent")))
    accounts = read_json(["gcloud", "iam", "service-accounts", "list", f"--project={project}", "--format=json"])
    if not isinstance(accounts, list):
        raise Stop("gcloud iam service-accounts list did not return a list")
    emails = sorted({acct["email"] for acct in accounts if isinstance(acct, dict) and acct.get("email")})
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        listed = list(pool.map(lambda email: user_keys(project, email), emails))
    print(f"{count(len(emails), 'service account')}, and the user-managed keys of each:")
    found, holders, unread = 0, 0, []
    for email, (keys, why) in zip(emails, listed):
        if keys is None:
            unread.append(email)
            print(f"  ?  {email}  could not list its keys: {why}")
            continue
        print(f"  {len(keys)}  {email}")
        for key in keys:
            print(key_line(key))
        found, holders = found + len(keys), holders + bool(keys)
    if found:
        print(f"{count(found, 'user-managed key')} on {count(holders, 'account')}"
              + (f" ({count(len(unread), 'more account')} not read)" if unread else "")
              + ". A key is a credential that does not expire and works wherever it is copied: delete each one "
              "nothing uses")
        print(f"  gcloud iam service-accounts keys delete KEY_ID --iam-account=ACCOUNT --project={project}")
        return KEYS_FOUND
    if unread:
        raise Stop(f"the keys of {count(len(unread), 'account')} could not be listed, so this is no proof of zero "
                   f"keys: {', '.join(unread)}")
    print(f"no user-managed keys: no key file can sign in as any account of {project}")
    return 0


# ---------------------------------------------------------------- the command line

def build_parser() -> argparse.ArgumentParser:
    lines = __doc__.splitlines()
    ap = argparse.ArgumentParser(prog="release.py", description=lines[0], epilog="\n".join(lines[2:]),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    lane = argparse.ArgumentParser(add_help=False)
    lane.add_argument("--project", default=os.environ.get("PROJECT") or "", help="the lane's project id (PROJECT)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("ci-vars", parents=[lane], help="the gh variable set lines documind-cd.yml needs (make ci-vars)")
    c.add_argument("--region", default=os.environ.get("REGION") or "",
                   help="the lane's region (REGION); empty takes the one the lane was planned in")
    c.add_argument("--terraform-dir", default=str(KIT / "terraform"), help="the lane's terraform/ (default: the kit's)")
    c.add_argument("--workflow", default=str(WORKFLOW), help="the CD workflow (default: the kit's documind-cd.yml)")
    c.set_defaults(fn=cmd_ci_vars)
    k = sub.add_parser("keys", parents=[lane], help="every service account's user-managed keys (make keys-check)")
    k.set_defaults(fn=cmd_keys)
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    try:
        return int(a.fn(a) or 0)
    except (Stop, infra.Stop) as e:
        sys.stdout.flush()
        print(f"STOP: {e}", file=sys.stderr)
        return STOPPED


if __name__ == "__main__":
    sys.exit(main())
