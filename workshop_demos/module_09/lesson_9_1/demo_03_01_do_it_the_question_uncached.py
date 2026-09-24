"""Lesson 9.1 / s3: The context cache: a pack, a cache, and the next answer

Summary and purpose:
Do it: the question, uncached

HTML instruction: bash — run in the operator shell, in the kit (a small ask function, a start time for the rows, and one question to the live API)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: backend vertex cache_hit none     tokens_in   1812  cached_tokens      0   2410 ms  | Employees may work remotely up to eight days

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html#L498

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask91() {   # one /v1/query to $1 about acme, as documind-ui-sa; prints the answer's cache fields
TOKEN="$(tok "$API")" URL="$1" Q="$2" python - <<'PY'
import json, os, urllib.error, urllib.request
body = json.dumps({"query": os.environ["Q"], "tenant_id": "acme", "top_k": 6}).encode()
req = urllib.request.Request(os.environ["URL"] + "/v1/query", data=body, method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["TOKEN"]})
try:
    a = json.load(urllib.request.urlopen(req, timeout=120))
    print(f"  backend {a['backend']:6} cache_hit {a['cache_hit']:8} tokens_in {a['tokens_in']:>6}  cached_tokens {a['cached_tokens']:>6}  {a['latency_ms']:>5} ms  | {a['answer'][:44]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}  {e.read().decode(errors='replace')[:90]}")
PY
}
export SINCE91="$(date -u +%FT%TZ)" Q91="How many days a month can I work remotely?"
ask91 "$API" "$Q91"
"""


def demonstrate(session):
    """Run Do it: the question, uncached at this checkpoint.

    Do it: the question, uncached

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a small ask function, a start time for the rows, and one question to the live API).
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
