"""Lesson 18.3 / s4: The manifest, read

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads the manifest and the image it runs; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: Deployment documind-vllm: 1 replica, and no autoscaler
  its node: nodeSelector cloud.google.com/gke-accelerator=nvidia-l4, so Autopilot provisions an L4 node for the pod
  image: ${IMAGE}, which make gke-up fills in: asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/gemma-vllm:latest
  limits: 1 GPU, 6 vCPU, 24Gi (requests default to the limits)
  env: HF_HUB_OFFLINE=1
  startup probe: GET /health every 10 s, 60 failures allowed: 600 s to load
  args: --model=google/gemma-3-4b-it --dtype=bfloat16 --gpu-memory-utilization=0.90 --max-model-len=4096 --port=8080
Service documind-vllm: ClusterIP (no type named, so the default), port 80 to 8080: no address outside the cluster
the image it runs: ENTRYPOINT [], CMD python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1 --timeout-keep-alive 120
  the manifest sets args and no command, and the ENTRYPOINT is empty: the container r

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.3-vllm-gke/Netsetos_GCP_Capstone_18.3_VLLM_GKE_WIX.html#L577

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
