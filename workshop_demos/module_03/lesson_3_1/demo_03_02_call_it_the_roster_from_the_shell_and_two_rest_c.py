"""Lesson 3.1 / s3: Tenant: something you are, never something you send

Summary and purpose:
First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again. Now the same question through the API three times. As the UI's account, which is on acme's roster, a query for acme is answered. As the outsider account - a fixture account that IAM admits into the service but no roster lists - the same request gets through Cloud Run's door and is then refused by the roster. With no token at all, Cloud Run's door refuses it before the API ever runs. Both refusals are 403s, so print the body too: the roster's refusal is a one-line JSON from the API, the door's is Cloud Run's HTML page. That difference is the tenant contract at work: the second caller got in, and was still told no.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_call_it_the_roster_from_the_shell_and_two_rest_c
Expected observation: ...,"latency_ms":1840,"stages":{"retrieval_backend":"vector",...},"cache_hit":"none"}
HTTP 200
{"detail":"not a member of this tenant"}
HTTP 403
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title> ...
HTTP 403

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L463

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """# a roster member: answered (the body is the answer; only its first line is shown)
curl -s -w "\\nHTTP %{http_code}\\n" -X POST $API/v1/query \\
  -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false}' | tail -c 200

# the outsider: admitted by IAM, refused by the roster
curl -s -w "\\nHTTP %{http_code}\\n" -X POST $API/v1/query \\
  -H "Authorization: Bearer $(otok)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false}'

# nobody at all: stopped at the door by Cloud Run, before the API runs
curl -s -w "\\nHTTP %{http_code}\\n" -X POST $API/v1/query \\
  -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period?","tenant_id":"acme","stream":false}' | head -c 160
"""


def demonstrate(session):
    """Run Call it: the roster from the shell, and two REST calls at this checkpoint.

    First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again. Now the same question through the API three times. As the UI's account, which is on acme's roster, a query for acme is answered. As the outsider account - a fixture account that IAM admits into the service but no roster lists - the same request gets through Cloud Run's door and is then refused by the roster. With no token at all, Cloud Run's door refuses it before the API ever runs. Both refusals are 403s, so print the body too: the roster's refusal is a one-line JSON from the API, the door's is Cloud Run's HTML page. That difference is the tenant contract at work: the second caller got in, and was still told no.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
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
