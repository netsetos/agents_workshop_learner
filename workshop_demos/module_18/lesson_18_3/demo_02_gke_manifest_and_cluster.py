"""Lesson 18.3: demo 02 gke manifest and cluster

Inspect the alternative manifest and the lane's actual cluster state.

Run order inside this file:
1. Do it (source window 14)
2. Do it (source window 17)
3. Do it (source window 19)

Prerequisites: demo_01_vllm_service.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the manifest and the image it runs; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, re
    rd = lambda p: open(p, encoding="utf-8").read()
    man, dock, main, mk = rd("gke/vllm-deployment.yaml"), rd("services/gemma-vllm/Dockerfile"), rd("services/gemma-vllm/main.py"), rd("Makefile")
    dep, svc = man.split("\n---\n", 1)
    val = lambda doc, key: re.search(r"^\s*" + re.escape(key) + r":\s*(.+)$", doc, re.M).group(1).strip().strip('"')
    args = re.findall(r"^\s+- (--\S+)$", dep, re.M)
    env = dict(re.findall(r'- name: (\S+)\n\s+value: "?([^"\n]+)"?', dep))
    sel = re.search(r"nodeSelector:\n\s+(\S+): (\S+)", dep).groups()
    repo = re.search(r"^IMAGE_REPO = (\S+)", mk, re.M).group(1)
    repo = repo.replace("$(REGION)", os.environ["REGION"]).replace("$(PROJECT)", os.environ["PROJECT"])
    sp = dep.split("startupProbe:", 1)[1].split("readinessProbe:", 1)[0]
    path = re.search(r"path: ([^,\s]+)", sp).group(1)
    fails, period = (int(re.search(k + r": (\d+)", sp).group(1)) for k in ("failureThreshold", "periodSeconds"))
    print(f"Deployment {val(dep, 'name')}: {val(dep, 'replicas')} replica, and no autoscaler")
    print(f"  its node: nodeSelector {sel[0]}={sel[1]}, so Autopilot provisions an L4 node for the pod")
    print(f"  image: {val(dep, 'image')}, which make gke-up fills in: {repo}/gemma-vllm:latest")
    print(f"  limits: {val(dep, 'nvidia.com/gpu')} GPU, {val(dep, 'cpu')} vCPU, {val(dep, 'memory')} (requests default to the limits)")
    print("  env: " + ", ".join(f"{k}={v}" for k, v in env.items()))
    print(f"  startup probe: GET {path} every {period} s, {fails} failures allowed: {fails * period} s to load")
    print("  args: " + " ".join(args))
    kind = re.search(r"^\s*type: (\S+)", svc, re.M)
    ports = re.search(r"port: (\d+)\n\s+targetPort: (\d+)", svc).groups()
    print(f"Service {val(svc, 'name')}: {kind.group(1) if kind else 'ClusterIP (no type named, so the default)'}, port {ports[0]} to {ports[1]}: "
          "no address outside the cluster")
    entry = re.search(r"^ENTRYPOINT (.+)$", dock, re.M).group(1).strip()
    cmd = " ".join(re.findall(r'"([^"]+)"', re.search(r"CMD \[(.*?)\]", dock, re.S).group(1)))
    print(f"the image it runs: ENTRYPOINT {entry}, CMD {cmd}")
    if entry == "[]" and args and not re.search(r"^\s+command:", dep, re.M):
        print(f"  the manifest sets args and no command, and the ENTRYPOINT is empty: the container runs {args[0]!r} as its program")
    reads = sorted(set(re.findall(r'os.getenv\("([A-Z_]+)"', main)))
    print(f"  main.py takes its model from the environment ({', '.join(reads)}), and reads none of those args")
    print(f"  the image holds no weights (step 3), and HF_HUB_OFFLINE={env['HF_HUB_OFFLINE']} forbids the download")
    print("verdict: as written, this pod cannot start")

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (read-only: describes the lane's cluster, looks for the vLLM service and image).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    P, R = os.environ["PROJECT"], os.environ["REGION"]
    
    
    def gc(*args):
        r = subprocess.run(["gcloud", *args, "--project", P, "--format=json"], capture_output=True, text=True)
        return json.loads(r.stdout) if r.returncode == 0 else None
    
    
    c = gc("container", "clusters", "describe", "documind-autopilot", "--region", R)
    auto = (c.get("autopilot") or {}).get("enabled", False)
    plane = "regional" if c["location"] == R else "zonal"
    print(f"documind-autopilot: {'AUTOPILOT' if auto else 'STANDARD'}, a {plane} control plane in {c['location']}, on {c['network']}, {c['status']}")
    for pool in c.get("nodePools", []):
        cfg = pool["config"]
        print(f"  node pool {pool['name']}: {pool['initialNodeCount']} x {cfg['machineType']} in {', '.join(pool['locations'])}, "
              f"{cfg['diskSizeGb']} GB {cfg['diskType']}, GPU: {cfg.get('accelerators') or 'none'}")
    E2 = {"us-central1": 0.06701142, "asia-south1": 0.08048436}       # e2-standard-2, USD an hour (Compute Engine pricing, 24 September 2026)
    if not auto and plane == "regional" and R in E2:
        hour = 0.10 + E2[R] * c["currentNodeCount"]
        print(f"  what it bills while it exists: $0.10 an hour for the control plane (the free tier covers only zonal and Autopilot "
              f"clusters) + ${E2[R] * c['currentNodeCount']:.4f} for the node = ${hour:.4f} an hour, Rs {hour * 85:.2f}; "
              f"Rs {hour * 85 * 730:,.0f} for a 730-hour month, plus the disk")
    v = gc("run", "services", "describe", "documind-vllm", "--region", "us-central1")
    print("documind-vllm on Cloud Run (us-central1): " + ("deployed" if v else "not deployed"))
    images = gc("artifacts", "docker", "images", "list", f"{R}-docker.pkg.dev/{P}/documind/gemma-vllm")
    print(f"the gemma-vllm image in {R}-docker.pkg.dev/{P}/documind: " + (f"{len(images)} version(s)" if images else "not built"))

def step_03_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (it stops before changing anything on a Standard lab).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.gates import expect_guard
    expect_guard(session, ["make", "gke-up", "PROJECT=" + session.config.project],
                 stop="STOP: the Standard CPU lab cannot run the L4 GPU lesson")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_14', step_01_example),
        ('source_17', step_02_example),
        ('source_19', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
