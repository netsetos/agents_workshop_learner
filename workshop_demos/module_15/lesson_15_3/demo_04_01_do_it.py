"""Lesson 15.3 / s4: The policies, the pins and the stores

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: acme: data_region=any
acme: retrieval_backend=vector
zeta: data_region=any
zeta: retrieval_backend=vertex_search
globex: data_region=in
globex: retrieval_backend=default (the deployment RETRIEVAL_BACKEND)
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID RAG_LOCATION=us-central1 AUDIT_BUCKET=documind-ai-YOUR-ID-audit \\
  python managed.py --project documind-ai-YOUR-ID --status --mode both
{"tenant": "acme", "store": "rag_engine", "ledger_current": 21, "held": 18, "missing": 3, "orphans": 0, "status": "drift", "missing_doc_keys": ["acme_0994e77d201672aa703e6d5a9a00590d117ad98239b319e900a0d6a787ede170", "acme_80403acbbf9b2ada3bb37bfa6983bd864696ed45ca459a5ad7cf0296596ca987", "acme_ef63c85dc631e96e6c46364c3188f3f7a9a9283ad2e88074494d378399e1a71b"], "orphan_doc_keys": []}
{"tenant": "acme", "store": "vertex_search", "ledger_current": 21, "held": 18, "missing": 3, "orphans": 0, "

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L592

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """for t in acme zeta globex; do
  make tenant-policy PROJECT="$PROJECT" TENANT=$t        # where its text may be held
  make tenant-backend PROJECT="$PROJECT" TENANT=$t       # which store answers it
done
make managed-status PROJECT="$PROJECT"                     # every store, held against the ledger
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
