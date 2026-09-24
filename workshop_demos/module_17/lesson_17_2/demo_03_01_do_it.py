"""Lesson 17.2 / s3: The checks that run before the spend

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the two self-tests and the rules; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: selftest: the evidence rule dropped jn-06's chunk and kept EMEA elsewhere and lk-09's 8, the question rule dropped lk-06's twin, the PAN row dropped, two formats agree, ModelDraft parses, the batch round trip holds
selftest: an untunable base and a rank the SDK cannot spell are refused before submission; adapter 4 is ADAPTER_SIZE_FOUR and the SDK accepts it
gemini-3.6-flash, adapter 4: refused before submission: managed SFT accepts ['gemini-3.1-flash-lite', 'gemini-3.5-flash'] as of 2026-09-04
gemini-3.1-flash-lite, adapter 3: refused before submission: the LoRA rank must be one of [1, 2, 4, 8, 16, 32]
gemini-3.1-flash-lite, adapter 32: accepted, ADAPTER_SIZE_THIRTY_TWO
make tune's defaults: {'epoch_count': 3, 'adapter_size': 'ADAPTER_SIZE_FOUR', 'tuned_model_display_name': 'documind-sft-v1'}
an endpoint whose path says us is called at: us; with GENERATOR_LOCATION=us-central1: us-central

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.2-managed-tuning/Netsetos_GCP_Capstone_17.2_Managed_Tuning_WIX.html#L454

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python evals/make_trainset.py --selftest
python evals/tune.py --selftest
python - <<'PY'
import ast, re, sys, types
sys.path[:0] = ["evals"]
import tune                                          # stdlib only when imported: no SDK, no project, no network
for base, adapter in (("gemini-3.6-flash", 4), ("gemini-3.1-flash-lite", 3), ("gemini-3.1-flash-lite", 32)):
    try:
        print(f"{base}, adapter {adapter}: accepted, {tune.config_for(base, 3, adapter, 'documind-sft-v2')['adapter_size']}")
    except SystemExit as e:
        print(f"{base}, adapter {adapter}: refused before submission: {str(e).split(': ', 1)[1].split('. ', 1)[0]}")
print(f"make tune's defaults: {tune.config_for('gemini-3.1-flash-lite', 3, 4, 'documind-sft-v1')}")
fn = next(n for n in ast.parse(open("services/rag-api/generator.py", encoding="utf-8").read()).body
          if isinstance(n, ast.FunctionDef) and n.name == "_endpoint_location")


def location(model, override="", region="asia-south1"):     # generator.py builds its clients when imported: the rule is lifted out
    ns = {"re": re, "settings": types.SimpleNamespace(generator_location=override, region=region)}
    exec(compile(ast.Module([fn], []), "generator.py", "exec"), ns)
    return ns["_endpoint_location"](model)


EP = "projects/NUMBER/locations/us/endpoints/ENDPOINT_ID"
print(f"an endpoint whose path says us is called at: {location(EP)}; with GENERATOR_LOCATION=us-central1: {location(EP, 'us-central1')}")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the two self-tests and the rules; no network).
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
