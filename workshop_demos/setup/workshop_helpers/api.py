"""Authenticated diagnostic API calls retaining stages, cache status and citations."""
import json
import urllib.error
import urllib.request
from .auth import identity_token
from .discovery import read_serving


class ApiClient:
    def __init__(self, config):
        self.config = config
        self.serving = read_serving(config, config.api_service, config.api_revision)
        self.audience = config.api_audience or self.serving.environment.get("SELF_URL") or self.serving.service_url
        self.url = (config.api_base_url or self.audience).rstrip("/")
        if not self.url.startswith("https://") or not self.audience:
            raise RuntimeError("Could not resolve the API URL and token audience.")

    def request(self, path, body=None, timeout=180):
        token = identity_token(self.config, self.audience)
        request = urllib.request.Request(
            self.url + path, method="POST" if body is not None else "GET",
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1500]
            raise RuntimeError(f"API {path}: HTTP {exc.code}: {detail}") from exc

    def check_fresh_answers(self):
        version = self.request("/version", timeout=30)
        if version.get("semantic_cache") != "off":
            raise RuntimeError(
                "This lifecycle answer demo requires the API's SEMANTIC_CACHE=off. "
                "Configure a serving demo revision with the cache off, or set VERIFY_API=False "
                "in demo_03 to demonstrate the storage/ledger lifecycle only. No deployment was changed."
            )
        return version

    def query(self, question, top_k=5):
        answer = self.request("/v1/query", {"query": question, "tenant_id": self.config.tenant_id,
                                           "stream": False, "top_k": top_k})
        if answer.get("cache_hit") != "none":
            raise RuntimeError("The API returned a cached or unclassified answer; it cannot prove this lifecycle transition.")
        return answer
