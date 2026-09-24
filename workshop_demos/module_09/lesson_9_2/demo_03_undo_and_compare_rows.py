"""Lesson 9.2: demo 03 undo and compare rows

Restore revision 1 and explain how old answers relate to the restored fingerprint.

Run order inside this file:
1. The corpus comes back: version 1, and the old answer with it (source window 24)
2. The corpus comes back: version 1, and the old answer with it (source window 26)
3. Every row of the walk (source window 28)

Prerequisites: demo_02_reissue_and_refresh.
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


# Original CLI workflow for step_01_the_corpus_comes_back_version_1_and_the_ol.
COMMANDS_01 = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/corpus/acme/hr_policy_2026.md

"""

def step_01_the_corpus_comes_back_version_1_and_the_ol(session):
    """Run The corpus comes back: version 1, and the old answer with it at this checkpoint.

    Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (version 1's bytes again: the undo).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_corpus_comes_back_version_1_and_the_ol.
COMMANDS_02 = """state92
ask92 "$CAND"

"""

def step_02_the_corpus_comes_back_version_1_and_the_ol(session):
    """Run The corpus comes back: version 1, and the old answer with it at this checkpoint.

    Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the state, and the candidate's ask).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_every_row_of_the_walk(session):
    """Run Every row of the walk at this checkpoint.

    Every row of the walk

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every acme usage row since the start; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
         f'AND jsonPayload.tenant="acme" AND timestamp>="{os.environ["SINCE92"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    for e in json.loads(out or "[]"):
        j, rev = e["jsonPayload"], e["resource"]["labels"]["revision_name"]
        print(f"  {rev[-9:]}  {j['model_backend']:6}  in {j['tokens_in']:>6}  cached {j['cached_tokens']:>6}  Rs {j['cost_usd'] * 85:.4f}  {j['latency_ms']:>5} ms")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_24', step_01_the_corpus_comes_back_version_1_and_the_ol),
        ('source_26', step_02_the_corpus_comes_back_version_1_and_the_ol),
        ('source_28', step_03_every_row_of_the_walk),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
