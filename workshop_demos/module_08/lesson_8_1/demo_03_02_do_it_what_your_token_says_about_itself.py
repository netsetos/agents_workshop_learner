"""Lesson 8.1 / s3: The door and the verifier: who may knock, and what makes a token count

Summary and purpose:
The cell mints two tokens for the API as documind-ui-sa: one the way tok does, and one without --include-email. It reads their claims without verifying them; the API does the verifying. Nothing is sent.

HTML instruction: bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_api_s_audiences_and_who_may_invoke_it
Expected observation: TOKEN: aud https://documind-api-NUMBER.asia-south1.run.app
       email documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com, email_verified True, iss https://accounts.google.com, 59 minutes left
BARE: aud https://documind-api-NUMBER.asia-south1.run.app
       email (none), email_verified (none), iss https://accounts.google.com, 59 minutes left

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L496

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" BARE="$(gcloud auth print-identity-token --audiences="$API" \\
  --impersonate-service-account="documind-ui-sa@$PROJECT.iam.gserviceaccount.com")" python - <<'PY'
import base64, json, os, time
for name in ("TOKEN", "BARE"):
    part = os.environ[name].split(".")[1]
    c = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))      # read, not verified: the API verifies
    print(f"{name}: aud {c.get('aud')}")
    print(f"       email {c.get('email', '(none)')}, email_verified {c.get('email_verified', '(none)')}, "
          f"iss {c.get('iss')}, {int((c['exp'] - time.time()) / 60)} minutes left")
PY
"""


def demonstrate(session):
    """Run Do it: what your token says about itself at this checkpoint.

    The cell mints two tokens for the API as documind-ui-sa: one the way tok does, and one without --include-email. It reads their claims without verifying them; the API does the verifying. Nothing is sent.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two tokens for the API, one with the email and one without; decoded, not sent).
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
