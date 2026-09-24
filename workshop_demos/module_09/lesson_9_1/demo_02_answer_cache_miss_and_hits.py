"""Lesson 9.1: demo 02 answer cache miss and hits

Create an answer-cache candidate and compare misses, hits and a paraphrase.

Run order inside this file:
1. Do it (source window 23)
2. Four asks: a miss, two hits and a paraphrase (source window 25)
3. Four asks: a miss, two hits and a paraphrase (source window 27)

Prerequisites: demo_01_context_cache_and_cost.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_example.
COMMANDS_01 = """make candidate PROJECT="$PROJECT" SEMANTIC_CACHE=on
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"; echo "CAND=$CAND"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on and no traffic).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_four_asks_a_miss_two_hits_and_a_paraphrase.
COMMANDS_02 = """ask91 "$CAND" "$Q91"                                   # 1: a miss - retrieved, generated, stored
ask91 "$CAND" "$Q91"                                   # 2: the same words - the exact rung
ask91 "$CAND" "how many days a month can i work remotely"      # 3: other case, no "?" - the same qhash
ask91 "$CAND" "How many days per month am I allowed to work from home?"   # 4: a paraphrase - the near rung, if it is 0.95 close

"""

def step_02_four_asks_a_miss_two_hits_and_a_paraphrase(session):
    """Run Four asks: a miss, two hits and a paraphrase at this checkpoint.

    One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (four asks to the candidate).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_four_asks_a_miss_two_hits_and_a_paraphrase(session):
    """Run Four asks: a miss, two hits and a paraphrase at this checkpoint.

    One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same rows cell, now with the candidate's).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
         f'AND jsonPayload.tenant="acme" AND timestamp>="{os.environ["SINCE91"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    for e in json.loads(out or "[]"):
        j, rev = e["jsonPayload"], e["resource"]["labels"]["revision_name"]
        print(f"  {rev[-9:]}  {j['model_backend']:6}  in {j['tokens_in']:>6}  cached {j['cached_tokens']:>6}  Rs {j['cost_usd'] * 85:.4f}  {j['latency_ms']:>5} ms")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_23', step_01_example),
        ('source_25', step_02_four_asks_a_miss_two_hits_and_a_paraphrase),
        ('source_27', step_03_four_asks_a_miss_two_hits_and_a_paraphrase),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
