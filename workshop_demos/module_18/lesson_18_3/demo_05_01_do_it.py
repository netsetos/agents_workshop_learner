"""Lesson 18.3 / s5: The lane's cluster, inspected

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (read-only: describes the lane's cluster, looks for the vLLM service and image)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: documind-autopilot: STANDARD, a regional control plane in asia-south1, on documind-vpc, RUNNING
  node pool documind-lab: 1 x e2-standard-2 in asia-south1-a, 30 GB pd-standard, GPU: none
  what it bills while it exists: $0.10 an hour for the control plane (the free tier covers only zonal and Autopilot clusters) + $0.0805 for the node = $0.1805 an hour, Rs 15.34; Rs 11,199 for a 730-hour month, plus the disk
documind-vllm on Cloud Run (us-central1): not deployed
the gemma-vllm image in asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind: not built

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.3-vllm-gke/Netsetos_GCP_Capstone_18.3_VLLM_GKE_WIX.html#L649

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
