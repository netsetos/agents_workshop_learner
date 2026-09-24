"""Lesson 4.4 / s7: Plan retirement, apply it, then prove zero drift

Summary and purpose:
The code that applies the plan

HTML instruction: bash — verify retirement, citations and the next read-only plan
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_plan_retirement_apply_it_then_prove_zero_drift
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L698

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ch44_source &&
python - <<'PY'
import json, os
from pathlib import Path
r=json.loads(Path(os.environ["DEMO_DIR"], "source.json").read_text())
assert r["status"]=="retired", "Do not continue until this exact source is retired."
print("The fixture is retired.")
PY
ch44_ask absent
ch44_plan clean
"""


def demonstrate(session):
    """Run The code that applies the plan at this checkpoint.

    The code that applies the plan

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — verify retirement, citations and the next read-only plan.
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
