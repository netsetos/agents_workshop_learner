"""Lesson 8.2 / s4: Cross-tenant: every isolation row, as the outsider and as a member

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (11 outsider requests, then 11 member questions)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: the outsider, on 11 isolation rows: 403 on 100%
  iso-01 as zeta   HTTP 200  answerable True   no '40,000'
  iso-02 as globex HTTP 200  answerable False  no '1,84,500'
  iso-03 as globex HTTP 200  answerable False  no '15 June'
  iso-04 as zeta   HTTP 200  answerable False  no '1,005'
  iso-05 as zeta   HTTP 200  answerable False  no 'AAAPZ1234C'
  iso-06 as globex HTTP 200  answerable False  no 'twenty-six weeks'
  iso-07 as globex HTTP 200  answerable False  no "fifteen days' wages"
  iso-08 as zeta   HTTP 200  answerable False  no 'recommendations of the Council'
  iso-09 as zeta   HTTP 200  answerable False  no 'single point of contact'
  iso-10 as globex HTTP 200  answerable False  no 'twice the rate of wages'
  mm-04  as zeta   HTTP 200  answerable False  no '5.2 per cent'

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html#L483

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask, check_isolation, contains, load_golden
api, token = os.environ["API"], os.environ["TOKEN"]
iso = [r for r in load_golden() if r["shape"] == "isolation"]
rate, bad = check_isolation(api, iso, token, os.environ["OUTSIDER"])
print(f"the outsider, on {len(iso)} isolation rows: 403 on {rate:.0%}", *bad, sep="\\n  ")
for r in iso:
    status, body, _ = ask(api, r["question"], r["tenant"], "eval@documind.in", token)
    leaked = [w for w in r["must_not_contain"] if contains(body.get("answer", ""), w)]
    print(f"  {r['id']:6} as {r['tenant']:6} HTTP {status}  answerable {str(body.get('answerable')):5}  "
          + (f"LEAKED {', '.join(leaked)}" if leaked else f"no {r['must_not_contain'][0]!r}"))
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (11 outsider requests, then 11 member questions).
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
