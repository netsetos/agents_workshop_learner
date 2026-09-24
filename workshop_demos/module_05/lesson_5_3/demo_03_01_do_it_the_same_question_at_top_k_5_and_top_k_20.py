"""Lesson 5.3 / s3: One answer, read end to end: the citations, their scores, the stages

Summary and purpose:
The cell asks the notice-period question twice and prints, for each answer, the stages block on one line and every citation with its score, its chunk position, its source and the start of its quote. The second answer offers the model twenty chunks instead of five.

HTML instruction: bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: top_k 5: pool 20 | from the index 20 | retrieve 6xx + rerank 3xx + generate 17xx ms of 28xx | rerank_fallback 0 | cache_hit none
   3 citations: the sources the model used, in the order it used them; [N] in the answer is the packed position
   [1] score 0.9xxx  #  1  hr_policy_2026.md          p.-  'NP-03 ...'
   [2] score 0.8xxx  #  4  hr_policy_2026.md          p.-  '...'
   [3] score 0.6xxx  #  2  hr_policy_2026.md          p.-  '...'
   sorted by score, the ranker's order among them: ['#1', '#4', '#2']

top_k 20: pool 20 | from the index 20 | retrieve 6xx + rerank 3xx + generate 3xxx ms of 4xxx | rerank_fallback 0 | cache_hit none
   4 citations: ...
   sorted by score, the ranker's order among them: ['#1', '#4', '#2', '#7']

saved /tmp/ans53_5.json and /tmp/ans53_20.json for steps 4, 7 and 8

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L462

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the same question at top_k 5 and top_k 20 at this checkpoint.

    The cell asks the notice-period question twice and prints, for each answer, the stages block on one line and every citation with its score, its chunk position, its source and the start of its quote. The second answer offers the model twenty chunks instead of five.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, subprocess, urllib.request
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = os.environ.get("Q", "What is the notice period for a confirmed E3?")
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"],
                         capture_output=True, text=True, check=True).stdout.strip()
    def ask(top_k):
        req = urllib.request.Request(f"{API}/v1/query", method="POST", data=json.dumps({"query": Q, "tenant_id": "acme", "stream": False, "top_k": top_k}).encode(),
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    for k in (5, 20):
        j = ask(k); s = j["stages"]
        json.dump(j, open(f"/tmp/ans53_{k}.json", "w"))
        print(f"\ntop_k {k}: pool {s['pool']} | from the index {s['vector_chunks']} | retrieve {s['retrieve_ms']} + rerank {s['rerank_ms']} + generate {s['generate_ms']} ms of {j['latency_ms']} | rerank_fallback {s.get('rerank_fallback', 0)} | cache_hit {j['cache_hit']}")
        print(f"   {len(j['citations'])} citations: the sources the model used, in the order it used them; [N] in the answer is the packed position")
        for i, c in enumerate(j["citations"], 1):
            print(f"   [{i}] score {c['score']:.4f}  #{c['chunk_id'].rsplit('#', 1)[1]:>3}  {c['source_uri'].split('/')[-1][:26]:26} p.{c.get('page') or '-'}  {c['quote'][:44]!r}")
        print("   sorted by score, the ranker's order among them:", [f"#{c['chunk_id'].rsplit('#', 1)[1]}" for c in sorted(j["citations"], key=lambda c: -c["score"])])
    print("\nsaved /tmp/ans53_5.json and /tmp/ans53_20.json for steps 4, 7 and 8")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
