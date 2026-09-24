"""Lesson 18.1: demo 01 gateway routes

Inspect gateway routes and their configured destinations.

Run order inside this file:
1. Do it (source window 8)
2. Do it (source window 10)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """python -m venv ~/gw-venv && ~/gw-venv/bin/pip install -q $(grep '^presidio' services/litellm/requirements.txt)   # the gateway image's pins
~/gw-venv/bin/python -m spacy download en_core_web_lg > /dev/null && echo "en_core_web_lg installed: the image's model, 400 MB"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """cd services/litellm && ~/gw-venv/bin/python - <<'PY'
import asyncio, sys, types
for name in ("litellm", "litellm.integrations", "litellm.integrations.custom_guardrail"):   # litellm is the image's, not this venv's:
    sys.modules[name] = types.ModuleType(name)                                              # the hook's base class, stood in
sys.modules["litellm.integrations.custom_guardrail"].CustomGuardrail = type("CustomGuardrail", (), {"__init__": lambda self, **kw: None})
import documind_classifier as dc
from documind_router import DocuMindRouter
print("Presidio's recognizers:", ", ".join(sorted(r.name.replace("Recognizer", "") for r in dc.get_analyzer().registry.recognizers)))
print("the classifier's own test cases, which nothing runs:")
for text, expected in dc.test_cases:
    print(f"  {text!r:32} expected {expected.name:12} got {dc.classify_tier(text).name}")
router = DocuMindRouter()
CONTEXT = ("Context:\\n[Source 1] hr_policy_2026.md\\nNP-03. A confirmed E3 serves a notice period of 60 days. "
           "Queries go to hr@acme.com.\\n\\nQuestion: What is the notice period for a confirmed E3?")
print("the hook, on four requests for documind-general:")
for text in ("What is the notice period for a confirmed E3?",
             "My PAN is ABCDE1234F. What is the notice period for a confirmed E3?",               # make smoke-gateway's own
             "My PAN is ABCDE1234F and I joined on 5 March 2026. What is my notice period?",
             CONTEXT):
    data = asyncio.run(router.async_pre_call_hook(None, None, {"model": "documind-general",
                                                               "messages": [{"role": "user", "content": text}]}, "completion"))
    print(f"  {data['metadata']['routing_tier']:12} -> {data['model']:18} {text.splitlines()[0]!r}")
print("and what the last one sends to Gemini:")
print("  " + data["messages"][0]["content"].replace("\\n", "\\n  "))
PY
cd ../..

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_example),
        ('source_10', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
