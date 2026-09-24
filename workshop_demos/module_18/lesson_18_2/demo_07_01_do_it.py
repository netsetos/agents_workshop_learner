"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (lesson 18.1's three requests, through the gateway)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: USD a million tokens, in and out (config.yaml): documind-general 1.50 and 7.50, documind-sensitive 20.50 and 20.50
  no personal data  HTTP 200  answered by gemini-3.6-flash; 11 tokens in, 1 out; x-litellm-response-cost 2.4e-05
  a bare PAN        HTTP 200  answered by gemini-3.6-flash; 16 tokens in, 1 out; x-litellm-response-cost 3.15e-05
  a PAN and a date  HTTP 200  answered by ollama_chat/documind-slm; 19 tokens in, 30 out; x-litellm-response-cost 0.0010045
                    Your notice period depends on your grade and confirmation status; the documents you shared do not say which applies to you.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L708

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (lesson 18.1's three requests, through the gateway).
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
    
    
    per_m = lambda g: f"{rates[g]['input'] * 1e6:.2f} and {rates[g]['output'] * 1e6:.2f}"
    print(f"USD a million tokens, in and out (config.yaml): documind-general {per_m('documind-general')}, documind-sensitive {per_m('documind-sensitive')}")
    for label, text in (("no personal data", "What is the notice period for a confirmed E3?"),
                        ("a bare PAN", "My PAN is ABCDE1234F. What is the notice period for a confirmed E3?"),
                        ("a PAN and a date", "My PAN is ABCDE1234F and I joined on 5 March 2026. What is my notice period?")):
        status, j, cost = ask(text)
        if status != 200:
            print(f"  {label:17} HTTP {status}  no answer")
            continue
        u = j["usage"]
        print(f"  {label:17} HTTP 200  answered by {j['model']}; {u['prompt_tokens']} tokens in, {u['completion_tokens']} out; "
              f"x-litellm-response-cost {cost}")
        if not j["model"].startswith("gemini"):
            print(f"  {'':17} {j['choices'][0]['message']['content']}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
