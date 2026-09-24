"""Lesson 5.1 / s4: Authorized: the tenant comes from identity, and one index serves three

Summary and purpose:
The UI's service account, which your tok() impersonates, sits on all three rosters. The first two calls send it the same question against acme and zeta; the third sends the outsider's token; the fourth sends the UI's token with a header that claims to be someone else. Each line shows the HTTP status. A request turned away for a reason that passes, a model quota hit, a Cloud Run scale-up or a dropped connection, is asked once more after five seconds; anything else prints the reason the service gave instead of a traceback.

HTML instruction: bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_embed_search_compare
Expected observation: acme: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 40,000. | ['hr_policy_2026.md']
zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement is Rs 25,000 against | ['hr_policy_zeta_2026.md']
outsider on acme: HTTP 403 | not a member of this tenant
ui-sa with a false header on zeta: HTTP 200 | The per-trip cap on domestic travel reimbursement | the header changed nothing

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L667

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: one identity, two tenants, one outsider at this checkpoint.

    The UI's service account, which your tok() impersonates, sits on all three rosters. The first two calls send it the same question against acme and zeta; the third sends the outsider's token; the fourth sends the UI's token with a header that claims to be someone else. Each line shows the HTTP status. A request turned away for a reason that passes, a model quota hit, a Cloud Run scale-up or a dropped connection, is asked once more after five seconds; anything else prints the reason the service gave instead of a traceback.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; two answered questions, two refusals; paise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, time, subprocess, urllib.request, urllib.error
    PROJECT, API = os.environ["PROJECT"], os.environ["API"]
    Q = "What is the per-trip cap on travel reimbursement?"
    def tok(sa):                                                     # the setup block's tok() and otok(), one per service account
        return subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                               f"--impersonate-service-account={sa}@{PROJECT}.iam.gserviceaccount.com"],
                              capture_output=True, text=True, check=True).stdout.strip()
    def ask(token, tenant, extra=None):
        """(status, reply): the JSON the API sent, or the start of whatever else came back; one retry on a status that passes."""
        body = json.dumps({"query": Q, "tenant_id": tenant, "stream": False}).encode()
        for attempt in (1, 2):
            req = urllib.request.Request(f"{API}/v1/query", data=body, method="POST",
                                         headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", **(extra or {})})
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    code, raw = r.status, r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                code, raw = e.code, e.read().decode("utf-8", "replace")
            except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
                code, raw = 0, f"{type(e).__name__}: {e}"
            if code in (0, 429, 500, 502, 503, 504) and attempt == 1:
                print(f"   ({tenant}: HTTP {code or 'none'}, {' '.join(raw.split())[:60]!r}; asking once more in five seconds)")
                time.sleep(5)
                continue
            try:
                return code, json.loads(raw)
            except ValueError:
                return code, {"detail": " ".join(raw.split())[:100]}
    ui = tok("documind-ui-sa")
    for t in ("acme", "zeta"):
        st, j = ask(ui, t)
        print(f"{t}: HTTP {st} |", str(j.get("answer") or j.get("detail", ""))[:70], "|", [c["source_uri"].split("/")[-1] for c in j.get("citations", [])[:1]])
    st, j = ask(tok("documind-outsider-sa"), "acme")
    print(f"outsider on acme: HTTP {st} | {j.get('detail', '')}")
    st, j = ask(ui, "zeta", {"x-user-email": "ceo@zeta.example"})
    print(f"ui-sa with a false header on zeta: HTTP {st} |", str(j.get("answer") or j.get("detail", ""))[:50], "| the header changed nothing" if st == 200 else "")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
