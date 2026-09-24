"""Lesson 5.1 / s6: The restricts, the per-request backend, and the stages block

Summary and purpose:
Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (two reads, one question)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_four_filters_four_verdicts
Expected observation: acme: retrieval_backend=vector
acme: data_region=any
{
 "policy_fallback": 0,
 "retrieval_backend": "vector",
 "retrieve_ms": 612,
 "pool": 20,
 "graph_chunks": 0,
 "managed_chunks": 0,
 "vector_chunks": 20,
 "rerank_ms": 388,
 "generate_ms": 1742
}
citations 3 | cache_hit none | latency_ms 2760

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L815

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python commands/lane.py tenant-backend acme
python commands/lane.py tenant-policy acme

curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"How many days of earned leave can I carry forward?","tenant_id":"acme","stream":false,"top_k":3}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(json.dumps(j['stages'], indent=1)); print('citations', len(j['citations']), '| cache_hit', j.get('cache_hit'), '| latency_ms', j['latency_ms'])"
"""


def demonstrate(session):
    """Run Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question at this checkpoint.

    Do it: the tenant's pin and policy, then a full stages block, Rs 0 plus one question

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (two reads, one question).
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
