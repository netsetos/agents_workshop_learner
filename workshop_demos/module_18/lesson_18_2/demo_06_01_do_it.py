"""Lesson 18.2 / s6: The cold start, timed

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, after documind-slm has been idle for more than 10 minutes
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: /api/tags              41.4 s   documind-slm:latest (4.3B, Q4_K_M)
/api/generate, first   12.0 s   'OK'
/api/generate, again    0.6 s   'OK'
a cold start: 53.4 s to the first answer - 41.4 s for an instance, then 11.4 s to load the model into the GPU

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L633

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, after documind-slm has been idle for more than 10 minutes.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess, time, urllib.request
    P, N = os.environ["PROJECT"], os.environ["NUMBER"]
    SLM = f"https://documind-slm-{N}.{os.environ.get('SLM_REGION', 'us-central1')}.run.app"
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email",
                          f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com", f"--audiences={SLM}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    
    
    def call(path, body=None):
        req = urllib.request.Request(SLM + path, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=300) as r:
            j = json.loads(r.read())
        return time.time() - t0, j
    
    
    gen = {"model": "documind-slm", "prompt": "Reply with the single word OK.", "stream": False}
    a, tags = call("/api/tags")                                    # waits for an instance, if there is none
    b, first = call("/api/generate", gen)                          # loads the model into the GPU, if it is not loaded
    c, again = call("/api/generate", gen)                          # warm
    m = tags["models"][0]
    print(f"/api/tags             {a:5.1f} s   {m['name']} ({m['details']['parameter_size']}, {m['details']['quantization_level']})")
    print(f"/api/generate, first  {b:5.1f} s   {first['response'].strip()!r}")
    print(f"/api/generate, again  {c:5.1f} s   {again['response'].strip()!r}")
    if a > 10:
        print(f"a cold start: {a + b:.1f} s to the first answer - {a:.1f} s for an instance, then {b - c:.1f} s to load the model into the GPU")
    else:
        print(f"the instance was still up ({a:.1f} s): Cloud Run keeps an idle GPU instance up to 10 minutes. Wait longer and run this again.")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
