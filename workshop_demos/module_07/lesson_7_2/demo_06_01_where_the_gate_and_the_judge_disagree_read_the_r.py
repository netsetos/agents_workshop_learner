"""Lesson 7.2 / s6: Where the gate and the judge disagree: read the row

Summary and purpose:
Four ways the two can meet, and the gate's misses read against the judge's answers. judge.py prints its summary and writes no per-row ratings, so "read the row" means reading the answers. The cell takes each row the gate failed and prints what the judge's own collection received for it.

HTML instruction: bash — run in the operator shell, in the kit (reads both files; changes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it_the_judge_on_your_lane
Expected observation: 2 row(s) cost the gate a point. The judge's own run answered them:
  jn-06  gate: answered without ['EMEA', '11.4']
         judge's answer: 'EMEA revenue fell in FY2026 [1].', 1 cited
         EMEA present; 11.4 absent
  lk-27  gate: refused
         judge's answer: 'The documents do not say.', 0 cited
         twenty per cent absent

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L747

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Where the gate and the judge disagree: read the row at this checkpoint.

    Four ways the two can meet, and the gate's misses read against the judge's answers. judge.py prints its summary and writes no per-row ratings, so "read the row" means reading the answers. The cell takes each row the gate failed and prints what the judge's own collection received for it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads both files; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, sys; sys.path.insert(0, "evals")
    from run_eval import contains
    gate = json.load(open("evals/reports/lesson72.json", encoding="utf-8"))["records"]
    judged = {x["id"]: x for x in json.load(open("evals/reports/judge72.json", encoding="utf-8"))}
    missed = [x for x in gate if not x["pass"]]
    print(f"{len(missed)} row(s) cost the gate a point. The judge's own run answered them:")
    for x in missed:
        j = judged.get(x["id"], {})
        figs = [f"{w} {'present' if contains(j.get('response', ''), w) else 'absent'}" for w in j.get("must_contain", [])]
        print(f"  {x['id']:6} gate: {x['why'] or x['outcome']}")
        print(f"         judge's answer: {j.get('response', '')[:80]!r}, {len(j.get('cited') or [])} cited")
        print(f"         {'; '.join(figs) or 'a refusal row: no figure to look for'}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
