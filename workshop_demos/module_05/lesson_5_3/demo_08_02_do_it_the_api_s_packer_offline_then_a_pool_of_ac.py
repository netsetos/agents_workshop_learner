"""Lesson 5.3 / s8: What the funnel costs, its knobs, and the packed set the citations come from

Summary and purpose:
The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

HTML instruction: bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_08_01_do_it_the_api_s_packer_offline_then_a_pool_of_ac
Expected observation: pool 20 | citations 2 | generate_ms 3xxx | tokens_in 8xxx | sources ['cgst_act_2017.pdf']
2026-09-2xT1x:xx:xx.xxxxxxZ	1x	x

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L924

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the maximum rate of central tax the CGST Act allows?","tenant_id":"acme","stream":false,"top_k":20}' \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('pool', s['pool'], '| citations', len(j['citations']), '| generate_ms', s['generate_ms'], '| tokens_in', j['tokens_in'], '| sources', sorted({c['source_uri'].split('/')[-1][:20] for c in j['citations']}))"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="context_budget_drop"' \\
  --project "$PROJECT" --freshness 1h --limit 3 --format='value(timestamp,jsonPayload.packed,jsonPayload.dropped)'
"""


def demonstrate(session):
    """Run Do it: the API's packer offline, then a pool of Act pages on the lane at this checkpoint.

    The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read).
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
