"""Lesson 9.3 / s4: The replay: the same pairs, asked live at 0.95

Summary and purpose:
Do it: the replay

HTML instruction: bash — run in the operator shell, in the kit (the 23 golden questions, then the 42 pairs, to the candidate; a few minutes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_the_candidate
Expected observation: pp-01 same right hit      211 ms  How much can I claim per trip for domestic travel?
  pp-15 same right hit      188 ms  Gratuity is paid at what rate per completed year?
  pp-16 same right hit      221 ms  What is the minimum bonus payable under the Bonus Ac
  pp-17 same right hit      209 ms  Under the Code on Wages, what is the rate for overti
  pp-18 same right hit      208 ms  Under the Code on Wages, what is the deadline for pa
  pp-19 same right hit      217 ms  The standing orders chapter of the IR Code applies f
  pp-20 same right hit      194 ms  Under the OSH Code, how many days of work earn a day
  pp-21 same right hit      153 ms  Under the DPDP Act, what is a Consent Manager?
  pp-25 diff FALSE HIT      230 ms  What is the notice period for a confirmed E2?
  pp-31 diff FALSE HIT      236 ms  Who approves a purchase of Rs 30,000?
  same-fact pairs served from the cache: 8 of

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.3-cache-measure/Netsetos_GCP_Capstone_9.3_Cache_Measure_WIX.html#L506

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """TOKEN="$(tok "$API")" python - <<'PY'
import json, os, time, urllib.error, urllib.request
URL, TOKEN = os.environ["CAND"], os.environ["TOKEN"]
gold = {r["id"]: r for r in (json.loads(l) for l in open("evals/golden.jsonl", encoding="utf-8") if l.strip())}
pairs = [json.loads(l) for l in open("evals/paraphrases.jsonl", encoding="utf-8") if l.strip()]
retried, failed = [], []
def ask(q, tenant):
    body = json.dumps({"query": q, "tenant_id": tenant, "top_k": 6}).encode()
    for attempt in range(2):                     # a 5xx or a timeout gets one more try, as run_eval.py gives it
        if attempt:
            time.sleep(2)
        req = urllib.request.Request(URL + "/v1/query", data=body, method="POST",
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN})
        try:
            a = json.load(urllib.request.urlopen(req, timeout=120))
            if attempt:
                retried.append(why)
            return a["backend"], a["answer"], a["latency_ms"]
        except urllib.error.HTTPError as e:
            why = f"HTTP {e.code}"
            if e.code < 500:
                break
        except OSError as e:                     # a timeout or a dropped connection
            why = type(e).__name__
    failed.append(f"{tenant} {q[:50]!r}: {why}")
    return "error", None, 0
first = {of: ask(gold[of]["question"], gold[of]["tenant"]) for of in sorted({p["of"] for p in pairs})}   # misses, stored when answerable
out = []
for p in pairs:
    backend, answer, ms = ask(p["question"], p["tenant"])
    src = next((of for of, (_, a, _) in first.items() if a is not None and a == answer), None) if backend == "cache" else None
    verdict = ("error" if backend == "error" else "miss" if backend != "cache" else "right hit" if p["same"] and src == p["of"]
               else "FALSE HIT" if src == p["of"] else f"hit from {src}")
    out.append({**p, "backend": backend, "ms": ms, "served_from": src, "verdict": verdict})
    if verdict not in ("miss", "error"):
        print(f"  {p['id']} {'same' if p['same'] else 'diff'} {verdict:12} {ms:>5} ms  {p['question'][:52]}")
json.dump(out, open(os.path.expanduser("~/cache93_replay.json"), "w", encoding="utf-8"), indent=1)
for same in (True, False):
    grp = [o for o in out if o["same"] is same]
    print(f"  {'same-fact' if same else 'different'} pairs served from the cache: {sum(o['backend'] == 'cache' for o in grp)} of {len(grp)}")
if retried:
    print(f"  {len(retried)} question(s) answered on a second try ({', '.join(sorted(set(retried)))} the first time): a blip, not an outage")
if failed:
    print(f"  {len(failed)} question(s) got no answer after a second try - the cell below reads the API's traceback:")
    for f in failed[:5]:
        print(f"    {f}")
PY
"""


def demonstrate(session):
    """Run Do it: the replay at this checkpoint.

    Do it: the replay

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the 23 golden questions, then the 42 pairs, to the candidate; a few minutes).
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
