"""Lesson 16.1 / s6: make smoke-media, green

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the gate: a minute or two)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: DocuMind Module 9 - live smoke test
  api: https://documind-api-NUMBER.asia-south1.run.app
  mcp: https://documind-mcp-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] generate  blob=acme/gen/cd18d3eb6f6dd202ce999de17eb66160.png cached=False
  [PASS] outsider refused  status=403
  [PASS] figure citation  kinds=['figure'] media_url=gs://documind-ai-YOUR-ID-uploads/acme/annual_report_2026_fig  "EMEA's revenue declined, from Rs 96 crore in FY2025 to Rs 91"
  [PASS] media documents  4 of 21 indexed documents are media: ['annual_report_2026_fig3.png', 'inv_2026_0412.png', 'payment_of_bonus_act_1965_p30.png', 'townhall_2026_q1.mp4']
  [PASS] signed PUT  gs://documind-ai-YOUR-ID-uploads/acme/smoke_media_probe.png
  [PASS] worker indexed the PUT  chunks=1 at 2026-09-24T08:14:00.300000+00:00
  --------------------------------------------------------
 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html#L781

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q fastmcp==3.4.7      # the gate's MCP legs (lesson 12.1 installed it; safe to repeat)
make smoke-media PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the gate: a minute or two).
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
