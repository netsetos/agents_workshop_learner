"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell (reads the gate's report)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_04_do_it
Expected observation: lk-06: pass, 1 citation(s); the route it asked for: documind-slm, through the gateway
8 of 10 rows passed; all thresholds met

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L838

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (reads the gate's report).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    rep = json.load(open(os.path.expanduser("~/slm182.json"), encoding="utf-8"))
    row = next(r for r in rep["records"] if r["id"] == "lk-06")
    print(f"lk-06: {'pass' if row['pass'] else 'fail'}, {row['citations']} citation(s); the route it asked for: {row['model']}, through the {row['backend']}")
    print(f"{sum(r['pass'] for r in rep['records'])} of {len(rep['records'])} rows passed; "
          + ("all thresholds met" if not rep["failed"] else "below the threshold: " + ", ".join(rep["failed"])))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
