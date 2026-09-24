"""Lesson 16.2 / s4: A generated image, and its usage row

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (one image, then a DEMO_MODE hit)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: generate 1: {'blob': 'acme/gen/9b79e5785c446f20e956772bbe9e2781.png', 'bucket': 'documind-ai-YOUR-ID-media', 'cached': False}
generate 2: {'blob': 'acme/gen/9b79e5785c446f20e956772bbe9e2781.png', 'bucket': 'documind-ai-YOUR-ID-media', 'cached': True}
the usage rows since 2026-09-24T08:10:00Z (Cloud Logging, oldest first):
  tenant acme, modality image, model gemini-3.1-flash-image, cost_usd 0.039, cached False, user documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
  tenant acme, modality image, model gemini-3.1-flash-image, cost_usd 0.0, cached True, user documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
the audit events since then, in documind-ai-YOUR-ID-audit (kept five years): 1
  media.generate by documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com: acme/gen/9b79e5785c446f20e956772bbe9e2781.png, meta {'model': 'gemini-3.1-flash-image', 'synthid': True, 'prom

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.2-studio-voice/Netsetos_GCP_Capstone_16.2_Studio_Voice_WIX.html#L592

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
