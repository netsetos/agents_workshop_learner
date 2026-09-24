"""Lesson 13.1 / s4: A right answer, and its trail

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the question, the answer and its trail)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  [1] hr_policy_2026.md  version 497809ffbaa6  chunk 1  'serves a notice period of 60 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-before.json

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html#L530

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask131() {   # ask131 LABEL: acme's E3 notice-period question as documind-ui-sa - the answer and its trail, kept in ~/ask131-LABEL.json
LABEL="$1" python - <<'PY'
import json, os, subprocess, urllib.request
label, P, API = os.environ["LABEL"], os.environ["PROJECT"], os.environ["API"]
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
body = json.dumps({"query": "What is the notice period for a confirmed E3?", "tenant_id": "acme"}).encode()
req = urllib.request.Request(API + "/v1/query", data=body, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
ans = json.load(urllib.request.urlopen(req, timeout=120))
json.dump(ans, open(os.path.expanduser(f"~/ask131-{label}.json"), "w"), indent=1)
s = ans["stages"]
print(ans["answer"])
for n, c in enumerate(ans["citations"], 1):
    version, chunk = c["chunk_id"].split(":", 1)[1].split("#")
    print(f"  [{n}] {c['source_uri'].rsplit('/', 1)[-1]}  version {version[:12]}  chunk {chunk}  {c['quote']!r}")
print(f"  cache_hit {ans['cache_hit']} | backend {ans['backend']} | answerable {ans['answerable']}")
print(f"  store {s.get('retrieval_backend')} | vector_chunks {s.get('vector_chunks')} | pool {s.get('pool')} | "
      f"rerank_fallback {s.get('rerank_fallback', 0)} | policy_fallback {s.get('policy_fallback')}")
print(f"  kept in ~/ask131-{label}.json")
PY
}
ask131 before
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the question, the answer and its trail).
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
