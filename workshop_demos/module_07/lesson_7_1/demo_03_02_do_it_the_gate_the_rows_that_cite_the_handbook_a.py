"""Lesson 7.1 / s3: The set as it stands: the gate, the rows that cite the handbook, and the clause no row asks about

Summary and purpose:
The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3. Ten rows cite the handbook, by --source. Now count by clause. The cell reads the handbook's sections and lists, for each clause that is not filler, the ACME rows that anchor on it.

HTML instruction: bash — run in the operator shell, in the kit (reads the handbook and golden.jsonl; changes nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_gate_the_rows_that_cite_the_handbook_a
Expected observation: hr_policy_2026.md: 282 sections, 272 of them GEN- filler
  NP-03      Notice period            lk-06 jn-02 jn-03 vr-01
  PB-02      Probation                lk-04 jn-01
  LV-01      Earned leave             lk-03 lk-07
  LV-07      Leave on exit            jn-01 jn-02 jn-03
  EXP-12     Travel reimbursement     lk-01
  PR-05      Payroll and Form 16      lk-02
  IT-SEC-04  Removable media          lk-05 jn-07
  SEC-09     Access review            <- no golden row asks about this clause
  FIN-02     Purchase approval        lk-08
  WFH-01     Remote work              lk-09

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L490

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the gate, the rows that cite the handbook, and the handbook's clauses at this checkpoint.

    The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3. Ten rows cite the handbook, by --source. Now count by clause. The cell reads the handbook's sections and lists, for each clause that is not filler, the ACME rows that anchor on it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the handbook and golden.jsonl; changes nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, re
    text = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    heads = re.findall(r"(?m)^## (\S+) \S (.+)$", text)
    rows = [json.loads(l) for l in open("evals/golden.jsonl", encoding="utf-8") if l.strip()]
    real = [(code, name) for code, name in heads if not code.startswith("GEN-")]
    print(f"hr_policy_2026.md: {len(heads)} sections, {len(heads) - len(real)} of them GEN- filler")
    for code, name in real:
        ids = [r["id"] for r in rows if r["tenant"] == "acme" and code in r["must_retrieve"]]
        print(f"  {code:10} {name:24} {' '.join(ids) or '<- no golden row asks about this clause'}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
