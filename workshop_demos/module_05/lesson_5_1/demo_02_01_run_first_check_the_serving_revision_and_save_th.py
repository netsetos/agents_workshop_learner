"""Lesson 5.1 / s2: Before the demo: verify the index, then select the tenant backend

Summary and purpose:
Run in $DEMO_ROOT. This reads the single revision receiving traffic, checks that its deployed ID exists, saves only the relevant settings under operator-evidence/lesson51/, and then selects vector for Acme. Empty optional settings take their code defaults. It stops before any embedding or tenant change if the deployment is invalid. A split-traffic service needs a chosen revision before this single-revision demonstration can proceed.

HTML instruction: bash — run before step 3; reads configuration and saves/sets the Acme pin
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L385

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Run first: check the serving revision and save the original pin at this checkpoint.

    Run in $DEMO_ROOT. This reads the single revision receiving traffic, checks that its deployed ID exists, saves only the relevant settings under operator-evidence/lesson51/, and then selects vector for Acme. Empty optional settings take their code defaults. It stops before any embedding or tenant change if the deployment is invalid. A split-traffic service needs a chosen revision before this single-revision demonstration can proceed.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run before step 3; reads configuration and saves/sets the Acme pin.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess, warnings
    from pathlib import Path
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import aiplatform
    from shared.tenancy import backend_for, set_backend
    
    project, region = os.environ["PROJECT"], os.environ["REGION"]
    flags = [f"--project={project}", f"--region={region}", "--format=json"]
    def read_run(kind, name):
        return json.loads(subprocess.run(
            ["gcloud", "run", kind, "describe", name] + flags,
            check=True, capture_output=True, text=True).stdout)
    
    service = read_run("services", "documind-api")
    if os.environ["API"].rstrip("/") != service["status"]["url"].rstrip("/"):
        raise SystemExit("STOP: API must be this service's URL for this demo.")
    traffic = [t for t in service["status"].get("traffic", []) if t.get("percent", 0) > 0]
    if len(traffic) != 1 or traffic[0].get("percent") != 100:
        raise SystemExit("STOP: inspect split traffic; this demo expects one serving revision.")
    revision = traffic[0]["revisionName"]
    env = {e["name"]: e.get("value", "") for e in
           read_run("revisions", revision)["spec"]["containers"][0].get("env", [])}
    cfg = {"project": project, "api": os.environ["API"], "revision": revision,
           "endpoint": env.get("VECTOR_INDEX_ENDPOINT", ""),
           "deployed_id": env.get("VECTOR_DEPLOYED_INDEX_ID", ""),
           "mode": env.get("RETRIEVAL_MODE") or "dense",
           "current_only": env.get("RETRIEVAL_CURRENT_ONLY") or "off",
           "top_k": int(env.get("TOP_K_RETRIEVE") or 20),
           "embed_model": env.get("EMBEDDING_MODEL") or "text-embedding-005",
           "graph": env.get("RETRIEVAL_GRAPH") or "off"}
    print(json.dumps(cfg, indent=2))
    if not cfg["endpoint"] or not cfg["deployed_id"]:
        raise SystemExit("STOP: the serving revision has no complete Vector Search configuration.")
    if cfg["current_only"] not in ("on", "off") or cfg["top_k"] < 1:
        raise SystemExit("STOP: invalid current-only or pool-size setting.")
    aiplatform.init(project=project, location=region)
    endpoint = aiplatform.MatchingEngineIndexEndpoint(cfg["endpoint"])
    deployed = [d.id for d in endpoint.deployed_indexes]
    print("Actual deployed IDs:", deployed)
    if cfg["deployed_id"] not in deployed:
        raise SystemExit("STOP: API deployed ID is absent. Use the repair note below, then rerun this block.")
    
    os.environ["GOOGLE_CLOUD_PROJECT"] = project
    evidence = Path("operator-evidence/lesson51")
    evidence.mkdir(parents=True, exist_ok=True)
    backup = evidence / "pin-before.json"
    current = backend_for("acme") or "default"
    if backup.exists():
        before = json.loads(backup.read_text())
        if before["project"] != project or current not in (before["backend"], "vector"):
            raise SystemExit("STOP: saved pin belongs to a different project or the pin changed independently.")
    else:
        before = {"project": project, "backend": current}
        with backup.open("x") as f:
            json.dump(before, f)
    (evidence / "settings.json").write_text(json.dumps(cfg, indent=2))
    print("Original Acme pin:", before["backend"])
    print("Acme demo pin:", set_backend("acme", "vector"))
    print("PASS: index configuration verified. Allow up to 60 seconds for the API's tenant-setting cache.")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
