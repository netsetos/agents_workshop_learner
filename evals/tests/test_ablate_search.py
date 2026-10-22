"""Offline check for the vertex_search arm against a standard-edition data store (22 October 2026).

The arm asked each search for extractive segments, an Enterprise feature. A standard-edition store refuses the whole
request (400 FailedPrecondition, "Cannot use enterprise edition features"), and its snippets stop short of the figure a
question asks for. So the store ranks the tenant's documents, and the passages are the kit's own rows of those
versions: the dense rung's nearest, three times k deep, kept when the store ranked their version - as
retriever._search_retrieve() serves them. discoveryengine is a stand-in here: no Google packages or network.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

EVALS = Path(__file__).resolve().parents[1]


def load_ablate():
    spec = importlib.util.spec_from_file_location("ablate_search_under_test", EVALS / "ablate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_discoveryengine(asked, ranked):
    class SearchServiceClient:
        def search(self, request):
            asked.append(request)
            return [types.SimpleNamespace(document=types.SimpleNamespace(id=i)) for i in ranked]

    class SearchRequest(types.SimpleNamespace):
        pass

    de = types.ModuleType("google.cloud.discoveryengine_v1")
    de.SearchServiceClient, de.SearchRequest = SearchServiceClient, SearchRequest
    return de


class TheStoreRanksTheKitsRowsAnswer(unittest.TestCase):
    def test_the_kits_nearest_rows_of_the_ranked_versions(self):
        ablate, asked = load_ablate(), []
        google = sys.modules.get("google") or types.ModuleType("google")
        cloud = sys.modules.get("google.cloud") or types.ModuleType("google.cloud")
        google.cloud = cloud
        de = fake_discoveryengine(asked, ["zeta_hb", "zeta_law", ""])
        rows = [{"chunk_id": "zeta:hb#3", "text": "NP-03: 30 days", "source_uri": "gs://u/zeta/hb.md", "doc_key": "zeta_hb"},
                {"chunk_id": "zeta:old#1", "text": "NP-03: 45 days", "source_uri": "gs://u/zeta/old.md", "doc_key": "zeta_old"},
                {"chunk_id": "zeta:law#9", "text": "one month's notice", "source_uri": "gs://u/zeta/law.md", "doc_key": "zeta_law"},
                {"chunk_id": "zeta:hb#4", "text": "PB-02: 15 days", "source_uri": "gs://u/zeta/hb.md", "doc_key": "zeta_hb"}]
        dense_asked = []
        with patch.dict(sys.modules, {"google": google, "google.cloud": cloud, "google.cloud.discoveryengine_v1": de}), \
                patch.object(cloud, "discoveryengine_v1", de, create=True):
            lane = ablate.Lane.__new__(ablate.Lane)              # no clients: vertex_search makes its own
            lane.project = "demo"
            lane.dense = lambda question, tenant, k: dense_asked.append((question, tenant, k)) or list(rows)
            got = lane.vertex_search("notice period for a confirmed employee?", "zeta", 2)
        self.assertEqual([c["chunk_id"] for c in got], ["zeta:hb#3", "zeta:law#9"])     # the old version is not ranked; cut to k
        self.assertEqual(dense_asked, [("notice period for a confirmed employee?", "zeta", 6)])
        request = asked[0]
        self.assertEqual(request.serving_config, "projects/demo/locations/global/collections/default_collection"
                                                 "/dataStores/documind-zeta/servingConfigs/default_search")
        self.assertEqual(request.page_size, 2)
        self.assertFalse(hasattr(request, "content_search_spec"), "no text is asked of a standard-edition store")


if __name__ == "__main__":
    unittest.main()
