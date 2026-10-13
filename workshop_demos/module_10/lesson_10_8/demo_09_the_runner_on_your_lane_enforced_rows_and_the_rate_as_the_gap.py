"""Lesson 10.8: The runner on your lane: enforced rows, and the rate as the gap

Do it: the proof's run Do it: the agents' surfaces, switches on The gcloud update makes another documind-chat revision, with neither switch set; the runner then sends the same five rows. The enforced rows cannot move: the tenant pin, the class filter and check_args know nothing of the switches. The measured rows can. Do it: the two runs side by side The peer row, at a local peer

Run order inside this file:
1. Do it: the proof's run (source window 42)
2. Do it: the agents' surfaces, switches on (source window 44)
3. Change it: the switches off, the same rows (source window 46)
4. Do it: the two runs side by side (source window 48)
5. The peer row, at a local peer (source window 50)

Prerequisites: demo_08_the_doors_by_hand_two_brains_the_router_the_lane_s_peer.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
Example: open this file at the matching HTML heading, Run once, then inspect
the observations below before continuing to the next numbered section.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_the_proof_s_run.
COMMANDS_01 = """make attack-eval PROJECT="$PROJECT" REPORT=evals/reports/attacks108_api.json LABEL="lesson 10.8"

"""

def step_01_the_proof_s_run(session):
    """Run Do it: the proof's run at this checkpoint.

    Do it: the proof's run

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the api set against the live revision: the proof's run).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/attack_api.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_agents_surfaces_switches_on.
COMMANDS_02 = """DOCUMIND_ID_TOKEN="$(tok "$CHAT")" python evals/run_attacks.py --chat-url "$CHAT" --desk --surfaces chat,desk \\
  --report evals/reports/attacks108_agents_on.json --label "fence and scrub on"

"""

def step_02_the_agents_surfaces_switches_on(session):
    """Run Do it: the agents' surfaces, switches on at this checkpoint.

    Do it: the agents' surfaces, switches on

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (five rows to documind-chat with the switches on).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/attack_agents_on.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_change_it_the_switches_off_the_same_rows.
COMMANDS_03 = """gcloud run services update documind-chat --region "$REGION" --project "$PROJECT" --quiet \\
  --remove-env-vars AGENT_FENCE,AGENT_SCRUB
DOCUMIND_ID_TOKEN="$(tok "$CHAT")" python evals/run_attacks.py --chat-url "$CHAT" --desk --surfaces chat,desk \\
  --report evals/reports/attacks108_agents_off.json --label "fence and scrub off"

"""

def step_03_change_it_the_switches_off_the_same_rows(session):
    """Run Change it: the switches off, the same rows at this checkpoint.

    The gcloud update makes another documind-chat revision, with neither switch set; the runner then sends the same five rows. The enforced rows cannot move: the tenant pin, the class filter and check_args know nothing of the switches. The measured rows can.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the switches off, then the same five rows).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/attack_agents_off.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

# Original CLI workflow for step_04_the_two_runs_side_by_side.
COMMANDS_04 = """make attack-offline COMPARE="evals/reports/attacks108_agents_on.json evals/reports/attacks108_agents_off.json"

"""

def step_04_the_two_runs_side_by_side(session):
    """Run Do it: the two runs side by side at this checkpoint.

    Do it: the two runs side by side

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the two reports side by side; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/attack_compare.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

# Original CLI workflow for step_05_the_peer_row_at_a_local_peer.
COMMANDS_05 = """DOCUMIND_PEER_URL=http://127.0.0.1:8080 python evals/run_attacks.py --peer-local --surfaces peer --report evals/reports/attacks108_peer.json

"""

def step_05_the_peer_row_at_a_local_peer(session):
    """Run The peer row, at a local peer at this checkpoint.

    The peer row, at a local peer

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — the author's shell, with the peer served locally over a local-profile MCP server (RUN_LIST.md).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/attack_peer.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_05)

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_42', step_01_the_proof_s_run),
        ('source_44', step_02_the_agents_surfaces_switches_on),
        ('source_46', step_03_change_it_the_switches_off_the_same_rows),
        ('source_48', step_04_the_two_runs_side_by_side),
        ('source_50', step_05_the_peer_row_at_a_local_peer),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
