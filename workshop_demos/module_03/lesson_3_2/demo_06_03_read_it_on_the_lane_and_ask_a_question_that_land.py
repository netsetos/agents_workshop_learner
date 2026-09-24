"""Lesson 3.2 / s6: Chunk by window: an Act becomes page windows

Summary and purpose:
Read it on the lane, and ask a question that lands on a page

HTML instruction: bash — run in the operator shell (acme pinned to vector, see the setup)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_read_it_on_the_lane_and_ask_a_question_that_land
Expected observation: 67 windows on the lane; first six: ['p1-0', 'p2-0', 'p2-1', 'p3-0', 'p3-1', 'p4-0']
pages seen: [1, 2, 3, 4, 5] ... 29
Under the Code on Wages, wages must be paid within seven days after the end of the wage period ... [Source 1]
19 code_on_wages_2019.pdf page 9 | (iv) monthly basis, before the expiry of the seventh day of the succ
20 code_on_wages_2019.pdf page 9 | ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L685

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"Within how many days must wages be paid after the wage period ends under the Code on Wages?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:160]); [print(c['chunk_id'].split('#')[1], c['source_uri'].split('/')[-1], 'page', c['page'], '|', c['quote'][:60]) for c in j['citations']]"
"""


def demonstrate(session):
    """Run Read it on the lane, and ask a question that lands on a page at this checkpoint.

    Read it on the lane, and ask a question that lands on a page

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (acme pinned to vector, see the setup).
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
