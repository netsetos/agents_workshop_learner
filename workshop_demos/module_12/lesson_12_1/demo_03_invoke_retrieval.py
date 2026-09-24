"""Lesson 12.1: demo 03 invoke retrieval

Call retrieve through a local MCP client and inspect its evidence.

Run order inside this file:
1. Do it (source window 17)

Prerequisites: demo_02_discover_tools.
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


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (tools/call from fastmcp's client).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    os.environ["MCP_TOKEN"] = session.identity_token("http://localhost:8121")
    os.environ["NO_EMAIL_TOKEN"] = session.identity_token("http://localhost:8121", include_email=False)
    import asyncio, logging, os, textwrap
    logging.disable(logging.WARNING)
    from fastmcp import Client
    from fastmcp.client.transports import StreamableHttpTransport
    from fastmcp.exceptions import ToolError
    def client(token):                                 # the transport smoke_mcp.py uses, pointed at your machine
        return Client(StreamableHttpTransport("http://localhost:8121/mcp", headers={"Authorization": f"Bearer {token}"}))
    async def main():
        async with client(os.environ["MCP_TOKEN"]) as c:
            out = (await c.call_tool("retrieve", {"query": "After how many years of continuous service does gratuity become payable?", "tenant": "acme"})).data
            print(f"retrieve: answerable {out['answerable']}, {len(out['citations'])} citations, confidence {out['confidence']}")
            print(f"  {(out.get('answer') or '')[:74]!r}")
            for n, cite in enumerate(out["citations"][:3], 1):
                print(f"  [{n}] {cite['source_uri'].rsplit('/', 1)[-1]} p.{cite.get('page')}  {cite['quote'][:36]!r}")
            for label, args in (("an argument it refuses", {"query": "notice period", "doc_type": "memo"}),
                                ("a tenant not on your roster", {"query": "notice period", "tenant": "initech"})):
                try:
                    await c.call_tool("retrieve", args)
                except ToolError as e:
                    print(textwrap.fill(f"{label}: {e}", 88, subsequent_indent="    "))
        async with client(os.environ["NO_EMAIL_TOKEN"]) as c:
            print(f"a token without an email lists {len(await c.list_tools())} tools, and calls:")
            try:
                await c.call_tool("retrieve", {"query": "notice period"})
            except ToolError as e:
                print(f"  {e}")
    asyncio.run(main())

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
