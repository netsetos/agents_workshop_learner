"""Lesson 7.1 / s4: A lookup row: written into build_golden.py, built, and judged

Summary and purpose:
The next cell judges six versions of the row in memory, with the gate's own two functions. It writes nothing.

HTML instruction: bash — run in the operator shell, in the kit (six versions of the row, judged in memory; writes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_add_the_row_build_gate
Expected observation: as written                               accepted
a figure the clause never gives          REFUSED
    lk-32: must_contain '45 working days' is not in acme's corpus - the row can only fail
words the file breaks across two lines   REFUSED
    lk-32: must_contain 'disabled automatically' is not in acme's corpus - the row can only fail
a clause code with a typo                REFUSED
    lk-32: anchor 'SEC-9' matches nothing in acme's corpus (slug? clause id? typo?)
nothing the answer must contain          REFUSED
    lk-32: an answerable row with no must_contain accepts any answer at all
another clause's figure                  accepted

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L578

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run What the gate catches, and the one mistake it cannot see at this checkpoint.

    The next cell judges six versions of the row in memory, with the gate's own two functions. It writes nothing.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (six versions of the row, judged in memory; writes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys; sys.path.insert(0, "evals")
    from run_eval import load_corpus, check_falsifiable, check_anchors
    corpus = load_corpus()
    row = {"id": "lk-32", "shape": "lookup", "tenant": "acme", "must_contain": ["45 days"],
           "must_retrieve": ["SEC-09", "hr_policy_2026"], "answerable": True}
    for name, change in [("as written", {}),
                         ("a figure the clause never gives", {"must_contain": ["45 working days"]}),
                         ("words the file breaks across two lines", {"must_contain": ["disabled automatically"]}),
                         ("a clause code with a typo", {"must_retrieve": ["SEC-9", "hr_policy_2026"]}),
                         ("nothing the answer must contain", {"must_contain": []}),
                         ("another clause's figure", {"must_contain": ["60 days"]})]:
        found = check_falsifiable([{**row, **change}], corpus) + check_anchors([{**row, **change}], corpus)
        print(f"{name:40} {'REFUSED' if found else 'accepted'}")
        for f in found:
            print("   ", f)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
