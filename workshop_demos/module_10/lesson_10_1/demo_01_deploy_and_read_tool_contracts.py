"""Lesson 10.1: demo 01 deploy and read tool contracts

Deploy/read the chat service and inspect the tool contracts the model sees.

Run order inside this file:
1. Do it: deploy (source window 6)
2. Do it: where it points, and its brains (source window 8)
3. Do it (source window 12)

Prerequisites: setup_prepare.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_deploy.
COMMANDS_01 = """make deploy-services PROJECT="$PROJECT" REGION="$REGION" SCRIPTS=commands/lesson-12.8.sh ADMIN_EMAILS="$ME"

"""

def step_01_deploy(session):
    """Run Do it: deploy at this checkpoint.

    Do it: deploy

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the chat service built and deployed in your region; several minutes).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_where_it_points_and_its_brains.
COMMANDS_02 = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
gcloud run services describe documind-chat --region "$REGION" --project "$PROJECT" --format=json \\
  | python -c 'import json, sys; s = json.load(sys.stdin); env = {e["name"]: e.get("value") for e in s["spec"]["template"]["spec"]["containers"][0].get("env", [])}; print("  RAG_API_URL", env.get("RAG_API_URL"), "| SELF_URL", env.get("SELF_URL"), "| DOCUMIND_BRAIN", env.get("DOCUMIND_BRAIN"))'
curl -s "$CHAT/health" -H "Authorization: Bearer $(tok "$CHAT")"; echo

"""

def step_02_where_it_points_and_its_brains(session):
    """Run Do it: where it points, and its brains at this checkpoint.

    Do it: where it points, and its brains

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (where the chat service points, and its brains).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (what the model reads of each tool; reads the source, installs nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast
    src = open("services/chat/tools.py", encoding="utf-8").read()
    for fn in ast.parse(src).body:
        if isinstance(fn, ast.FunctionDef) and any(getattr(d, "id", "") == "tool" for d in fn.decorator_list):
            a = fn.args.args
            dflt = [None] * (len(a) - len(fn.args.defaults)) + fn.args.defaults
            shown = [f"{x.arg}: {ast.unparse(x.annotation)}" + (f" = {ast.unparse(v)}" if v is not None else "") for x, v in zip(a, dflt) if x.arg != "runtime"]
            hidden = [x.arg for x in a if x.arg == "runtime"]
            print(f"  {fn.name}({', '.join(shown)})" + (f"    hidden: {hidden[0]}" if hidden else ""))
            print(f"      {ast.get_docstring(fn).splitlines()[0]}")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_6', step_01_deploy),
        ('source_8', step_02_where_it_points_and_its_brains),
        ('source_12', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
