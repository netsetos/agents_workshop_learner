"""Lesson 17.3 / s5: The gate on both revisions

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads the two reports)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: live  candidate  needs
  request_success_rate   100.0%     100.0%   100%
  answerable_rate         97.9%      97.9%    80%
  citation_rate          100.0%     100.0%    95%
  citation_valid_rate    100.0%     100.0%   100%
  must_contain_rate       97.8%      95.7%    85%
  correct_rate            95.7%      93.6%    68%
  refusal_rate           100.0%     100.0%    90%
  media_kind_rate        100.0%     100.0%    80%
  isolation_403_rate     100.0%     100.0%   100%
  jn-03: pass on live, fail on the candidate (answered without ['45', '60'])
  jn-06: fail on live, pass on the candidate (ok)
  jn-09: pass on live, fail on the candidate (answered without ['8.33', 'twenty per cent'])
  3 row(s) changed verdict; median round trip ... ms live, ... ms candidate

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L638

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the two reports).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    base, cand = (json.load(open(os.path.expanduser(f"~/{n}173.json"), encoding="utf-8")) for n in ("base", "cand"))
    print(f"  {'':21} {'live':>7} {'candidate':>10}  {'needs':>5}")
    for k in base["scores"]:
        if k in base["judged"] or k in cand["judged"]:
            flag = "  FAIL" if k in cand["failed"] else ""
            print(f"  {k:21} {base['scores'][k]:7.1%} {cand['scores'][k]:10.1%}  {base['thresholds'][k]:5.0%}{flag}")
    was = {r["id"]: r["pass"] for r in base["records"]}
    moved = [r for r in cand["records"] if was.get(r["id"]) != r["pass"]]
    for r in moved:
        print(f"  {r['id']}: {'pass' if was.get(r['id']) else 'fail'} on live, {'pass' if r['pass'] else 'fail'} on the candidate ({r['why'] or r['outcome']})")
    med = lambda rep: sorted(x["latency_ms"] for x in rep["records"])[len(rep["records"]) // 2]
    print(f"  {len(moved)} row(s) changed verdict; median round trip {med(base)} ms live, {med(cand)} ms candidate")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
