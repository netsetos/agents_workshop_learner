"""Lesson 4.2 / s5: Do it: revision 3 of the handbook, on the lane

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (writes the revision to your home directory, then one re-issue)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_six_edits_through_the_worker_s_planner
Expected observation: /home/you/hr_policy_2026_rev3.md | version key acme_54337b4ba3f0...
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	acme_54337b4ba3f0109a...	283	281	2	283	2026-11-01
>> retired (doc_keys, chunks, expire days): [u'acme_497809ffbaa603c4...']	283	30
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html#L558

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import os, hashlib
v1 = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
r3 = v1.replace("# ACME Employee Handbook 2026\\n", "# ACME Employee Handbook 2026 (revision 3)\\n\\nEffective from: 2026-11-01. Revision 3 changes NP-03: the notice period for a confirmed E3 becomes 90 days.\\n", 1)
r3 = r3.replace("serves a notice period of 60 days", "serves a notice period of 90 days", 1)
path = os.path.expanduser("~/hr_policy_2026_rev3.md")
open(path, "w", encoding="utf-8", newline="\\n").write(r3)
print(path, "| version key acme_" + hashlib.sha256(r3.encode("utf-8")).hexdigest()[:12] + "...")
PY

make reindex PROJECT=$PROJECT TENANT=acme FILE=$HOME/hr_policy_2026_rev3.md NAME=hr_policy_2026.md
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (writes the revision to your home directory, then one re-issue).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
