"""Lesson 18.2: demo 01 model definition and billing

Prepare the supplied/stock model definition and read startup/idle billing controls.

Run order inside this file:
1. Do it (source window 8)
2. Do it (source window 12)

Prerequisites: setup_prepare.
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
COMMANDS_01 = """cd services/slm && HF_HUB_DISABLE_PROGRESS_BARS=1 ~/tf-venv/bin/python make_modelfile.py --model unsloth/gemma-4-E2B-it --gguf documind-slm.gguf > ~/Modelfile.182
cd ../.. && cat ~/Modelfile.182

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (downloads the tokenizer's files, about 31 MB; no GPU, no Google Cloud).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the kit's files; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import re
    mk, cfg, api, ev, sm = (open(p, encoding="utf-8").read() for p in ("Makefile", "services/litellm/config.yaml",
                            "services/rag-api/config.py", "evals/run_eval.py", "smoke/smoke_slm.py"))
    deploy = mk.split("\ndeploy-slm:", 1)[1].split("\n\n", 1)[0]
    flag = dict(re.findall(r"--([a-z-]+) (\S+)", deploy))
    d, p, f = (int(x) for x in re.search(r"initialDelaySeconds=(\d+),periodSeconds=(\d+),failureThreshold=(\d+)", deploy).groups())
    smoke = re.search(r"timeout: int = (\d+)", sm).group(1)
    row = re.search(r"urlopen\(req, timeout=(\d+)\)", ev).group(1)
    gw = float(re.search(r'Field\(([\d.]+), alias="GATEWAY_TIMEOUT_S"\)', api).group(1))
    timeout, group = {}, None
    for line in cfg.splitlines():
        m = re.match(r"  - model_name: (\S+)", line)
        group = m.group(1) if m else group
        m = re.match(r"\s+timeout: (\d+)", line)
        if m:
            timeout[group] = int(m.group(1))
    fall = {k: v.replace('"', "") for k, v in re.findall(r"- (documind-[a-z]+): \[([^\]]*)\]", cfg)}
    print(f"the SLM: {flag['gpu']} {flag['gpu-type']}, {flag['cpu']} vCPU, {flag['memory']}; {flag['min-instances']} to {flag['max-instances']} instance; "
          f"{flag['concurrency']} requests at a time; {flag['timeout']} s a request")
    print(f"its startup probe: /api/tags after {d} s, every {p} s, {f} failures allowed: {d + p * f} s for Ollama to list the model")
    print(f"make smoke-slm waits {smoke} s a call")
    print(f"a gate row: run_eval waits {row} s for the API, and asks once more two seconds after a timeout")
    print(f"the API waits {gw:.0f} s for the gateway (GATEWAY_TIMEOUT_S)")
    for route in ("documind-slm", "documind-sensitive"):
        print(f"the gateway waits {timeout[route]} s for {route}, then " + (f"falls back to {fall[route]}" if route in fall else "stops: it has no fallback"))
    L4, CPU, MEM = 0.0001867, 0.000018, 0.000002       # Google's us-central1 rates, USD a second (Cloud Run pricing, 24 September 2026)
    cpu, mem = int(flag["cpu"]), int(flag["memory"].rstrip("Gi"))
    hour = (L4 + cpu * CPU + mem * MEM) * 3600
    print(f"the bill, by the instance: ({L4:.7f} + {cpu} x {CPU:.6f} + {mem} x {MEM:.6f}) USD a second = {hour:.4f} USD an hour = Rs {hour * 85:.2f}")
    print(f"  up to 10 idle minutes after the last request: Rs {hour * 85 / 6:.2f}; min-instances 1 for a 720-hour month: Rs {hour * 85 * 720:,.0f}")
    print("  the kit's own figure: " + re.search(r"costs (Rs [\d,]+/month)", mk).group(1) + ", at $1.42 an hour")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_8', step_01_example),
        ('source_12', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
