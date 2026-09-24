"""Lesson 16.2 / s6: An answer read aloud, and a question nobody hears

Summary and purpose:
The first cell asks the town hall question as documind-ui-sa. It reads the answer aloud with the UI's own cached_tts, twice, and saves the audio as ~/answer.ogg. The text is the answer's first 1,500 characters, as the chat's toggle reads it.

HTML instruction: bash — run in the operator shell, in the kit (one answer, read aloud twice)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: the answer: The CFO said EMEA was the one region that shrank: revenue fell 5.2 per cent, from 96 crore to 91 crore, because two large renewals in Germany slipped into the first quarter of FY2027 [3].
read aloud 1: a miss, synthesised by Chirp 3 HD and written to gs://documind-ai-YOUR-ID-tts-cache/tts/d28fac84987c....ogg (36,799 bytes of Ogg Opus)
read aloud 2: a hit, read back from gs://documind-ai-YOUR-ID-tts-cache/tts/d28fac84987c....ogg (36,799 bytes of Ogg Opus)
saved ~/answer.ogg: in Cloud Shell, cloudshell download ~/answer.ogg hands it to your browser to play

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.2-studio-voice/Netsetos_GCP_Capstone_16.2_Studio_Voice_WIX.html#L732

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q google-cloud-speech==2.40.0 google-cloud-texttospeech==2.37.0   # the UI image's two speech clients
python - <<'PY'
import hashlib, json, os, subprocess, sys, types, urllib.request
P = os.environ["PROJECT"]
os.environ.update(GOOGLE_CLOUD_PROJECT=P, TTS_CACHE_BUCKET=f"{P}-tts-cache", SPEECH_REGION="asia-south1")     # the UI's own settings
sys.modules["streamlit"] = types.ModuleType("streamlit")    # voice.py imports streamlit and never calls it
sys.path.insert(0, "services/frontend")
import voice                                                  # the UI's module, unchanged
API, UI = os.environ["API"], f"documind-ui-sa@{P}.iam.gserviceaccount.com"
Q = "In the FY2026 town hall, what did the CFO say happened to EMEA revenue?"
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}", f"--impersonate-service-account={UI}"],
                     capture_output=True, text=True, check=True).stdout.strip()
req = urllib.request.Request(API + "/v1/query", data=json.dumps({"query": Q, "tenant_id": "acme"}).encode(),
                             headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
answer = json.load(urllib.request.urlopen(req, timeout=180))["answer"]
print("the answer:", answer)
text = answer[:1500]                                          # what chat.py reads aloud: the first 1,500 characters
key = hashlib.sha256(f"en-IN-Chirp3-HD-Kore|1.0|ogg|{text}".encode()).hexdigest()
blob = voice.TTS_CACHE_BUCKET.blob(f"tts/{key}.ogg")
for n in (1, 2):
    hit = blob.exists()
    audio = voice.cached_tts(text)
    print(f"read aloud {n}: {'a hit, read back from' if hit else 'a miss, synthesised by Chirp 3 HD and written to'} "
          f"gs://{P}-tts-cache/tts/{key[:12]}....ogg ({len(audio):,} bytes of Ogg Opus)")
path = os.path.expanduser("~/answer.ogg")
open(path, "wb").write(audio)
print("saved ~/answer.ogg: in Cloud Shell, cloudshell download ~/answer.ogg hands it to your browser to play")
PY
"""


def demonstrate(session):
    """Run Definition at this checkpoint.

    The first cell asks the town hall question as documind-ui-sa. It reads the answer aloud with the UI's own cached_tts, twice, and saves the audio as ~/answer.ogg. The text is the answer's first 1,500 characters, as the chat's toggle reads it.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one answer, read aloud twice).
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
