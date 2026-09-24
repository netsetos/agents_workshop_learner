"""Lesson 15.3 / s6: globex stays home: the skip, the ledger row, and a pin the policy overrides

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a note to globex, whose text may not leave India)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: ...
>> gs://documind-ai-YOUR-ID-uploads/globex/globex_visitor_note_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	globex_f03a05df186ad39dec858f13c24a17424d7d35438eb57faf83d2f1144d9aee29	1	0	1	0	
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=globex_visitor_note_2026.md API=<candidate url>

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L747

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """cat > "$HOME/globex_visitor_note.md" <<EOF
# Globex visitor note

Visitors to the Globex office sign the register at reception and wear a visitor badge at all times.

Written by $ME on $(date -u +%Y-%m-%dT%H:%M:%SZ) for lesson 15.3.
EOF
export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make reindex PROJECT="$PROJECT" TENANT=globex FILE="$HOME/globex_visitor_note.md" NAME=globex_visitor_note_2026.md
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a note to globex, whose text may not leave India).
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
