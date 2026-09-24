"""Lesson 15.3 / s5: Ask the stores, and find who found the cited chunk

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (acme's pin back to RAG Engine, then one question for each tenant)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: acme: retrieval_backend=rag_engine
acme: retrieval_backend rag_engine, policy_fallback 0; pool 17, 14 from a managed store
  A: A confirmed employee at grade E3 or above serves a notice period of 60 days [2].
  cites acme:acme_497809ff...#rag-c31c1f459b60 (hr_policy_2026.md)
zeta: retrieval_backend vertex_search, policy_fallback 0; pool 12, 12 from a managed store
  A: A confirmed employee at grade L4 or above serves a notice period of 30 days [1].
  cites zeta:zeta_e920a147...#vs-9b9cb379153b (hr_policy_zeta_2026.md)
globex: retrieval_backend vector, policy_fallback 0; pool 20, 0 from a managed store
  A: Either party may terminate the agreement for convenience on 120 days' written notice [1].
  cites globex:a0d13745...#2 (msa_globex_2026.md)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L649

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make tenant-backend PROJECT="$PROJECT" TENANT=acme RETRIEVAL_BACKEND=rag_engine     # make up's pin, back
sleep 60      # the API reads a tenant's settings once a minute per instance
ask153() {   # ask153 TENANT...: each tenant's question as documind-ui-sa - the store that served, the answer, the cited chunk
python - "$@" <<'PY'
import json, os, re, subprocess, sys, urllib.request
P, API = os.environ["PROJECT"], os.environ["API"]
Q = {"acme": "How long is the notice period for a confirmed employee?", "zeta": "How long is the notice period for a confirmed employee?",
     "globex": "How much notice does either party give to end the Globex agreement for convenience?"}
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
short = lambda cid: re.sub(r"([0-9a-f]{8})[0-9a-f]{56}", r"\\1...", cid)      # the version's sha256, cut to 8
for t in sys.argv[1:]:
    req = urllib.request.Request(API + "/v1/query", data=json.dumps({"query": Q[t], "tenant_id": t}).encode(),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    a = json.load(urllib.request.urlopen(req, timeout=180))
    s = a["stages"]
    print(f"{t}: retrieval_backend {s['retrieval_backend']}, policy_fallback {s['policy_fallback']}; pool {s['pool']}, {s['managed_chunks']} from a managed store")
    print(f"  A: {a['answer']}")
    for c in a["citations"]:
        print(f"  cites {short(c['chunk_id'])} ({c['source_uri'].rsplit('/', 1)[-1]})")
PY
}
ask153 acme zeta globex
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (acme's pin back to RAG Engine, then one question for each tenant).
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
