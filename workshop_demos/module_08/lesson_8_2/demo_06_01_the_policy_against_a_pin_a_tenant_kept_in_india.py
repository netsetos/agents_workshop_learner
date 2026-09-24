"""Lesson 8.2 / s6: The policy against a pin: a tenant kept in India, pinned to a store outside it

Summary and purpose:
A pin set, a minute's wait, one question, its usage row, and the pin cleared. The cell pins globex to rag_engine, a managed store in us-central1, then waits a minute, because the API reads each tenant's settings once a minute. It asks one of globex's own questions and reads the question's usage row: which backend served, and policy_fallback. Then it clears the pin. RETRIEVAL_BACKEND is given on each make line on purpose, because a value exported in your shell would otherwise win.

HTML instruction: bash — run in the operator shell, in the kit (a pin set, one question, its usage row, the pin cleared)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_the_three_policies
Expected observation: globex: retrieval_backend=rag_engine
globex asked: HTTP 200, answerable True
vector	1
globex: retrieval_backend=default

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html#L572

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make tenant-backend TENANT=globex RETRIEVAL_BACKEND=rag_engine
sleep 65                        # the API reads tenant_settings once a minute
TOKEN="$(tok "$API")" python - <<'PY'
import os, sys; sys.path.insert(0, "evals")
from run_eval import ask
status, body, _ = ask(os.environ["API"], "Who is a Data Fiduciary under the DPDP Act?", "globex", "eval@documind.in", os.environ["TOKEN"])
print(f"globex asked: HTTP {status}, answerable {body.get('answerable')}")
PY
sleep 20
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" AND jsonPayload.tenant="globex"' \\
  --project "$PROJECT" --freshness=10m --limit 1 --format='value(jsonPayload.retrieval_backend,jsonPayload.policy_fallback)'
make tenant-backend TENANT=globex RETRIEVAL_BACKEND=default
"""


def demonstrate(session):
    """Run The policy against a pin: a tenant kept in India, pinned to a store outside it at this checkpoint.

    A pin set, a minute's wait, one question, its usage row, and the pin cleared. The cell pins globex to rag_engine, a managed store in us-central1, then waits a minute, because the API reads each tenant's settings once a minute. It asks one of globex's own questions and reads the question's usage row: which backend served, and policy_fallback. Then it clears the pin. RETRIEVAL_BACKEND is given on each make line on purpose, because a value exported in your shell would otherwise win.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a pin set, one question, its usage row, the pin cleared).
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
