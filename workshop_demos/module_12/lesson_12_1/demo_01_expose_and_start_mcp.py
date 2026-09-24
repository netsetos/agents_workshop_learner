"""Lesson 12.1: demo 01 expose and start mcp

Read the declared tools and start the local MCP server.

Run order inside this file:
1. Do it: what the server declares (source window 9)
2. Do it (source window 13)

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


def step_01_what_the_server_declares(session):
    """Run Do it: what the server declares at this checkpoint.

    Do it: what the server declares

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the server imported and listed in memory; no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import asyncio, logging, sys, textwrap, warnings
    warnings.filterwarnings("ignore")
    sys.path.insert(0, ".")
    import services.mcp.server as server               # the kit's server, imported, not run
    logging.disable(logging.WARNING)                   # its INFO lines; step 6 reads them from a running server
    from fastmcp import Client
    async def main():
        async with Client(server.mcp) as c:            # in memory: no HTTP and no identity, and listing needs neither
            info = c.initialize_result
            print(f"server {info.serverInfo.name}, protocol {info.protocolVersion}")
            print(f"instructions: {info.instructions[:78]}...")
            for t in await c.list_tools():
                s = t.inputSchema
                print(f"{t.name}: {textwrap.shorten(t.description.splitlines()[0], 66, placeholder='...')}")
                for p, spec in s["properties"].items():
                    kind = spec.get("type") or " or ".join(a["type"] for a in spec.get("anyOf", []))
                    need = "required" if p in s.get("required", []) else f"default {spec.get('default')!r}"
                    print(f"   {p:16} {kind:14}  {need:19} {textwrap.shorten(spec.get('description', ''), 32, placeholder='...')}")
    asyncio.run(main())

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's server on your machine, in the background).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    session.set_environment(SELF_URL="http://localhost:8121", RAG_API_URL=os.environ["API"],
                            GOOGLE_CLOUD_PROJECT=session.config.project,
                            DOCUMIND_IMPERSONATE_SA=session.config.ui_service_account)
    session.start_local_service([sys.executable, "-m", "uvicorn", "services.mcp.server:app", "--port", "8121"],
                                "http://localhost:8121/health", expected_health={"status": "ok", "self_url": "http://localhost:8121"})
    print("Owned MCP server log:", session.state["local_service"]["log"])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_what_the_server_declares),
        ('source_13', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
