"""Lesson 5.3 / s6: make usage: where the time went, p95 per stage, and the view behind it

Summary and purpose:
Do it: the selftest, then the lane's last day, then its rows into the reader

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the selftest touches nothing, and reading the log is free)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_03_do_it_on_a_candidate_a_deadline_no_call_can_meet
Expected observation: selftest: by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
zeta                         1      1500      120    0.0332      2.82    5200   0.00
acme                         2      3800      450    0.0091      0.77    1400   0.50

selftest: where the time went (p95 per stage, by tenant)
tenant                 answers  p95 ms  retrieve  rerank  generate   pool
-------------------------------------------------------------------------
zeta                         1    5200       200     120      4800   20.0
acme                         2    1400       220     130       990   20.0

selftest OK - grouped like tenant_daily: dearest tenant first, tokens summed, p95 the 95th latency, unanswerable a rate, p95 per stage and the pool beside it

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L725

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python evals/usage_rows.py --selftest
make usage PROJECT=$PROJECT HOURS=24
"""


def demonstrate(session):
    """Run Do it: the selftest, then the lane's last day, then its rows into the reader at this checkpoint.

    Do it: the selftest, then the lane's last day, then its rows into the reader

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the selftest touches nothing, and reading the log is free).
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
