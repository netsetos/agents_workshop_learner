"""Lesson 3.3 / s4: The call: 768 numbers under the document task type

Summary and purpose:
This cell costs money, a very small amount: two calls on a 234-character clause, about a tenth of a paisa. It reads NP-03's text and stored vector off the lane, embeds the same text under the document profile with the worker's exact settings, and compares by cosine. Then it embeds the same text under the query profile and compares again.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash; two paid calls)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_call_it_three_reads_of_one_pair
Expected observation: lane vector: 768 numbers; first three [0.0213, -0.0117, 0.0388]
same text, RETRIEVAL_DOCUMENT: cosine to the lane's vector 1.0
same text, RETRIEVAL_QUERY:    cosine to the lane's vector 0.9xxx

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L531

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: embed one clause yourself, both ways at this checkpoint.

    This cell costs money, a very small amount: two calls on a 234-character clause, about a tenth of a paisa. It reads NP-03's text and stored vector off the lane, embeds the same text under the document profile with the worker's exact settings, and compares by cosine. Then it embeds the same text under the query profile and compares again.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash; two paid calls).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, math, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    from google import genai
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    row = next(db.collection("chunks").where("tenant_id", "==", "acme")
                 .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md")
                 .where("current", "==", True).where("locator", "==", "NP-03").stream()).to_dict()
    lane = list(row["embedding"])
    client = genai.Client(enterprise=True, project=PROJECT, location="us-central1")   # embeddings are regional
    def embed(text, task):
        r = client.models.embed_content(model="text-embedding-005", contents=[text],
                                        config={"output_dimensionality": 768, "task_type": task})
        return list(r.embeddings[0].values)
    def cosine(a, b):
        return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    doc, qry = embed(row["text"], "RETRIEVAL_DOCUMENT"), embed(row["text"], "RETRIEVAL_QUERY")
    print("lane vector:", len(lane), "numbers; first three", [round(v, 4) for v in lane[:3]])
    print("same text, RETRIEVAL_DOCUMENT: cosine to the lane's vector", round(cosine(doc, lane), 4))
    print("same text, RETRIEVAL_QUERY:    cosine to the lane's vector", round(cosine(qry, lane), 4))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
