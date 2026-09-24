"""Read a serving revision as JSON; never silently use the newest candidate."""
from dataclasses import dataclass
import json
from .auth import gcloud

PUBLIC_KEYS = {
    "SELF_URL", "SEMANTIC_CACHE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY",
    "RETRIEVAL_MODE", "MANAGED_MIRROR", "RAG_LOCATION", "SEARCH_LOCATION",
    "AUDIT_BUCKET", "RETENTION_DAYS", "EMBEDDING_MODEL", "REGION",
    "VECTOR_INDEX_ENDPOINT", "VECTOR_DEPLOYED_INDEX_ID",
}


@dataclass(frozen=True)
class ServingConfig:
    service: str
    revision: str
    service_url: str
    environment: dict


def select_revision(service, override=""):
    active = {item.get("revisionName") for item in service.get("status", {}).get("traffic", [])
              if item.get("percent", 0) > 0}
    if len(active) != 1 or None in active:
        raise RuntimeError("This pilot requires one serving revision. Service traffic is split or absent.")
    serving = active.pop()
    if override and override != serving:
        raise RuntimeError("The pinned revision is not the sole serving revision. Refresh settings.local.json.")
    return serving


def read_serving(config, service_name, revision_override=""):
    flags = (f"--project={config.project}", f"--region={config.cloud_run_region}", "--format=json")
    service = json.loads(gcloud("run", "services", "describe", service_name, *flags))
    revision = select_revision(service, revision_override)
    if not revision.startswith(service_name + "-"):
        raise ValueError("Selected revision does not belong to the requested service.")
    document = json.loads(gcloud("run", "revisions", "describe", revision, *flags))
    containers = document.get("spec", {}).get("containers", [])
    if len(containers) != 1:
        raise RuntimeError("This pilot expects a single application container.")
    env = {}
    for row in containers[0].get("env", []):
        key = row["name"].upper()
        if key not in PUBLIC_KEYS:
            continue
        if "value" not in row:
            raise RuntimeError(f"{key} is a referenced value; configure this pilot for explicit settings before continuing.")
        env[key] = row["value"]
    return ServingConfig(service_name, revision, service.get("status", {}).get("url", ""), env)
