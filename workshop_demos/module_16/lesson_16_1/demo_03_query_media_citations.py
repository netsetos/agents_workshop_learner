"""Lesson 16.1: demo 03 query media citations

Ask about the clip and verify media citation/timestamp evidence.

Run order inside this file:
1. Do it (source window 23)
2. Do it (source window 25)

Prerequisites: demo_02_index_and_inspect_segments.
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


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (golden row mm-03's question, as the UI asks it).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, datetime, json, os, re, subprocess, urllib.request
    import google.auth
    from google.auth import impersonated_credentials
    from google.cloud import storage
    P, API = os.environ["PROJECT"], os.environ["API"]
    UI = f"documind-ui-sa@{P}.iam.gserviceaccount.com"
    Q = "In the FY2026 town hall, what did the CFO say happened to EMEA revenue?"            # golden row mm-03
    ns = {}                                                       # the UI's pill and clock, lifted from services/frontend/citations.py
    for node in ast.parse(open("services/frontend/citations.py", encoding="utf-8").read()).body:
        if isinstance(node, ast.FunctionDef) and node.name in ("_mmss", "_label"):
            exec(compile(ast.Module([node], []), "citations.py", "exec"), ns)
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}", f"--impersonate-service-account={UI}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(API + "/v1/stream", data=json.dumps({"query": Q, "tenant_id": "acme"}).encode(),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    sources, answer, event = [], "", None
    with urllib.request.urlopen(req, timeout=180) as r:           # the events the UI reads: the packed sources first, then the tokens
        for raw in r:
            line = raw.decode("utf-8").rstrip("\n")
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: ") and event == "citation":
                c = json.loads(line[6:])
                sources.append({"text": c["quote"], "source_uri": c["source"], "page_start": c.get("page"), "kind": c.get("kind", "text"),
                                "media_url": c.get("media_url"), "start": c.get("start"), "end": c.get("end")})
            elif line.startswith("data: ") and event == "token":
                answer += json.loads(line[6:])["t"]
    CITE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")                   # citations.py's own pattern
    cited = [int(n) for g in CITE.findall(answer) for n in g.replace(" ", "").split(",")]
    pill = lambda m: "".join(ns["_label"](int(n), sources[int(n) - 1] if 0 < int(n) <= len(sources) else None) for n in m.group(1).replace(" ", "").split(","))
    print(f"{len(sources)} sources packed:", " ".join(f"[{i}] {s['kind']}" for i, s in enumerate(sources, 1)))
    print("the UI shows:", CITE.sub(pill, answer))
    kinds = sorted({sources[n - 1]["kind"] for n in cited if 0 < n <= len(sources)})
    print(f"run_eval's rule for mm-03: cited kinds {kinds}, a segment asked for -> {'PASS' if 'segment' in kinds else 'FAIL'}")
    truth = json.load(open("evals/corpus/acme/townhall_2026_q1.segments.json", encoding="utf-8"))["segments"]
    said = next(t for t in truth if "5.2 per cent" in t["text"])  # the ground truth: the turn in which the CFO says it
    print(f"the ground truth: {said['speaker']} says '5.2 per cent' in the turn {ns['_mmss'](said['start'])}-{ns['_mmss'](said['end'])}")
    signer = impersonated_credentials.Credentials(source_credentials=google.auth.default()[0], target_principal=UI, lifetime=900,
                                                  target_scopes=["https://www.googleapis.com/auth/devstorage.read_only"])
    for n in cited:
        c = sources[n - 1]
        if c["kind"] != "segment":
            continue
        start = int(float(c["start"] or 0))
        holds = c["start"] <= said["end"] and c["end"] >= said["start"]
        print(f"[Clip {n}]: the player opens {c['source_uri'].rsplit('/', 1)[-1]} at {ns['_mmss'](start)}, the clip runs to "
              f"{ns['_mmss'](c['end'])}; it holds the turn -> {'PASS' if holds else 'FAIL'}")
        bucket, name = c["media_url"].removeprefix("gs://").split("/", 1)
        url = storage.Client(project=P, credentials=signer).bucket(bucket).blob(name).generate_signed_url(
            version="v4", expiration=datetime.timedelta(minutes=15), method="GET", credentials=signer)
        print(f"  open it at that second, for 15 minutes, as documind-ui-sa:\n  {url}#t={start}")

# Original CLI workflow for step_02_example.
COMMANDS_02 = """python -m pip install -q fastmcp==3.4.7      # the gate's MCP legs (lesson 12.1 installed it; safe to repeat)
make smoke-media PROJECT="$PROJECT"

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the gate: a minute or two).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_23', step_01_example),
        ('source_25', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
