"""Lesson 18.1 / s6: A PAN re-routed, and the cost header

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (three short answers through the gateway)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: documind-general is priced at 1.50 and 7.50 USD a million tokens, in and out (config.yaml)
  no personal data  HTTP 200  answered by gemini-3.6-flash; 11 tokens in, 20 out; x-litellm-response-cost 0.0001665
  a bare PAN        HTTP 200  answered by gemini-3.6-flash; 16 tokens in, 20 out; x-litellm-response-cost 0.000174
  a PAN and a date  HTTP 500  no answer: the route the hook chose has no backend yet, and no fallback

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L636

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (three short answers through the gateway).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, re, subprocess, urllib.error, urllib.request
    P, N, R = os.environ["PROJECT"], os.environ["NUMBER"], os.environ["REGION"]
    GW = f"https://documind-gateway-{N}.{R}.run.app"
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email",
                          f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com", f"--audiences={GW}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    rates, group = {}, None                                        # config.yaml's per-token rates, by route
    for line in open("services/litellm/config.yaml", encoding="utf-8"):
        m = re.match(r"  - model_name: (\S+)", line)
        group = m.group(1) if m else group
        m = re.match(r"\s+(input|output)_cost_per_token: ([\d.]+)", line)
        if m:
            rates.setdefault(group, {})[m.group(1)] = float(m.group(2))
    
    
    def ask(text):
        body = json.dumps({"model": "documind-general", "messages": [{"role": "user", "content": text}], "max_tokens": 60}).encode()
        req = urllib.request.Request(f"{GW}/v1/chat/completions", data=body, method="POST",
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {tok}"})
        try:
            with urllib.request.urlopen(req, timeout=150) as r:
                return r.status, json.loads(r.read()), r.headers.get("x-litellm-response-cost")
        except urllib.error.HTTPError as e:
            return e.code, None, None
    
    
    g = rates["documind-general"]
    print(f"documind-general is priced at {g['input'] * 1e6:.2f} and {g['output'] * 1e6:.2f} USD a million tokens, in and out (config.yaml)")
    for label, text in (("no personal data", "What is the notice period for a confirmed E3?"),
                        ("a bare PAN", "My PAN is ABCDE1234F. What is the notice period for a confirmed E3?"),
                        ("a PAN and a date", "My PAN is ABCDE1234F and I joined on 5 March 2026. What is my notice period?")):
        status, j, cost = ask(text)
        if status == 200:
            u = j["usage"]
            print(f"  {label:17} HTTP 200  answered by {j['model']}; {u['prompt_tokens']} tokens in, {u['completion_tokens']} out; "
                  f"x-litellm-response-cost {cost}")
        else:
            print(f"  {label:17} HTTP {status}  no answer: the route the hook chose has no backend yet, and no fallback")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
