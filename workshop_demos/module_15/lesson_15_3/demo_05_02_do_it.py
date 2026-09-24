"""Lesson 15.3 / s5: Ask the stores, and find who found the cited chunk

Summary and purpose:
The answer's citation carries no found_by, because the kit's Citation has no such field. The stamp is on the chunk in the pool. This cell asks the API again, then runs the kit's own retrieve() in your shell with backend rag_engine, the call the API made, and looks for the cited chunk in that pool.

HTML instruction: bash — run in the operator shell, in the kit (the same question to the API, then through the kit's own retrieve())
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: the API: retrieval_backend rag_engine, 14 of the pool's 17 chunks from the store
the same question through the kit's retrieve(), backend rag_engine: 17 chunks
  found_by rag_engine    14   for example acme:acme_497809ff...#rag-c31c1f459b60
  found_by (none)         3   for example acme:0994e77d...#0
the chunk the answer cites: acme:acme_497809ff...#rag-c31c1f459b60
  found_by rag_engine, score 0.706 (1 minus its distance), from hr_policy_2026.md

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L695

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    The answer's citation carries no found_by, because the kit's Citation has no such field. The stamp is on the chunk in the pool. This cell asks the API again, then runs the kit's own retrieve() in your shell with backend rag_engine, the call the API made, and looks for the cited chunk in that pool.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same question to the API, then through the kit's own retrieve()).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, re, subprocess, sys, urllib.request
    P, API = os.environ["PROJECT"], os.environ["API"]
    os.environ["GOOGLE_CLOUD_PROJECT"] = P                  # the kit's settings, read as the API reads them
    sys.path[:0] = [".", "services/rag-api"]
    Q = "How long is the notice period for a confirmed employee?"
    short = lambda cid: re.sub(r"([0-9a-f]{8})[0-9a-f]{56}", r"\1...", cid)
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                         capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(API + "/v1/query", data=json.dumps({"query": Q, "tenant_id": "acme"}).encode(),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    a = json.load(urllib.request.urlopen(req, timeout=180))
    s = a["stages"]
    print(f"the API: retrieval_backend {s['retrieval_backend']}, {s['managed_chunks']} of the pool's {s['pool']} chunks from the store")
    import retriever                                        # the kit's retrieval stage, run in this shell with your credentials
    pool = retriever.retrieve(Q, "acme", 5, backend="rag_engine")
    kinds = {}
    for c in pool:
        kinds.setdefault(c.get("found_by"), []).append(c)
    print(f"the same question through the kit's retrieve(), backend rag_engine: {len(pool)} chunks")
    for k, v in kinds.items():
        print(f"  found_by {k or '(none)':13} {len(v):2}   for example {short(v[0]['id'])}")
    by_id = {c["id"]: c for c in pool}
    for c in a["citations"]:
        hit = by_id.get(c["chunk_id"])
        print(f"the chunk the answer cites: {short(c['chunk_id'])}")
        if hit:
            print(f"  found_by {hit['found_by']}, score {hit['score']:.3f} (1 minus its distance), from {hit['source_uri'].rsplit('/', 1)[-1]}")
        else:
            print("  not in this pool: ask again (the store answers the same text for the same question)")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
