"""Offline check for the vertex_search arm against a standard-edition data store (22 October 2026).

The arm asked each search for extractive segments, an Enterprise feature. A standard-edition store refuses the whole
request (400 FailedPrecondition, "Cannot use enterprise edition features"), so 7.4's arm failed on every row while the
API, asking the same way, fell back to the Firestore rung on every zeta query. The arm now asks once, then for
snippets alone, and unescapes them as text. discoveryengine is a stand-in here: no Google packages or network.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

EVALS = Path(__file__).resolve().parents[1]
REFUSAL = ("400 Cannot use enterprise edition features (website search, multi-modal search, extractive "
           "answers/segments, etc.) in a standard edition search engine.")


def load_ablate():
    spec = importlib.util.spec_from_file_location("ablate_search_under_test", EVALS / "ablate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Spec(types.SimpleNamespace):
    """ContentSearchSpec and its parts: keyword fields, settable afterwards as the code sets extractive_content_spec."""


def fake_discoveryengine(asked):
    class SearchServiceClient:
        def search(self, request):
            asked.append(request.content_search_spec)
            if getattr(request.content_search_spec, "extractive_content_spec", None) is not None:
                raise RuntimeError(REFUSAL)
            doc = types.SimpleNamespace(id="zeta_hb", derived={"snippets": [
                {"snippet": "A <b>confirmed</b> employee&#39;s notice is 30 days."}]})
            return [types.SimpleNamespace(document=doc)]

    class ContentSearchSpec(Spec):
        SnippetSpec = ExtractiveContentSpec = Spec

    class SearchRequest(Spec):
        pass

    SearchRequest.ContentSearchSpec = ContentSearchSpec
    de = types.ModuleType("google.cloud.discoveryengine_v1")
    de.SearchServiceClient, de.SearchRequest = SearchServiceClient, SearchRequest
    de.Document = types.SimpleNamespace(to_dict=lambda d: {"derived_struct_data": d.derived})
    return de


class SnippetsAfterARefusal(unittest.TestCase):
    def test_the_arm_asks_again_for_snippets_and_unescapes_them(self):
        ablate, asked = load_ablate(), []
        google = sys.modules.get("google") or types.ModuleType("google")
        cloud = sys.modules.get("google.cloud") or types.ModuleType("google.cloud")
        google.cloud = cloud
        de = fake_discoveryengine(asked)
        with patch.dict(sys.modules, {"google": google, "google.cloud": cloud, "google.cloud.discoveryengine_v1": de}), \
                patch.object(cloud, "discoveryengine_v1", de, create=True):
            lane = ablate.Lane.__new__(ablate.Lane)              # no clients: vertex_search makes its own
            lane.project, lane.segments_refused = "demo", False
            lane.source_of = lambda tenant, key: f"gs://demo-uploads/{tenant}/handbook.md"
            first = lane.vertex_search("notice period for a confirmed employee?", "zeta", 5)
            second = lane.vertex_search("earned leave?", "zeta", 5)
        self.assertEqual(first, [{"chunk_id": "zeta:zeta_hb#vs-0", "text": "A confirmed employee's notice is 30 days.",
                                  "source_uri": "gs://demo-uploads/zeta/handbook.md"}])
        self.assertTrue(lane.segments_refused)
        self.assertEqual(len(second), 1)
        # one refused request with segments, then snippets alone for the retry and every later search
        self.assertEqual([getattr(s, "extractive_content_spec", None) is not None for s in asked], [True, False, False])


if __name__ == "__main__":
    unittest.main()
