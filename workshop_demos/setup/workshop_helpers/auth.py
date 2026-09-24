"""SDK ADC and gcloud identities are separate; no token is logged."""
import shutil
import subprocess


def gcloud(*args, timeout=90):
    executable = shutil.which("gcloud")
    if not executable:
        raise RuntimeError("gcloud is not on the IDE process PATH. Run PyCharm in the Cloud Workstation.")
    result = subprocess.run([executable, *args], capture_output=True, text=True,
                            timeout=timeout, check=False)
    if result.returncode:
        raise RuntimeError(f"gcloud {' '.join(args[:3])} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def checked_credentials():
    try:
        import google.auth
        from google.auth.transport.requests import Request
    except ImportError as exc:
        raise RuntimeError("Google libraries are missing in this interpreter. Run setup/bootstrap.py with INSTALL_LIVE_DEPENDENCIES=True.") from exc

    class BoundedRequest(Request):
        def __call__(self, *args, **kwargs):
            kwargs["timeout"] = 20
            return super().__call__(*args, **kwargs)

    try:
        credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        credentials.refresh(BoundedRequest())
    except Exception as exc:
        raise RuntimeError(
            "Python ADC could not refresh. Run setup/authenticate.py on this workstation. "
            "If GOOGLE_APPLICATION_CREDENTIALS is set in your Run Configuration, it selects "
            f"a different credential file. Original error: {exc}"
        ) from exc
    return credentials


def identity_token(config, audience):
    return gcloud("auth", "print-identity-token", "--include-email",
                  f"--audiences={audience}",
                  f"--impersonate-service-account={config.ui_service_account}",
                  f"--project={config.project}")
