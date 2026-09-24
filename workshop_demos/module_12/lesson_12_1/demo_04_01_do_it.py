"""Lesson 12.1 / s4: Start the server on your machine

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the kit's server on your machine, in the background)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_what_the_server_declares
Expected observation: {"status":"ok","profile":"gcp","self_url":"http://localhost:8121"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L478

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """PYTHONPATH=. SELF_URL=http://localhost:8121 RAG_API_URL="$API" GOOGLE_CLOUD_PROJECT="$PROJECT" \\
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" \\
  python -m uvicorn services.mcp.server:app --port 8121 > /tmp/mcp121.log 2>&1 &
export MCP_PID=$!
export MCP_TOKEN="$(tok http://localhost:8121)"   # an ID token minted for THIS server, with your roster member's email
export NO_EMAIL_TOKEN="$(gcloud auth print-identity-token --audiences=http://localhost:8121 \\
  --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com")"   # the same account, no email
until curl -sf http://localhost:8121/health; do sleep 1; done; echo
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's server on your machine, in the background).
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
