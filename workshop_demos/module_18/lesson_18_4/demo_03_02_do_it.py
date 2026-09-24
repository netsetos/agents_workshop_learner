"""Lesson 18.4 / s3: The table's maths, read

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads the script, the tools module and config.yaml; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: a row asks the gateway for a route by name: documind-general, documind-slm (make compare's default)
  its context: the citations' quotes of the API's own answer - retrieve() posts to /v1/query
  if that answer takes more than 20 s, the row's context is empty, and only the log says so
from the gateway's reply a row keeps the answer and the token counts, and reads neither the model that answered nor x-litellm-response-cost
its price is the script's own, by the route asked (USD a million tokens, in / out):
  documind-general    table  1.50 /  7.50   config.yaml  1.50 /  7.50
  documind-reasoning  table  1.50 /  7.50   config.yaml  2.00 / 12.00  <- no entry: documind-general's
  documind-slm        table 20.50 / 20.50   config.yaml 20.50 / 20.50
  documind-sensitive  table  1.50 /  7.50   config.yaml 20.50 / 20.50  <- no entry: documind-general's
  documind-inference  table  1.50 /  7.50   c

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.4-compare-shutdown/Netsetos_GCP_Capstone_18.4_Compare_Shutdown_WIX.html#L459

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads the script, the tools module and config.yaml; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import re
    rd = lambda p: open(p, encoding="utf-8").read()
    cb, dt, cfg, mk = rd("services/slm/compare_backends.py"), rd("shared/documind_tools.py"), rd("services/litellm/config.yaml"), rd("Makefile")
    ask = cb.split("def ask(", 1)[1].split("\ndef ", 1)[0]
    backends = re.search(r"BACKENDS:-([\w,-]+)\}", mk).group(1)
    print(f"a row asks the gateway for a route by name: {backends.replace(',', ', ')} (make compare's default)")
    print("  its context: the citations' quotes of the API's own answer - retrieve() posts to "
          + re.search(r'requests\.post\(f"\{RAG_API_URL\}(/v1/\w+)"', dt).group(1))
    wait = re.search(r'"RAG_TIMEOUT_S", "(\d+)"', dt).group(1)
    print(f"  if that answer takes more than {wait} s, the row's context is empty, and only the log says so")
    reads = [k for k in ("model", "x-litellm-response-cost") if f'"{k}")' in ask or f'["{k}"]' in ask]
    print("from the gateway's reply a row keeps the answer and the token counts, and reads "
          + (", ".join(reads) if reads else "neither the model that answered nor x-litellm-response-cost"))
    prices = {k: (float(a), float(b)) for k, a, b in re.findall(r'"(documind-[a-z]+)": \(([\d.]+), ([\d.]+)\)', cb)}
    rates, group = {}, None
    for line in cfg.splitlines():
        m = re.match(r"  - model_name: (\S+)", line)
        group = m.group(1) if m else group
        m = re.match(r"\s+(input|output)_cost_per_token: ([\d.]+)", line)
        if m:
            rates.setdefault(group, {})[m.group(1)] = float(m.group(2)) * 1e6
    print("its price is the script's own, by the route asked (USD a million tokens, in / out):")
    for route, r in rates.items():
        pin, pout = prices.get(route, prices["documind-general"])
        note = "" if route in prices else "  <- no entry: documind-general's"
        print(f"  {route:19} table {pin:5.2f} / {pout:5.2f}   config.yaml {r['input']:5.2f} / {r['output']:5.2f}{note}")
    n = 20
    print(f"p95 on {n} rows is sorted row {max(0, int(round(0.95 * n)) - 1) + 1} of {n}: the slowest row never shows")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
