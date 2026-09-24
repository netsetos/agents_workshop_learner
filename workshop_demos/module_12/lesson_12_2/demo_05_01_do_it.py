"""Lesson 12.2 / s5: The gate: make smoke-mcp

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the module's gate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_read_it_back
Expected observation: DocuMind MCP - live smoke test
  target: https://documind-mcp-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] health  {"status":"ok","profile":"gcp","self_url":"https://documind-mcp-NUMBER.asia-south1.run.app"}
  [PASS] tools/list  ['calculate_processing_cost', 'corpus_stats', 'list_documents', 'retrieve']
  [PASS] retrieve  answerable=True citations=5  'Five years of continuous service [1].'
  [PASS] outsider refused  documind-outsider-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com is not on tenant 'acme''s roster
  --------------------------------------------------------
  4 passed, 0 failed

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L512

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export MCP="https://documind-mcp-$NUMBER.$REGION.run.app" SINCE122="$(date -u +%FT%TZ)"
make smoke-mcp PROJECT="$PROJECT" REGION="$REGION"   # the module's gate: health, tools/list, retrieve, the outsider refused
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the module's gate).
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
