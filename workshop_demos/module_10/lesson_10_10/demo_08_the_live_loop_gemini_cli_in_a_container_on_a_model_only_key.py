"""Lesson 10.10: The live loop: Gemini CLI in a container, on a model-only key

DRY_RUN=1 prints the two docker run lines an iteration would run, and starts nothing: no Docker, image or key is needed. Without the author's cap and key, the live loop does not start. It has no default spend, and it runs only on a model-only key, never on your gcloud login or Application Default Credentials. The author ran the loop in Cloud Shell, which has Docker, with the image built in the same session (Cloud Shell's Docker storage does not outlive it). The cap came from a one-iteration dry run in batch 1. If the probe finds the key needs a project, RALPH_PROJECT adds GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION=global to the agent's environment. The author ran the loop in Cloud Shell, which has Docker, with the image built in the same session (Cloud Shell's Docker storage does not outlive it). The cap came from a one-iteration dry run in batch 1. If the probe finds the key needs a project, RALPH_PROJECT adds GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION=global to the agent's environment. Then the reviewer, on the loop's own work:

Run order inside this file:
1. Do it: the two containers, printed (source window 62)
2. Do it: the live loop on your lane (source window 64)
3. The author's run (source window 66)
4. The author's run (source window 68)

Prerequisites: demo_07_the_reviewer_a_linter_first_then_gemini_on_your_lane.
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


# Original CLI workflow for step_01_the_two_containers_printed.
COMMANDS_01 = """make ralph DRY_RUN=1

"""

def step_01_the_two_containers_printed(session):
    """Run Do it: the two containers, printed at this checkpoint.

    DRY_RUN=1 prints the two docker run lines an iteration would run, and starts nothing: no Docker, image or key is needed.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the live loop's two containers, printed; nothing starts).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: ralph --dry-run: the two containers an iteration runs, and nothing else; nothing is started
      the agent: docker run --rm --init --name ralph-<run>-01 --cap-drop ALL --security-opt no-new-privileges --read-only --tmpfs /tmp --memory 2g --pids-limit 256 --cpus 2 --user UID:GID --env-file <run>/agent.env --env RALPH_MODEL=gemini-3.6-flash --env HOME=/tmp --mount type=bind,source=<run>/workspace,target=/work --mount type=bind,source=/home/you/deploy_module_rag/commands/ralph/PROMPT.md,target=/ralph/PROMPT.md,readonly --mount type=bind,source=/home/you/deploy_module_rag/commands/ralph/settings.json,target=/etc/gemini-cli/settings.json,readonly --workdir /work documind-ralph ralph-iteration
        it
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_live_loop_on_your_lane.
COMMANDS_02 = """make ralph                        # live, with no cap
make ralph RALPH_BUDGET_INR=30    # live, with a cap and no key

"""

def step_02_the_live_loop_on_your_lane(session):
    """Run Do it: the live loop on your lane at this checkpoint.

    Without the author's cap and key, the live loop does not start. It has no default spend, and it runs only on a model-only key, never on your gcloud login or Application Default Credentials.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the live loop without the author's cap or key).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: ERROR: the live loop has no default spend: give it RALPH_BUDGET_INR=<cap>, set from a dry run (make ralph RALPH_MAX_ITERS=1 RALPH_BUDGET_INR=<a small cap> reads one iteration's rupees)
    make: *** [mk/coding.mk:31: ralph] Error 2
    ERROR: RALPH_API_KEY is not set: the live loop runs only on a model-only credential the author creates for the run and deletes after it, never on your gcloud login or ADC
    make: *** [mk/coding.mk:31: ralph] Error 2
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_the_author_s_run.
COMMANDS_03 = """make ralph-image GEMINI_CLI_VERSION=PIN            # PIN: the version the batch-1 probe pinned; once a session
read -rs RALPH_API_KEY && export RALPH_API_KEY     # the model-only key, typed: never echoed, never in history
make ralph RALPH_MAX_ITERS=8 RALPH_BUDGET_INR=CAP OUT="$HOME/ralph-live"   # CAP: from the batch-1 dry run

"""

def step_03_the_author_s_run(session):
    """Run The author's run at this checkpoint.

    The author ran the loop in Cloud Shell, which has Docker, with the image built in the same session (Cloud Shell's Docker storage does not outlive it). The cap came from a one-iteration dry run in batch 1. If the probe finds the key needs a project, RALPH_PROJECT adds GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION=global to the agent's environment.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — the author's run, on the author's lane, in Cloud Shell (batch 4): yours refuses, as above.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/ralph_loop.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

# Original CLI workflow for step_04_the_author_s_run.
COMMANDS_04 = """export RUN="$(ls -dt "$HOME"/ralph-live/ralph-* | head -n 1)"
make review-diff PROJECT="$PROJECT" DIFF="$RUN/ralph.patch"

"""

def step_04_the_author_s_run(session):
    """Run The author's run at this checkpoint.

    The author ran the loop in Cloud Shell, which has Docker, with the image built in the same session (Cloud Shell's Docker storage does not outlive it). The cap came from a one-iteration dry run in batch 1. If the probe finds the key needs a project, RALPH_PROJECT adds GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION=global to the agent's environment. Then the reviewer, on the loop's own work:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — the author's run (batch 4): the reviewer on the live loop's work.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/review_diff.txt]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_62', step_01_the_two_containers_printed),
        ('source_64', step_02_the_live_loop_on_your_lane),
        ('source_66', step_03_the_author_s_run),
        ('source_68', step_04_the_author_s_run),
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
