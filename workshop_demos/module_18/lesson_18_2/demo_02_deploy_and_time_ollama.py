"""Lesson 18.2: demo 02 deploy and time ollama

Deploy/smoke the stock model and measure a real cold start.

Run order inside this file:
1. Do it (source window 17)
2. Do it (source window 19)
3. Do it (source window 21)

Prerequisites: demo_01_model_definition_and_billing.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_example.
COMMANDS_01 = """make deploy-slm PROJECT="$PROJECT" SLM_STOCK=gemma3:4b      # the first build pulls 3.3 GB into the image: minutes

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a GPU service: it bills while an instance lives).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """make smoke-slm PROJECT="$PROJECT"

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit, right after the deploy.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_example(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_example),
        ('source_19', step_02_example),
        ('source_21', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
