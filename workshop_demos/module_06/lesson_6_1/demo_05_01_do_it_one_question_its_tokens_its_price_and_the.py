"""Lesson 6.1 / s5: One answer's tokens: the packed set's estimate, the model's count, and the price

Summary and purpose:
Do it: one question, its tokens, its price, and the estimate beside it

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question, a rupee)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_three_texts_two_counters_one_pool_twice
Expected observation: the answer: tokens_in 1xxx | cached_tokens 0 | tokens_out 4xx | cost_usd 0.00xxxx | citations 3 | model gemini-3.6-flash
cost.price(): $0.00xxxx = Rs 0.xxxx at 85.0 | in 1xxx out 4xx cached 0
the estimate for the same packed set: fixed 168 + context 8xx = 1xxx | the model counted 1xxx | ratio 0.9x

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L624

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: one question, its tokens, its price, and the estimate beside it at this checkpoint.

    Do it: one question, its tokens, its price, and the estimate beside it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one question, a rupee).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, json, subprocess, urllib.request
    sys.path[:0] = [".", "services/rag-api"]
    from context_budget import estimate_tokens, pack_chunks
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = "What is the notice period for a confirmed E3?"
    tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                          f"--impersonate-service-account=documind-ui-sa@{PROJECT}.iam.gserviceaccount.com"], capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request(f"{API}/v1/query", method="POST", data=json.dumps({"query": Q, "tenant_id": "acme", "stream": False, "top_k": 5}).encode(),
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=180))
    print(f"the answer: tokens_in {j['tokens_in']} | cached_tokens {j.get('cached_tokens', 0)} | tokens_out {j['tokens_out']} | cost_usd {j['cost_usd']} | citations {len(j['citations'])} | model {j['model']}")
    try:
        from cost import price                                                     # the API's own arithmetic; offline the price table falls back to the file's rates
        p = price(j["model"], j["tokens_in"], j["tokens_out"], j.get("cached_tokens", 0))
        print(f"cost.price(): ${p['usd']} = Rs {p['inr']} at {p['usd_inr_rate']} | in {p['tokens_in']} out {p['tokens_out']} cached {p['cached_tokens']}")
    except ImportError as e:
        print("cost.price() needs google-cloud-bigquery in the venv:", e)
    try:
        d = json.load(open("/tmp/pool53.json"))                                   # lesson 5.3's ranked pool for this question
        ranked = [dict(d["pool"][i], source_uri="gs://uploads/acme/" + d["pool"][i]["source"]) for i, _ in d["ranked"]][:5]
        context, packed, dropped = pack_chunks(ranked, 7832, estimate_tokens)
        est = 168 + estimate_tokens(context)
        print(f"the estimate for the same packed set: fixed 168 + context {estimate_tokens(context)} = {est} | the model counted {j['tokens_in']} | ratio {j['tokens_in'] / est:.2f}")
    except FileNotFoundError:
        print("no /tmp/pool53.json here: run lesson 5.3's step 4 first to put the estimate beside tokens_in")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
