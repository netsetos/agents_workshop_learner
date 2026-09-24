"""Lesson 16.2 / s6: An answer read aloud, and a question nobody hears

Summary and purpose:
Play it: in Cloud Shell, cloudshell download ~/answer.ogg hands the file to your browser. That is the second proof: an answer read aloud. The second cell gives that audio to the UI's own transcribe, first where the UI runs it, then in eu. eu is a location Google lists chirp_3 in, for Hindi and English (India). The audio leaves India for that one call: a synthetic voice reading an answer about acme, whose policy is any (lesson 15.3). This is the function:

HTML instruction: bash — run in the operator shell, in the kit (the answer's audio, transcribed twice)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_definition
Expected observation: transcribe() where the UI runs it, asia-south1: ''
transcribe() in eu: 'The CFO said EMEA was the one region that shrank: revenue fell 5.2 per cent, from 96 crore to 91 crore, because two large renewals in Germany slipped into the first quarter of FY2027.'

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.2-studio-voice/Netsetos_GCP_Capstone_16.2_Studio_Voice_WIX.html#L790

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Definition at this checkpoint.

    Play it: in Cloud Shell, cloudshell download ~/answer.ogg hands the file to your browser. That is the second proof: an answer read aloud. The second cell gives that audio to the UI's own transcribe, first where the UI runs it, then in eu. eu is a location Google lists chirp_3 in, for Hindi and English (India). The audio leaves India for that one call: a synthetic voice reading an answer about acme, whose policy is any (lesson 15.3). This is the function:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the answer's audio, transcribed twice).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import importlib, os, sys, types
    P = os.environ["PROJECT"]
    os.environ.update(GOOGLE_CLOUD_PROJECT=P, TTS_CACHE_BUCKET=f"{P}-tts-cache", SPEECH_REGION="asia-south1")     # the UI's own settings
    sys.modules["streamlit"] = types.ModuleType("streamlit")    # voice.py imports streamlit and never calls it
    sys.path.insert(0, "services/frontend")
    import voice                                                  # the UI's module, unchanged
    audio = open(os.path.expanduser("~/answer.ogg"), "rb").read()
    print(f"transcribe() where the UI runs it, asia-south1: {voice.transcribe(audio)!r}")
    os.environ["SPEECH_REGION"] = "eu"                          # the same function, pointed at a location Google lists chirp_3 in
    voice = importlib.reload(voice)
    print(f"transcribe() in eu: {voice.transcribe(audio)!r}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
