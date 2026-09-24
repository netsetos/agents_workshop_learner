"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (one golden question through the candidate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_do_it
Expected observation: lk-06: What is the notice period for a confirmed E3?
answer: A confirmed E3 serves a notice period of 60 days [1].
  cites acme:lk-06#0
model documind-slm, backend gateway: the route the API asked for, whoever answered
cost 0.03977 USD for 1900 tokens in and 40 out: documind-slm's rate, so the small model answered

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L767

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one golden question through the candidate).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, re, subprocess, urllib.request
    P, N, R = os.environ["PROJECT"], os.environ["NUMBER"], os.environ["REGION"]
    API, CAND = f"https://documind-api-{N}.{R}.run.app", os.environ["CAND"]
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email",       # the API checks the token against its own URL
                          f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com", f"--audiences={API}"],
                         capture_output=True, text=True, check=True).stdout.strip()
    rates, group = {}, None
    for line in open("services/litellm/config.yaml", encoding="utf-8"):
        m = re.match(r"  - model_name: (\S+)", line)
        group = m.group(1) if m else group
        m = re.match(r"\s+(input|output)_cost_per_token: ([\d.]+)", line)
        if m:
            rates.setdefault(group, {})[m.group(1)] = float(m.group(2))
    q = "What is the notice period for a confirmed E3?"                        # golden row lk-06
    req = urllib.request.Request(f"{CAND}/v1/query", data=json.dumps({"query": q, "tenant_id": "acme"}).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        j = json.loads(r.read())
    print("lk-06:", q)
    print("answer:", j["answer"])
    for c in j["citations"]:
        print("  cites", c["chunk_id"])
    print(f"model {j['model']}, backend {j['backend']}: the route the API asked for, whoever answered")
    tin, tout, cost = j["tokens_in"], j["tokens_out"], j["cost_usd"]
    priced = {g: tin * v["input"] + tout * v["output"] for g, v in rates.items() if g in ("documind-slm", "documind-general")}
    who = [g for g, usd in priced.items() if cost is not None and abs(usd - cost) < 1e-9]
    print(f"cost {cost} USD for {tin} tokens in and {tout} out: " + (f"{who[0]}'s rate, so " + ("the small model answered" if who[0] == "documind-slm"
          else "Gemini answered: the hook moved it") if who else "no route's rate matches"))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
