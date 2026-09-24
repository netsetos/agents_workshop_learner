"""Lesson 8.1 / s6: One request, end to end: a forged header, and the row that ignores it

Summary and purpose:
Two questions to acme, one claiming to be the CEO, and the two usage rows they leave. The cell asks the same question twice with run_eval.py's own ask(), which sets an x-user-email header on every request. The first names the eval account; the second claims to be ceo@acme.example. Both carry your token and no assertion, so the bearer leg names the caller. After twenty seconds for the logs to land, the cell reads the two newest query rows for acme.

HTML instruction: bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_which_services_call_the_shared_verifier
Expected observation: x-user-email eval@documind.in   HTTP 200, answerable True
x-user-email ceo@acme.example   HTTP 200, answerable True
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme
YYYY-MM-DDTHH:MM:SS.ssssssZ	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	acme

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L694

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask
q = "What is the notice period for a confirmed E3?"
for header in ("eval@documind.in", "ceo@acme.example"):
    status, body, ms = ask(os.environ["API"], q, "acme", header, os.environ["TOKEN"])
    print(f"x-user-email {header:18} HTTP {status}, answerable {body.get('answerable')}")
PY
sleep 20
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" AND jsonPayload.tenant="acme"' \\
  --project "$PROJECT" --freshness=10m --limit 2 --format='value(timestamp,jsonPayload.user,jsonPayload.tenant)'
"""


def demonstrate(session):
    """Run One request, end to end: a forged header, and the row that ignores it at this checkpoint.

    Two questions to acme, one claiming to be the CEO, and the two usage rows they leave. The cell asks the same question twice with run_eval.py's own ask(), which sets an x-user-email header on every request. The first names the eval account; the second claims to be ceo@acme.example. Both carry your token and no assertion, so the bearer leg names the caller. After twenty seconds for the logs to land, the cell reads the two newest query rows for acme.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two questions, one with a forged x-user-email; then their usage rows).
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
