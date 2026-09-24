"""Lesson 6.2 / s4: One answer from the lane, field by field, with every quote checked against its row

Summary and purpose:
Do it: one question, two halves, three rows

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question and three Firestore reads, a rupee)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_six_drafts_one_resolution_two_refusals
Expected observation: the contract: {"answer": "A confirmed employee in grade E3 must serve a notice period of ... [1]...", "citations": "3 citations", "confidence": "high", "answerable": true}
the envelope: {'model': 'gemini-3.6-flash', 'backend': 'vertex', 'tokens_in': 1xxx, 'tokens_out': 4xx, 'cached_tokens': 0, 'cost_usd': 0.00xxxx, 'latency_ms': 2xxx, 'cache_hit': 'none'}
[N] marks in the answer: ['1', '2', '3'] | citations returned: 3
   [1] #  1 hr_policy_2026.md        page None score 0.9xxx kind text | row found True | quote in the row True | 1x words
   [2] #  4 hr_policy_2026.md        page None score 0.8xxx kind text | row found True | quote in the row True | 1x words
   [3] #  2 hr_policy_2026.md        page None score 0.6xxx kind text | row found True | quote in the row True | 1x words

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L565

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: one question, two halves, three rows at this checkpoint.

    Do it: one question, two halves, three rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question and three Firestore reads, a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, re, json, subprocess, urllib.request, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"], capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(f"{API}/v1/query", method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                                 data=json.dumps({"query": "What is the notice period for a confirmed E3?", "tenant_id": "acme", "stream": False, "top_k": 3}).encode())
    j = json.load(urllib.request.urlopen(req, timeout=180))
    print("the contract:", json.dumps({"answer": j["answer"][:90] + "...", "citations": f"{len(j['citations'])} citations", "confidence": j["confidence"], "answerable": j["answerable"]}, ensure_ascii=False))
    print("the envelope:", {k: j[k] for k in ("model", "backend", "tokens_in", "tokens_out", "cached_tokens", "cost_usd", "latency_ms", "cache_hit")})
    print("[N] marks in the answer:", sorted(set(re.findall(r"\[(\d+)\]", j["answer"])), key=int), "| citations returned:", len(j["citations"]))
    db = firestore.Client(project=PROJECT)
    norm = lambda s: " ".join(s.split()).lower()
    for i, c in enumerate(j["citations"], 1):
        row = db.collection("chunks").document(c["chunk_id"]).get().to_dict() or {}
        print(f"   [{i}] #{c['chunk_id'].rsplit('#', 1)[1]:>3} {c['source_uri'].split('/')[-1][:24]:24} page {c['page']} score {c['score']:.4f} kind {c['kind']} | row found {bool(row)} | quote in the row {norm(c['quote']) in norm(row.get('text', ''))} | {len(c['quote'].split())} words")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
