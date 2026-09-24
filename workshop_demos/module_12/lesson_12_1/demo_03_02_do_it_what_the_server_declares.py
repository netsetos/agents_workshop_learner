"""Lesson 12.1 / s3: Expose: what the server declares

Summary and purpose:
Do it: what the server declares

HTML instruction: bash — run in the operator shell, in the kit (the server imported and listed in memory; no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_fastmcp
Expected observation: server DocuMind, protocol 2025-11-25
instructions: DocuMind answers questions about a tenant's documents with citations. Use `ret...
retrieve: Retrieve grounded passages from DocuMind's corpus, with the...
   query            string          required            The question, in natural...
   doc_type         string          default 'all'       policy, contract, invoice,...
   top_k            integer         default 5           How many passages to return...
   tenant           string or null  default None        Only if you belong to several...
list_documents: What is in the caller's corpus: one row per uploaded document,...
   status           string          default 'indexed'   indexed, processing, failed,...
   tenant           string or null  default None        Only if you belong to several...
corpus_stats: Chunks and documents in the caller's corpus, by document type...
   tenant 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L409

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
