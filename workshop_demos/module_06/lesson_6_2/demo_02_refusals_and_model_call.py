"""Lesson 6.2: demo 02 refusals and model call

Compare three refusal envelopes and reproduce the structured model request.

Run order inside this file:
1. Do it: three questions, three envelopes, three rows (source window 21)
2. Do it: the same call, from the shell (source window 26)

Prerequisites: demo_01_answer_contract_and_citations.
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


# Original CLI workflow for step_01_three_questions_three_envelopes_three_rows.
COMMANDS_01 = """ask() { curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" -d "$1" \\
  | python -c "import sys, json; j = json.load(sys.stdin); print('answerable', j['answerable'], '| confidence', j['confidence'], '| citations', len(j['citations']), '| backend', j['backend'], '| tokens', j['tokens_in'], '+', j['tokens_out'], '| cost_usd', j['cost_usd'], '| pool', j['stages']['pool'], '|', j['answer'][:64])"; }
ask '{"query":"What is the notice period at Globex for a confirmed employee?","tenant_id":"globex","stream":false,"top_k":3}'
ask '{"query":"What was ACME\\u0027s revenue in FY2024?","tenant_id":"acme","stream":false,"top_k":3}'
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"doc_type":"policy"}}'
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" AND jsonPayload.unanswerable_flag=1' \\
  --project "$PROJECT" --freshness 5m --limit 3 --format='value(jsonPayload.tenant,jsonPayload.answerable,jsonPayload.model_backend,jsonPayload.tokens_in,jsonPayload.cost_usd)'

"""

def step_01_three_questions_three_envelopes_three_rows(session):
    """Run Do it: three questions, three envelopes, three rows at this checkpoint.

    Do it: three questions, three envelopes, three rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (three questions, two of them model calls: a rupee; one log read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_the_same_call_from_the_shell(session):
    """Run Do it: the same call, from the shell at this checkpoint.

    Do it: the same call, from the shell

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one model call at the generator's rate, a few paise).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, ast, json
    sys.path[:0] = [".", "services/rag-api"]
    from google import genai
    from google.genai import types
    from shared.documind_schemas import ModelDraft, resolve
    from shared import documind_corpus as dc
    from context_budget import pack_chunks, estimate_tokens
    K = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(open("services/rag-api/generator.py", encoding="utf-8").read()).body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "SYSTEM"}
    client = genai.Client(enterprise=True, project=os.environ["PROJECT"], location="global")          # _client: a model NAME is served on the global endpoint
    MODEL = os.environ.get("GENERATOR_MODEL", "gemini-3.6-flash")
    handbook = dc.chunk_document({"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://uploads/acme/hr_policy_2026.md",
                                  "text": open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()}, "acme")
    context, packed, dropped = pack_chunks([next(c for c in handbook if c["locator"] == L) for L in ("NP-03", "PB-02")], 7832, estimate_tokens)
    Q = "What is the notice period for a confirmed E3?"
    prompt = f"{K['SYSTEM']}\n\nContext:\n{context}\n\nQuestion: {Q}"                                # generate(): no dated rule, no packed chunk carries a date
    r = client.models.generate_content(model=MODEL, contents=[prompt], config=types.GenerateContentConfig(
        response_mime_type="application/json", response_schema=ModelDraft, max_output_tokens=2048,
        thinking_config=types.ThinkingConfig(thinking_level="LOW")))                                 # _call(), without a tenant cache
    draft = r.parsed if isinstance(r.parsed, ModelDraft) else ModelDraft.model_validate(json.loads(r.text))
    print("finish:", r.candidates[0].finish_reason.name, "| the draft:", json.dumps(draft.model_dump(), ensure_ascii=False)[:200], "...")
    ans = resolve(draft, packed)
    print("resolved:", [(c.chunk_id, c.page, c.score) for c in ans.citations], "| answerable", ans.answerable, "| confidence", ans.confidence)
    u = r.usage_metadata
    thoughts = getattr(u, "thoughts_token_count", None) or 0
    print("usage: prompt", u.prompt_token_count, "| candidates", u.candidates_token_count, "| thoughts", thoughts, "| cached", getattr(u, "cached_content_token_count", None) or 0)
    try:
        from cost import price                                                                        # the API's own arithmetic
        p = price(MODEL, u.prompt_token_count or 0, (u.candidates_token_count or 0) + thoughts, 0)
        print(f"priced as the API would: ${p['usd']} = Rs {p['inr']} at {p['usd_inr_rate']}")
    except ImportError as e:
        print("cost.price() needs google-cloud-bigquery in the venv:", e)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_three_questions_three_envelopes_three_rows),
        ('source_26', step_02_the_same_call_from_the_shell),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
