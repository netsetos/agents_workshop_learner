"""Lesson 7.1 / s7: Paraphrase pairs and generated candidates: two kinds of row that are not golden

Summary and purpose:
make make-evalset asks Gemini for one question and answer per chunk of the quality-gated feed. The feed is rag_data.index_feed, joined to the chunks the worker mirrors into BigQuery, so a chunk the quality scan held back never becomes a question. Each pair is scanned by the one PII list, shared/pii.py, and dropped on any finding, never rewritten. What comes out is a candidate: a question with no figure it must contain, and the chunk's id as its only anchor. A golden row is a contract a person writes, and a generated question inherits the blind spots of the model that wrote it. So the file is golden_generated.jsonl, and the gate never reads it. What would the gate say if a candidate were merged as it is? The cell builds one for SEC-09 the way make_evalset.py writes it. Its chunk id is the worker's own: the tenant, the hash of the handbook's bytes, and #8, SEC-09's position after the preamble and seven clauses. Then the cell judges the reviewed version.

HTML instruction: bash — run in the operator shell, in the kit (a candidate for SEC-09 as make-evalset writes one, judged in memory)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_paraphrase_pairs
Expected observation: gen-001  REFUSED
    gen-001: an answerable row with no must_contain accepts any answer at all
    gen-001: anchor 'acme:497809ffbaa6...#8' matches nothing in acme's corpus (slug? clause id? typo?)
lk-32    accepted

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L888

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Generated candidates at this checkpoint.

    make make-evalset asks Gemini for one question and answer per chunk of the quality-gated feed. The feed is rag_data.index_feed, joined to the chunks the worker mirrors into BigQuery, so a chunk the quality scan held back never becomes a question. Each pair is scanned by the one PII list, shared/pii.py, and dropped on any finding, never rewritten. What comes out is a candidate: a question with no figure it must contain, and the chunk's id as its only anchor. A golden row is a contract a person writes, and a generated question inherits the blind spots of the model that wrote it. So the file is golden_generated.jsonl, and the gate never reads it. What would the gate say if a candidate were merged as it is? The cell builds one for SEC-09 the way make_evalset.py writes it. Its chunk id is the worker's own: the tenant, the hash of the handbook's bytes, and #8, SEC-09's position after the preamble and seven clauses. Then the cell judges the reviewed version.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a candidate for SEC-09 as make-evalset writes one, judged in memory).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import hashlib, sys; sys.path.insert(0, "evals")
    from run_eval import load_corpus, check_falsifiable, check_anchors
    corpus = load_corpus()
    sha = hashlib.sha256(open("evals/corpus/acme/hr_policy_2026.md", "rb").read()).hexdigest()
    candidate = {"id": "gen-001", "shape": "generated", "question": "How long can an account stay unused before it is disabled?",
                 "tenant": "acme", "must_contain": [], "must_retrieve": [f"acme:{sha}#8"], "answerable": True}
    reviewed = {**candidate, "id": "lk-32", "shape": "lookup", "must_contain": ["45 days"], "must_retrieve": ["SEC-09", "hr_policy_2026"]}
    for row in (candidate, reviewed):
        found = check_falsifiable([row], corpus) + check_anchors([row], corpus)
        print(f"{row['id']:8} {'REFUSED' if found else 'accepted'}")
        for f in found:
            print("   ", f.replace(sha, sha[:12] + "..."))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
