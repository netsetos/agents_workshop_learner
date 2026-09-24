"""Lesson 18.1 / s3: The hook's decisions, traced

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: Presidio's recognizers: CreditCard, Crypto, Date, Email, Iban, Ip, MacAddress, MedicalLicense, Nhs, Phone, Spacy, Url, UsBank, UsItin, UsLicense, UsPassport, UsSsn
the classifier's own test cases, which nothing runs:
  'What is GDPR?'                  expected PUBLIC       got PUBLIC
  'Email me at user@acme.com'      expected CONFIDENTIAL got CONFIDENTIAL
  'My Aadhaar is 2345-6789-0123'   expected RESTRICTED   got PUBLIC
  'SSN 123-45-6789'                expected RESTRICTED   got PUBLIC
  'PAN ABCDE1234F'                 expected RESTRICTED   got PUBLIC
the hook, on four requests for documind-general:
  PUBLIC       -> documind-general   'What is the notice period for a confirmed E3?'
  PUBLIC       -> documind-general   'My PAN is ABCDE1234F. What is the notice period for a confirmed E3?'
  RESTRICTED   -> documind-sensitive 'My PAN is ABCDE1234F and I joined on 5 March 2026. What is

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L459

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """cd services/litellm && ~/gw-venv/bin/python - <<'PY'
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the gateway's own classifier and hook; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
