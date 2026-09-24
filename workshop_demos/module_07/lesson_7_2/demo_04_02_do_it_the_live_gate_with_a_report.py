"""Lesson 7.2 / s4: The live half: every row, two identities, nine rates, three exit codes

Summary and purpose:
Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point.

HTML instruction: bash — run in the operator shell, in the kit (reads the report; changes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_live_gate_with_a_report
Expected observation: answerable_rate    46 answered          of 47 answerable rows
  must_contain_rate  45 with the figure   of 46 ANSWERED
  correct_rate       45 right             of 47 ANSWERABLE
  refusal_rate       18 refused           of 18 unanswerable rows
  pass  request_success_rate  100.0%  (needs 100%)
  pass  answerable_rate        97.9%  (needs 80%)
  pass  citation_rate         100.0%  (needs 95%)
  pass  citation_valid_rate   100.0%  (needs 100%)
  pass  must_contain_rate      97.8%  (needs 85%)
  pass  correct_rate           95.7%  (needs 68%)
  pass  refusal_rate          100.0%  (needs 90%)
  pass  media_kind_rate       100.0%  (needs 80%)
  pass  isolation_403_rate    100.0%  (needs 100%)
  cost a point: jn-06 (answered without ['EMEA', '11.4']), lk-27 (refused)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html#L584

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the live gate, with a report at this checkpoint.

    Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the report; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json
    r = json.load(open("evals/reports/lesson72.json", encoding="utf-8"))
    gold = {g["id"]: g for g in map(json.loads, open("evals/golden.jsonl", encoding="utf-8"))}
    rec = r["records"]
    A = [x for x in rec if gold[x["id"]]["answerable"]]
    answered = [x for x in A if x["outcome"] == "ok" and x["answerable"]]
    contained = [x for x in answered if not x["why"].startswith("answered without")]
    U = [x for x in rec if not gold[x["id"]]["answerable"]]
    refused = [x for x in U if x["outcome"] == "ok" and not x["answerable"]]
    print(f"  answerable_rate    {len(answered):2} answered          of {len(A)} answerable rows")
    print(f"  must_contain_rate  {len(contained):2} with the figure   of {len(answered)} ANSWERED")
    print(f"  correct_rate       {sum(x['pass'] for x in A):2} right             of {len(A)} ANSWERABLE")
    print(f"  refusal_rate       {len(refused):2} refused           of {len(U)} unanswerable rows")
    for k, v in r["scores"].items():
        verdict = "FAIL" if k in r["failed"] else "pass" if k in r["judged"] else " -- "
        print(f"  {verdict}  {k:21} {v:6.1%}  (needs {r['thresholds'][k]:.0%})")
    print("  cost a point:", ", ".join(f"{x['id']} ({x['why'] or x['outcome']})" for x in rec if not x["pass"]) or "nothing")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
