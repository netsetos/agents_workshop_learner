"""Lesson 8.1 / s3: The door and the verifier: who may knock, and what makes a token count

Summary and purpose:
Do it: the API's audiences, and who may invoke it

HTML instruction: bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: IAP_AUDIENCE  /projects/NUMBER/locations/asia-south1/services/documind-ui
              /projects/NUMBER/locations/asia-south1/services/documind-chat
SELF_URL      https://documind-api-NUMBER.asia-south1.run.app
run.invoker   serviceAccount:documind-chat-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-outsider-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
              serviceAccount:documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L472

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the API's audiences, and who may invoke it at this checkpoint.

    Do it: the API's audiences, and who may invoke it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the API's two audiences and who may invoke it; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def gcloud(*a):
        cmd = ["gcloud", *a, "--region", os.environ["REGION"], "--project", os.environ["PROJECT"], "--format=json"]
        return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    env = {e["name"]: e.get("value", "") for e in gcloud("run", "services", "describe", "documind-api")["spec"]["template"]["spec"]["containers"][0].get("env", [])}
    for k in ("IAP_AUDIENCE", "SELF_URL"):
        print(f"{k:13}", "\n              ".join(env.get(k, "(unset)").split(",")))
    for b in gcloud("run", "services", "get-iam-policy", "documind-api").get("bindings", []):
        if b["role"] == "roles/run.invoker":
            print("run.invoker  ", "\n              ".join(sorted(b["members"])))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
