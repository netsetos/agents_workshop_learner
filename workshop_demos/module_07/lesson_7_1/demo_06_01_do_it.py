"""Lesson 7.1 / s6: Ask the two rows once: the live half's own functions, and the outsider's 403

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (three requests to the API; under a rupee)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_03_the_third_try_listed_and_the_gate_green
Expected observation: lk-32 as acme: HTTP 200, answerable True, 1 citation(s), 2410 ms
   An account unused for 45 days is disabled automatically and must be re-approved to restore it [1].
   must_contain '45 days': found
   cites acme/hr_policy_2026.md
iso-11 as zeta: HTTP 200, answerable True, 1 citation(s), 2230 ms
   Earned leave is encashed on exit at basic pay, capped at 20 days [1].
   must_contain '20 days': found
   must_not_contain 'capped at 45 days': absent
   cites zeta/hr_policy_zeta_2026.md
iso-11 asked by documind-outsider-sa: HTTP 403 (the isolation gate requires 403)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L798

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" OUTSIDER="$(otok)" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask, contains, load_golden
api, rows = os.environ["API"], {r["id"]: r for r in load_golden()}
for rid in ("lk-32", "iso-11"):
    r = rows[rid]
    status, body, ms = ask(api, r["question"], r["tenant"], "eval@documind.in", os.environ["TOKEN"])
    answer, cites = body.get("answer", ""), body.get("citations") or []
    print(f"{rid} as {r['tenant']}: HTTP {status}, answerable {body.get('answerable')}, {len(cites)} citation(s), {ms} ms")
    print("   " + answer[:120])
    for w in r["must_contain"]:
        print(f"   must_contain {w!r}: {'found' if contains(answer, w) else 'MISSING'}")
    for w in r.get("must_not_contain", []):
        print(f"   must_not_contain {w!r}: {'LEAKED' if contains(answer, w) else 'absent'}")
    print("   cites " + ", ".join(sorted({c["source_uri"].split("/", 3)[-1] for c in cites})))
status, _, _ = ask(api, rows["iso-11"]["question"], "zeta", "outsider@not-a-tenant.invalid", os.environ["OUTSIDER"])
print(f"iso-11 asked by documind-outsider-sa: HTTP {status} (the isolation gate requires 403)")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three requests to the API; under a rupee).
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
