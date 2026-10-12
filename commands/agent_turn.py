#!/usr/bin/env python3
"""make agent-turn: one turn of an agent pattern, printed whole (workshop lessons 10.1-10.3 and 10.5).

    python commands/agent_turn.py --offline [--pattern loop|react_text|plan_first] [--desk astar|handbook|statute]
                                  [--thinking minimal|low|medium|high] [--tenant acme] [--question "..."] [--json]
                                  [--invent ["Rs 2,50,000"]]                          # Rs 0, no credential
    python commands/agent_turn.py --live ...         # one real turn on your lane: commands/agent-turn.sh sets it up

It prints each model call - the thinking level it was sent with, its input, thinking and visible tokens and its
rupees - then the tools that call asked for, with their arguments, and what each returned (a search's passages by n,
file and section; a calculator's figure and formula; a refusal's words), then the answer as the Desk shows it (the
model's text, then the lines code writes, desk_agent.compose()), the totals, and the figure check: every figure in the
model's text is a calculator's, the question's or a passage's (desk_calc.unsupported()). The patterns are
commands/agent_patterns.py's. The default question is the gratuity row of evals/agent_tasks.jsonl: Rs 52,000 a month
after 7 years 8 months. A model's text beside its tool calls is printed (plan_first's plan); for react_text, each call
prints the Thought and Action lines the model wrote, what the parser cut from them, and the Observation code wrote.

--invent (offline, react_text only, lesson 10.1's Change-it): the scripted model writes on past its calculator's
Action, an Observation of its own (default "Rs 2,50,000") and a Final Answer from it, as a model does whose stop
sequence does not hold. The parser's cut keeps it out; with that line deleted, the invention is the answer and the
figure check flags it.

--offline: a scripted model and the kit's own corpus, so every count is the script's (agent_patterns.py says how it
counts); the turn never slips. --live needs the lane's environment, which commands/agent-turn.sh exports:
GOOGLE_CLOUD_PROJECT (the model's project), RAG_API_URL (rag-api, for /v1/passages) and DOCUMIND_IMPERSONATE_SA (the
account a shell mints rag-api's ID token as: documind-ui-sa, which every tenant's roster holds). A live turn is a few
gemini-3.6-flash calls on location global, under the chat service's limits of 12 calls and Rs 5. --json prints the
turn's record as one JSON object instead.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_patterns as ap  # noqa: E402
from shared import desk_calc  # noqa: E402

# langchain-core's check of a tool's input serialises the ToolRuntime the desk's tools take, and pydantic warns about
# the context in it, once a tool call: the Desk's own turns do the same. The warning says nothing about the turn.
warnings.filterwarnings("ignore", message="Pydantic serializer warnings", category=UserWarning)
DEFAULT_ROW = "calc-gratuity-7y8m"
LIVE_ENV = ("GOOGLE_CLOUD_PROJECT", "RAG_API_URL", "DOCUMIND_IMPERSONATE_SA")


def _args(args: dict) -> str:
    return ", ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in (args or {}).items())


def _figure(result: dict) -> str:
    unit, value = result.get("unit"), result.get("value")
    if unit == "INR":
        return desk_calc.inr(value) if value is not None else "no figure"
    if unit == "days":
        return f"{desk_calc.num(value)} days"
    if unit == "yes/no":
        return "yes" if value else "no"
    return str(value)


def _result(tool: dict) -> list[str]:
    """What one tool returned, in a line or a few."""
    r = tool.get("result") or {}
    if tool["status"] == "error" or "error" in r:
        return [f"refused: {' '.join(str(r.get('error') or r.get('text') or '').split())[:300]}"]
    if tool["name"] == "retrieve":
        found = r.get("passages") or []
        out = [f"{len(found)} passage{'' if len(found) == 1 else 's'}" + ("" if r.get("answerable") else ", not answerable")
               + (f" ({r['note']})" if r.get("note") else "")]
        out += [f"  [{p.get('n')}] {p.get('source')}" + (f", {p['section']}" if p.get("section") else f" ({p.get('doc_type')})")
                for p in found]
        return out
    if "value" in r:
        return [f"= {_figure(r)}: {r.get('formula')}"]
    return [json.dumps(r, ensure_ascii=False)[:300]]


def _wrote(text: str) -> list[str]:
    """A model's text beside its tool calls (plan_first's plan), in a line or a few."""
    lines = [line.strip() for line in (text or "").strip().splitlines() if line.strip()]
    if len(lines) == 1:
        return [f"  the model wrote: {lines[0]}"]
    return ["  the model wrote:"] + [f"    {line}" for line in lines]


def _react(step: dict) -> list[str]:
    """One react_text call: the lines code read of what the model wrote, what the cut dropped, then the Action code ran
    and the Observation it wrote, or the answer."""
    react = step["react"]
    out = [f"  {line.rstrip()}" for line in react["read"].splitlines() if line.strip()]
    if react.get("cut"):
        out.append("  cut by the parser, which reads nothing from the first \"Observation:\" on:")
        out += [f"    | {line.rstrip()}" for line in react["cut"].splitlines() if line.strip()]
    if react.get("error"):
        out.append(f"  {ap.STOP} {react['error']}    <- written by code: no Action it could run")
    for tool in step["tools"]:
        out.append(f"  -> code runs {tool['name']}({_args(tool['args'])}); the Observation it writes:")
        out += ["       " + line for line in _result(tool)]
    if "final" in react:
        out.append("  -> no tool: the Final Answer is the answer")
    return out


def render(turn: dict, offline: bool, invents: str | None = None) -> str:
    da = ap._da()
    desk, thinking = turn["desk"], turn["thinking"]
    classes = ap.classes_for(desk)
    tools = [t.name for t in da.TOOLSETS[desk]]
    out = [f"agent turn: pattern {turn['pattern']}, desk {desk}, tenant {turn['tenant']}",
           f"  the desk: one retrieve over {', '.join(classes)}, and {len(tools) - 1} calculators: {', '.join(tools[1:])}",
           f"  thinking: {thinking}, sent with every call" if thinking else
           f"  thinking: {da.THINKING_LEVEL}, the desk agent's own (THINKING= sends minimal, low, medium or high with every call)"]
    pat = ap.pattern(turn["pattern"])
    if pat.name != "loop":
        out.append(f"  {pat.name} (lesson {pat.lessons}): {pat.what}")
    if offline:
        level = thinking or da.THINKING_LEVEL
        out.append("  OFFLINE: a scripted model and the kit's own corpus, no credential, no cost. Every count below is the "
                   f"script's: {ap.CHARS_PER_TOKEN} characters a token, {ap.SCRIPTED_THINKING[level]} thinking tokens a call "
                   f"at {level}")
        if invents:
            out.append(f"  --invent: past its calculator's Action the scripted model writes \"{ap.STOP} {invents}\" "
                       "and a Final Answer from it, as a model does whose stop sequence does not hold")
    out += [f"question: {turn['question']}", ""]
    calls = {c["n"]: c for c in turn["calls"]}
    for step in turn["trace"]:
        c = calls.get(step["call"])
        if c is None:
            out.append(f"the turn's limits stopped it: {step['text']}")
            continue
        out.append(f"model call {c['n']} (thinking {c['thinking_level']}): in {c['tokens_in']:,}, thinking "
                   f"{c['thinking_tokens']:,}, visible {c['visible_tokens']:,} tokens, Rs {c['inr']:.4f}")
        if "react" in step:
            out += _react(step)
            continue
        if step["text"] and step["tools"]:
            out += _wrote(step["text"])
        for tool in step["tools"]:
            out.append(f"  -> {tool['name']}({_args(tool['args'])})")
            out += ["       " + line for line in _result(tool)]
        if not step["tools"]:
            out.append("  -> no tool: the answer")
    for c in turn["calls"]:
        if c.get("error"):
            out.append(f"model call {c['n']} failed: {c['error']}")
    out += ["", "answer, as the Desk shows it (the model's text, then what code writes):"]
    out += ["  " + line if line else "" for line in (turn["composed"] or "(no answer)").splitlines()]
    flagged = desk_calc.unsupported(turn["answer"], turn["calculations"], turn["question"],
                                    *[p.get("text") or "" for p in turn["passages"]])
    import limits
    unread = sum(bool((s.get("react") or {}).get("error")) for s in turn["trace"])
    out += ["", f"{turn['model_calls']} model calls ({limits.MAX_MODEL_CALLS} at most), {turn['retrieve_calls']} "
                f"search{'' if turn['retrieve_calls'] == 1 else 'es'}, {len(turn['calculations'])} calculation"
                f"{'' if len(turn['calculations']) == 1 else 's'}, {len(turn['refusals'])} refused or failed tool "
                f"call{'' if len(turn['refusals']) == 1 else 's'}"
                + (f", {unread} format error{'' if unread == 1 else 's'}" if pat.text else "")
                + f"; stopped by {turn['stopped_by'] or 'nothing'}",
            f"tokens: in {turn['tokens_in']:,}, thinking {turn['thinking_tokens']:,}, visible {turn['visible_tokens']:,}; "
            f"Rs {turn['inr']:.4f} for the model calls at list price, Rs {turn['rag_inr']:.4f} for rag-api"
            + (" (the script's tokens: nothing is billed)" if offline else ""),
            "figure check: " + ("every figure in the model's text is a calculator's, the question's or a passage's "
                                "(desk_calc.unsupported: none)" if not flagged else
                                f"no calculator, question or passage wrote {', '.join(flagged)} (desk_calc.unsupported)")]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap_ = argparse.ArgumentParser(description="One turn of an agent pattern, printed whole (make agent-turn).")
    mode = ap_.add_mutually_exclusive_group(required=True)
    mode.add_argument("--offline", action="store_true", help="a scripted model and the kit's corpus: Rs 0")
    mode.add_argument("--live", action="store_true", help="one real turn on your lane (commands/agent-turn.sh)")
    ap_.add_argument("--pattern", default="loop", help=f"built: {', '.join(ap.PATTERNS)}; planned: {', '.join(ap.PLANNED)}")
    ap_.add_argument("--desk", default="astar", choices=("astar", "handbook", "statute"))
    ap_.add_argument("--thinking", choices=ap.THINKING_LEVELS, help="unset: the desk agent's own, low")
    ap_.add_argument("--tenant", default="acme")
    ap_.add_argument("--question", help="unset: the gratuity row of evals/agent_tasks.jsonl")
    ap_.add_argument("--json", action="store_true", help="the turn's record as JSON")
    ap_.add_argument("--invent", nargs="?", const="Rs 2,50,000", metavar="OBSERVATION",
                     help="offline react_text: the model writes its own Observation past its stop sequence")
    a = ap_.parse_args(argv)
    try:
        ap.pattern(a.pattern)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if a.invent is not None and not (a.offline and ap.pattern(a.pattern).text):
        print("ERROR: --invent is for --offline --pattern react_text: the scripted text model invents the Observation",
              file=sys.stderr)
        return 2
    question = a.question or next(r["question"] for r in ap.tasks() if r["id"] == DEFAULT_ROW)
    if a.live:
        missing = [k for k in LIVE_ENV if not os.environ.get(k)]
        if missing:
            print(f"ERROR: --live needs {', '.join(missing)}: run make agent-turn PROJECT=<id>, which sets them "
                  f"(commands/agent-turn.sh), or --offline for the scripted turn", file=sys.stderr)
            return 2
    try:
        if a.offline:
            with ap.offline():
                llm = ap.scripted(question, a.tenant, pattern=a.pattern, invents=a.invent)
                turn = ap.run(a.pattern, question, llm=llm, desk=a.desk, thinking=a.thinking, tenant=a.tenant)
        else:
            turn = ap.run(a.pattern, question, llm=ap.gemini(), desk=a.desk, thinking=a.thinking, tenant=a.tenant)
    except Exception as e:                                   # noqa: BLE001 - the turn failed: say how, exit 1
        print(f"the turn failed: {type(e).__name__}: {' '.join(str(e).split())[:300]}", file=sys.stderr)
        return 1
    print(json.dumps(turn, ensure_ascii=False, indent=1) if a.json else render(turn, a.offline, a.invent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
