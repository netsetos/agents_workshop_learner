"""Lesson 4.4 / s5: Prove the document works

Summary and purpose:
On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it. Checkpoint: source indexed at this upload's generation, a cited answer naming locker Q7 in Jaipur, and no pending repair. If the source is indexed but the query has not caught up, repeat ch44_ask present and inspect its evidence; do not upload again merely to wait.

HTML instruction: bash — after the checkpoint passes, save the observed chunk count
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_prove_the_document_works
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L647

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Prove the document works at this checkpoint.

    On the Documents page, use Refresh indexing status and find the exact lesson44_<run-id>.md row. The first upload may need time for the worker and retrieval tier to catch up. The pin is cached for about a minute; the answer's stages prove which backend actually served it. Checkpoint: source indexed at this upload's generation, a cited answer naming locker Q7 in Jaipur, and no pending repair. If the source is indexed but the query has not caught up, repeat ch44_ask present and inspect its evidence; do not upload again merely to wait.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — after the checkpoint passes, save the observed chunk count.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    from pathlib import Path
    d=Path(os.environ["DEMO_DIR"])
    r=json.loads((d/"source.json").read_text())
    assert r["status"]=="indexed" and r["doc_key"]==os.environ["DOC_KEY"]
    assert str(r["generation"])==os.environ["CH44_GENERATION"]
    assert int(r["chunks"])>0
    (d/"initial-chunks.txt").write_text(str(r["chunks"]), encoding="utf-8")
    print("N =", r["chunks"])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
