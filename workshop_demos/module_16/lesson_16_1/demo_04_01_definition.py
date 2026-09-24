"""Lesson 16.1 / s4: The clip built, the transcript withdrawn, the video heard

Summary and purpose:
make media MEDIA_ARGS=--video runs evals/build_media.py:

HTML instruction: bash — run in the operator shell, in the kit (the town hall synthesised: a minute or two)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: python evals/build_media.py --video
  keep annual_report_2026_fig3.png (43 KB) - exists; --force re-renders
  keep inv_2026_0412.png (123 KB) - exists; --force re-renders
  keep payment_of_bonus_act_1965_p30.png (151 KB) - exists; --force re-renders
  voices: {'Meera': 'en-IN-Chirp3-HD-Aoede', 'Arjun': 'en-IN-Chirp3-HD-Charon'}
  Meera    0.0-  21.5s  Good morning, everyone, and welcome to the FY2026 town hall....
  Arjun   22.2-  57.7s  Thanks, Meera. Let me start with the table you all have on s...
  Meera   58.4-  69.6s  On people, headcount closed at 4,180, up from 3,742, and att...
  Arjun   70.3-  93.1s  On capital expenditure we invested 78 crore during the year....
  Meera   93.8- 104.8s  Thank you, Arjun. Questions are open on the portal until Fri...
  corpus/acme/townhall_2026_q1.mp4: 1.5 MB, 106 s, 5 utterances; ground truth beside it in townhall_2026_q1.segments.json

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html#L532

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q Pillow==12.3.0 google-cloud-texttospeech==2.37.0 imageio-ffmpeg==0.6.0   # slides, voices, a static ffmpeg
make media MEDIA_ARGS=--video
"""


def demonstrate(session):
    """Run Definition at this checkpoint.

    make media MEDIA_ARGS=--video runs evals/build_media.py:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the town hall synthesised: a minute or two).
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
