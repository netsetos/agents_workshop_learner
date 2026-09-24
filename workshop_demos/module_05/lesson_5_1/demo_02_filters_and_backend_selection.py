"""Lesson 5.1: demo 02 filters and backend selection

Exercise the filter contract and inspect per-request backend stages.

Run order inside this file:
1. Do it: four filters, four verdicts (source window 16)
2. Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question (source window 21)

Prerequisites: demo_01_query_vector_and_identity.
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


# Original CLI workflow for step_01_four_filters_four_verdicts.
COMMANDS_01 = """ask() { curl -s -w "\\nHTTP %{http_code}" -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d "{\\"query\\":\\"What is the notice period for a confirmed E3?\\",\\"tenant_id\\":\\"acme\\",\\"stream\\":false,\\"filters\\":$1}" \\
  | python -c "import sys,json; raw=sys.stdin.read(); body,code=raw.rsplit('HTTP ',1); j=json.loads(body); print(code.strip(), '|', (j.get('detail') or f\\"answerable {j['answerable']} pool {j['stages']['pool']} | {j['answer'][:60]}\\"))"; }
ask '{"tenant_id":"zeta"}'
ask '{"doc_type":3}'
ask '{"doc_type":"policy"}'
ask '{"kind":"text"}'

"""

def step_01_four_filters_four_verdicts(session):
    """Run Do it: four filters, four verdicts at this checkpoint.

    Do it: four filters, four verdicts

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two 400s cost nothing; two questions, paise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_tenant_s_pin_and_policy_then_a_full_st.
COMMANDS_02 = """python commands/lane.py tenant-backend acme
python commands/lane.py tenant-policy acme

curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"How many days of earned leave can I carry forward?","tenant_id":"acme","stream":false,"top_k":3}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(json.dumps(j['stages'], indent=1)); print('citations', len(j['citations']), '| cache_hit', j.get('cache_hit'), '| latency_ms', j['latency_ms'])"

"""

def step_02_the_tenant_s_pin_and_policy_then_a_full_st(session):
    """Run Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question at this checkpoint.

    Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (two reads, one question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_16', step_01_four_filters_four_verdicts),
        ('source_21', step_02_the_tenant_s_pin_and_policy_then_a_full_st),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
