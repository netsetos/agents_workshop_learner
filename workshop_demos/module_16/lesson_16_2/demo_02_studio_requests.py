"""Lesson 16.2: demo 02 studio requests

Exercise the implemented Studio examples and inspect their responses.

Run order inside this file:
1. Do it (source window 13)
2. Do it (source window 16)

Prerequisites: demo_01_studio_capabilities.
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
    Operations: bash — run in the operator shell, in the kit (one image, then a DEMO_MODE hit).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast, datetime as dt, json, os, subprocess, time, urllib.request
    import google.auth
    from google.auth import impersonated_credentials
    from google.cloud import storage
    P, API = os.environ["PROJECT"], os.environ["API"]
    UI = f"documind-ui-sa@{P}.iam.gserviceaccount.com"
    PROMPT = next(ast.literal_eval(n.value) for n in ast.parse(open("services/frontend/studio.py", encoding="utf-8").read()).body
                  if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "DEFAULT_PROMPT")     # the Studio tab's own prompt
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}", f"--impersonate-service-account={UI}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    since = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for n in (1, 2):                                              # the second is DEMO_MODE's to serve
        req = urllib.request.Request(API + "/v1/media/generate", data=json.dumps({"prompt": PROMPT, "tenant_id": "acme"}).encode(),
                                     headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
        body = json.load(urllib.request.urlopen(req, timeout=180))
        print(f"generate {n}: {body}")
    time.sleep(15)                                                # a moment for Cloud Logging to hold the rows
    rows = json.loads(subprocess.run(["gcloud", "logging", "read", 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" '
                                      f'AND jsonPayload.event="media" AND timestamp>="{since}"', f"--project={P}", "--format=json", "--limit=10"],
                                     capture_output=True, text=True, check=True).stdout)
    print(f"the usage rows since {since} (Cloud Logging, oldest first):")
    for e in reversed(rows):
        j = e["jsonPayload"]
        print(f"  tenant {j['tenant']}, modality {j['modality']}, model {j['model']}, cost_usd {j['cost_usd']}, cached {j['cached']}, user {j['user']}")
    start = dt.datetime.fromisoformat(since.replace("Z", "+00:00"))
    events = [json.loads(b.download_as_text()) for b in storage.Client(project=P).bucket(f"{P}-audit").list_blobs(
        prefix=f"{start:%Y/%m/%d}/acme/media.generate-") if b.time_created >= start]
    print(f"the audit events since then, in {P}-audit (kept five years): {len(events)}")
    for ev in events:
        print(f"  {ev['action']} by {ev['actor']['user_email']}: {ev['target']['blob']}, meta {ev['meta']}")
    signer = impersonated_credentials.Credentials(source_credentials=google.auth.default()[0], target_principal=UI, lifetime=900,
                                                  target_scopes=["https://www.googleapis.com/auth/devstorage.read_only"])
    url = storage.Client(project=P, credentials=signer).bucket(body["bucket"]).blob(body["blob"]).generate_signed_url(
        version="v4", expiration=dt.timedelta(minutes=15), method="GET", credentials=signer)
    print(f"the image, for 15 minutes, as documind-ui-sa (the Studio's own signer):\n  {url}")

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two refusals, then lesson 16.1's video through the door).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import datetime as dt, hashlib, json, os, subprocess, time, urllib.error, urllib.parse, urllib.request
    P, API = os.environ["PROJECT"], os.environ["API"]
    UI = f"documind-ui-sa@{P}.iam.gserviceaccount.com"
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}", f"--impersonate-service-account={UI}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    
    
    def door(filename, content_type):                             # POST /v1/media/upload-url, as a roster member
        q = urllib.parse.urlencode({"filename": filename, "content_type": content_type, "tenant_id": "acme"})
        req = urllib.request.Request(f"{API}/v1/media/upload-url?{q}", data=b"", method="POST", headers={"Authorization": "Bearer " + tok})
        try:
            return 200, json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode()).get("detail")
    
    
    for fn, ct in (("townhall.zip", "application/zip"), ("../globex/townhall_2026_q1.mp4", "video/mp4")):
        print(f"upload-url {fn} as {ct}: {door(fn, ct)}")
    code, body = door("townhall_2026_q1.mp4", "video/mp4")
    print(f"upload-url townhall_2026_q1.mp4 as video/mp4: {code}, a PUT into gs://{body['bucket']}/{body['blob']}, signed for 15 minutes")
    data = open("evals/corpus/acme/townhall_2026_q1.mp4", "rb").read()        # lesson 16.1's video
    since = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    put = urllib.request.Request(body["url"], data=data, method="PUT", headers={"Content-Type": "video/mp4"})
    print(f"PUT {len(data):,} bytes straight to the bucket: HTTP {urllib.request.urlopen(put, timeout=300).status}")
    key = "acme_" + hashlib.sha256(data).hexdigest()              # the worker's claim key: the bytes' own hash
    for _ in range(30):
        time.sleep(10)
        rows = json.loads(subprocess.run(["gcloud", "logging", "read", 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-ingest" '
                                          f'AND jsonPayload.doc_key="{key}" AND timestamp>="{since}"', f"--project={P}", "--format=json", "--limit=5"],
                                         capture_output=True, text=True, check=True).stdout)
        if rows:
            break
    for e in reversed(rows):
        print("the worker:", json.dumps(e["jsonPayload"]))

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_example),
        ('source_16', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
