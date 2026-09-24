"""Lesson 5.2: demo 03 hybrid candidate

Create a no-traffic hybrid candidate, compare the two questions and inspect policy limits.

Run order inside this file:
1. Do it: hybrid on a candidate, the same two questions to both revisions, then undo (source window 31)
2. Do it: hybrid on a candidate, the same two questions to both revisions, then undo (source window 33)
3. Do it: hybrid on a candidate, the same two questions to both revisions, then undo (source window 35)
4. Where hybrid cannot go (source window 38)

Prerequisites: demo_02_rrf_and_ablation.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_hybrid_on_a_candidate_the_same_two_questio.
COMMANDS_01 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RETRIEVAL_MODE=hybrid --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
for U in "$API" "$CAND"; do
  curl -s "$U/version" -H "Authorization: Bearer $(tok "$API")" \\
    | python -c "import sys, json; j = json.load(sys.stdin); print('$U'.split('//')[1].split('.')[0].ljust(36), 'mode', j['retrieval_mode'], '| backend', j['retrieval_backend'])"
done

"""

def step_01_hybrid_on_a_candidate_the_same_two_questio(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; two version reads).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_hybrid_on_a_candidate_the_same_two_questio.
COMMANDS_02 = """ask() { curl -s -X POST "$1/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d "{\\"query\\":\\"$2\\",\\"tenant_id\\":\\"acme\\",\\"stream\\":false,\\"top_k\\":3}" \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('  ', '$1'.split('//')[1].split('---')[0].split('.')[0][:9].ljust(10), [c['chunk_id'].rsplit('#', 1)[1].rjust(3) + ' ' + c['source_uri'].split('/')[-1][:22] for c in j['citations']], '| retrieve_ms', s['retrieve_ms'], '| pool', s['pool'], '| vector_chunks', s['vector_chunks'])"; }
for Q in "What is the total payable on invoice INV-2026-0412?" "What is the notice period for a confirmed E3?"; do
  echo "$Q"; ask "$API" "$Q"; ask "$CAND" "$Q"
done

"""

def step_02_hybrid_on_a_candidate_the_same_two_questio(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (four questions, one or two rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_hybrid_on_a_candidate_the_same_two_questio.
COMMANDS_03 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --remove-env-vars RETRIEVAL_MODE --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
curl -s "$API/version" -H "Authorization: Bearer $(tok "$API")" | python -c "import sys, json; print('live mode:', json.load(sys.stdin)['retrieval_mode'])"
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'

"""

def step_03_hybrid_on_a_candidate_the_same_two_questio(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live mode read again).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def step_04_where_hybrid_cannot_go(session):
    """Run Where hybrid cannot go at this checkpoint.

    Two places, one at startup and one at runtime. A managed backend has no sparse leg to fuse and the Firestore rung's vector index takes one dense vector and nothing else, so check_retrieval_modes() refuses both pairs before the service serves; a tenant pinned to a managed store under hybrid mode is served from the deployment's backend with a retrieval_pin_ignored line instead. At runtime the chaos rung applies to hybrid as to dense: an unreachable index degrades to the Firestore rung, which is dense only, with a vector_search_fallback line and never a 500. The cell asks the validator the two questions offline.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: no call leaves the machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    sys.path[:0] = [".", "services/rag-api"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    for k in ("RETRIEVAL_MODE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY", "TOP_K_RETRIEVE", "RERANK_TIMEOUT_S", "SEMANTIC_CACHE"):
        if os.environ.get(k) == "":
            del os.environ[k]                                  # an empty export from an earlier names box means the default
    from config import check_retrieval_modes
    for backend, mode in (("vector", "hybrid"), ("firestore", "hybrid"), ("rag_engine", "hybrid"), ("firestore", "dense")):
        try:
            check_retrieval_modes(backend, mode); print(f"{backend:10} {mode:6} -> allowed")
        except ValueError as e:
            print(f"{backend:10} {mode:6} -> refused: {str(e)[:96]}...")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_31', step_01_hybrid_on_a_candidate_the_same_two_questio),
        ('source_33', step_02_hybrid_on_a_candidate_the_same_two_questio),
        ('source_35', step_03_hybrid_on_a_candidate_the_same_two_questio),
        ('source_38', step_04_where_hybrid_cannot_go),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
