"""Lesson 16.2 / s3: The Studio's and the voice's rules, run

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the rules, run; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: 1. a generation: {'event': 'media', 'modality': 'image', 'model': 'gemini-3.1-flash-image', 'tokens_in': 0, 'cost_usd': 0.039, 'cached': False}
1. a DEMO_MODE hit: {'event': 'media', 'modality': 'image', 'model': 'gemini-3.1-flash-image', 'tokens_in': 0, 'cost_usd': 0.0, 'cached': True}
2. event=chat    copied       by the sink, never read by tenant_daily
2. event=media   never copied by the sink, read by tenant_daily
2. event=query   copied       by the sink, read by tenant_daily
2. event=stream  copied       by the sink, read by tenant_daily
3. read aloud 1, en-IN-Chirp3-HD-Kore: synthesised, then cached (1 object in the bucket)
3. read aloud 2, en-IN-Chirp3-HD-Kore: read back from the cache (1 object in the bucket)
3. read aloud 3, hi-IN-Chirp3-HD-Kore: synthesised, then cached (2 objects in the bucket)
   the first object: tts/171aae62fa1f4b3a....ogg, the SHA-256 of 'en-IN-Chirp3-HD-

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.2-studio-voice/Netsetos_GCP_Capstone_16.2_Studio_Voice_WIX.html#L467

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the rules, run; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, hashlib, os, re, sys, types
    # 1. the Studio's usage row, as media.py writes it (media.py builds its clients at import, so _usage() is lifted out)
    src = open("services/rag-api/media.py", encoding="utf-8").read()
    ns = {"IMAGE_MODEL": re.search(r'IMAGE_MODEL = "([^"]+)"', src).group(1)}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and node.name == "_usage":
            exec(compile(ast.Module([node], []), "media.py", "exec"), ns)
    USD = float(re.search(r"IMAGE_USD = ([0-9.]+)", src).group(1))
    for cached in (False, True):
        row = ns["_usage"]("acme", "documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com", USD, cached, 180 if cached else 7400)
        print(f"1. {'a DEMO_MODE hit' if cached else 'a generation'}:", {k: row[k] for k in ("event", "modality", "model", "tokens_in", "cost_usd", "cached")})
    # 2. which usage events reach tenant_daily: the sink copies some into BigQuery, the view reads others
    sink = open("terraform/sink.tf", encoding="utf-8").read()
    view = open("terraform/sql/tenant_daily.sql", encoding="utf-8").read()
    copied = set(re.findall(r'jsonPayload\.event = "(\w+)"', sink))
    read = set(re.findall(r'"(\w+)"', view.split("WHERE jsonPayload.event IN (", 1)[1].split(")", 1)[0]))
    for event in sorted(copied | read):
        print(f"2. event={event:7} {'copied' if event in copied else 'never copied':12} by the sink, {'read' if event in read else 'never read'} by tenant_daily")
    # 3. the UI's cached_tts, run with its clients stood in: a bucket in memory, a voice that counts its calls
    store, said = {}, []
    class Blob:
        def __init__(self, name): self.name = name
        def exists(self): return self.name in store
        def download_as_bytes(self): return store[self.name]
        def upload_from_string(self, data, content_type=None): store[self.name] = data
    class Voice:
        def streaming_synthesize(self, requests):
            reqs = list(requests)
            said.append(reqs[0].streaming_config.voice.name)
            yield types.SimpleNamespace(audio_content=b"OggS" + reqs[1].input.text.encode())
    Kw = lambda **kw: types.SimpleNamespace(**kw)
    for name, attrs in (("streamlit", {}), ("google.cloud.speech_v2", {"SpeechClient": lambda **kw: None}),
                        ("google.cloud.speech_v2.types", {}), ("google.cloud.speech_v2.types.cloud_speech", {}),
                        ("google.cloud.storage", {"Client": lambda: types.SimpleNamespace(bucket=lambda n: types.SimpleNamespace(blob=Blob))}),
                        ("google.cloud.texttospeech", {"TextToSpeechClient": Voice, "StreamingSynthesizeConfig": Kw, "VoiceSelectionParams": Kw,
                                                       "StreamingAudioConfig": Kw, "AudioEncoding": Kw(OGG_OPUS="OGG_OPUS"),
                                                       "StreamingSynthesizeRequest": Kw, "StreamingSynthesisInput": Kw})):
        sys.modules[name] = types.ModuleType(name)
        sys.modules[name].__dict__.update(attrs)
    sys.modules["google.cloud.speech_v2.types"].cloud_speech = sys.modules["google.cloud.speech_v2.types.cloud_speech"]
    os.environ.update(GOOGLE_CLOUD_PROJECT="documind-ai-YOUR-ID", TTS_CACHE_BUCKET="documind-ai-YOUR-ID-tts-cache")
    sys.path.insert(0, "services/frontend")
    import voice                                                  # the UI's module, unchanged
    text = "EMEA revenue fell 5.2 per cent, from 96 crore to 91 crore."      # the Studio's own text to speak
    for n, v in ((1, "en-IN-Chirp3-HD-Kore"), (2, "en-IN-Chirp3-HD-Kore"), (3, "hi-IN-Chirp3-HD-Kore")):
        before = len(said)
        voice.cached_tts(text, voice=v, lang=v[:5])
        print(f"3. read aloud {n}, {v}: {'synthesised, then cached' if len(said) > before else 'read back from the cache'} "
              f"({len(store)} object{'s' if len(store) > 1 else ''} in the bucket)")
    key = hashlib.sha256(f"en-IN-Chirp3-HD-Kore|1.0|ogg|{text}".encode()).hexdigest()
    print(f"   the first object: tts/{key[:16]}....ogg, the SHA-256 of 'en-IN-Chirp3-HD-Kore|1.0|ogg|' and the text")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
