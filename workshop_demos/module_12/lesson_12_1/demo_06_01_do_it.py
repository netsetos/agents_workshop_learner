"""Lesson 12.1 / s6: Invoke: retrieve from a local client

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (tools/call from fastmcp's client)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: retrieve: answerable True, 5 citations, confidence high
  'Gratuity becomes payable after not less than five years of continuous serv'
  [1] payment_of_gratuity_act_1972.pdf p.2  'rendered continuous service for not '
  [2] payment_of_gratuity_act_1972.pdf p.2  'the completion of continuous service'
  [3] payment_of_gratuity_act_1972.pdf p.2  'for every completed year of service '
an argument it refuses: doc_type must be one of ('policy', 'contract', 'invoice',
    'report', 'statute', 'guidance', 'form', 'research_paper') or all, not 'memo'
a tenant not on your roster: documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    is not on tenant 'initech''s roster
a token without an email lists 4 tools, and calls:
  not authenticated: the bearer token carries no verified email

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L535

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (tools/call from fastmcp's client).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
