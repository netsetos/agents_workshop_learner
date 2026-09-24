"""Lesson 5.3 / s6: make usage: where the time went, p95 per stage, and the view behind it

Summary and purpose:
Do it: the selftest, then the lane's last day, then its rows into the reader

HTML instruction: bash — run in the operator shell (the rows themselves, one JSON line each, for the reader in step 1)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_selftest_then_the_lane_s_last_day_then
Expected observation: NN rows; 1 with rerank_fallback 1; 0 with an empty pool
{"event": "query", "tenant": "acme", "user": "documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com", "tokens_in": xxxx.0, "tokens_out": xxx.0, "cached_tokens": 0.0, "cost_usd": 0.00xxxx, "latency_ms": 2xxx.0, "answerable": true, "retrieve_ms": 6xx.0, "rerank_ms": 3xx.0, "generate_ms": 1xxx.0, "pool": 20.0, "rerank_fallback": 0.0, ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L750

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="query" OR jsonPayload.event="stream")' \\
  --project "$PROJECT" --freshness 24h --limit 40 --format=json \\
  | python -c "import sys, json; [print(json.dumps(e['jsonPayload'])) for e in json.load(sys.stdin) if 'jsonPayload' in e]" > /tmp/rows53.jsonl
python -c "import json; rows = [json.loads(l) for l in open('/tmp/rows53.jsonl')]; print(len(rows), 'rows;', sum(int(r.get('rerank_fallback') or 0) for r in rows), 'with rerank_fallback 1;', sum(1 for r in rows if not r.get('pool')), 'with an empty pool')"
head -c 700 /tmp/rows53.jsonl
"""


def demonstrate(session):
    """Run Do it: the selftest, then the lane's last day, then its rows into the reader at this checkpoint.

    Do it: the selftest, then the lane's last day, then its rows into the reader

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the rows themselves, one JSON line each, for the reader in step 1).
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
