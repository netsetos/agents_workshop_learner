"""Lesson 6.4 / s6: Citations: the pills, the sources, and the link signed through IAM

Summary and purpose:
In the browser, under the answer from step 5, open Sources and click Open source on the note. A new tab shows the note's text from the bucket, through a link that stops working in 15 minutes. Then capture the same answer as a transcript and paste it into the renderer in step 1:

HTML instruction: bash — run in the operator shell (one stream, a rupee)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_ask_in_the_browser_ask_from_the_shell_read
Expected observation: citation events: 5 | tokens: NN | done: 1
first citation: pune_visitor_rules.md | kind text | page None | quote 'VR-01 - Badges\\nEvery visitor to the Pune warehou'
...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L678

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What colour badge do visitors wear at the Pune warehouse?","tenant_id":"acme","top_k":5}' > /tmp/stream64.txt
echo "citation events: $(grep -c '^event: citation' /tmp/stream64.txt) | tokens: $(grep -c '^event: token' /tmp/stream64.txt) | done: $(grep -c '^event: done' /tmp/stream64.txt)"
grep -m1 '^data: {"n": 1' /tmp/stream64.txt | cut -c7- \\
  | python -c "import json,sys; d=json.load(sys.stdin); print('first citation:', d['source'].split('/')[-1], '| kind', d['kind'], '| page', d['page'], '| quote', repr(d['quote'][:48]))"
cat /tmp/stream64.txt
"""


def demonstrate(session):
    """Run Do it: open the source, then render your own transcript at this checkpoint.

    In the browser, under the answer from step 5, open Sources and click Open source on the note. A new tab shows the note's text from the bucket, through a link that stops working in 15 minutes. Then capture the same answer as a transcript and paste it into the renderer in step 1:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one stream, a rupee).
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
