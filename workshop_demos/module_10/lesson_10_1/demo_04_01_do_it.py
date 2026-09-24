"""Lesson 10.1 / s4: The contract: what the model reads of each tool

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (what the model reads of each tool; reads the source, installs nothing)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_where_it_points_and_its_brains
Expected observation: retrieve(query: str, doc_type: str = 'all', top_k: int = 5)    hidden: runtime
      Retrieve grounded passages from DocuMind's corpus.
  calculate_processing_cost(total_pages: int, num_documents: int = 1, processing_type: str = 'standard')
      Estimate document processing cost in USD and INR.
  get_usage_stats(metric: str, days: int = 7)    hidden: runtime
      Get DocuMind RAG pipeline usage statistics.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L465

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (what the model reads of each tool; reads the source, installs nothing).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import ast
    src = open("services/chat/tools.py", encoding="utf-8").read()
    for fn in ast.parse(src).body:
        if isinstance(fn, ast.FunctionDef) and any(getattr(d, "id", "") == "tool" for d in fn.decorator_list):
            a = fn.args.args
            dflt = [None] * (len(a) - len(fn.args.defaults)) + fn.args.defaults
            shown = [f"{x.arg}: {ast.unparse(x.annotation)}" + (f" = {ast.unparse(v)}" if v is not None else "") for x, v in zip(a, dflt) if x.arg != "runtime"]
            hidden = [x.arg for x in a if x.arg == "runtime"]
            print(f"  {fn.name}({', '.join(shown)})" + (f"    hidden: {hidden[0]}" if hidden else ""))
            print(f"      {ast.get_docstring(fn).splitlines()[0]}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
