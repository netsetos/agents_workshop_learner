"""Lesson 6.4 / s4: The upload: a note you write, uploaded in the browser, followed to the ledger

Summary and purpose:
First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault.

HTML instruction: bash — run in the operator shell (writes one small file in your home directory)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_service_s_account_iap_s_flag_who_may_s
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L527

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """cat > "$HOME/pune_visitor_rules.md" <<EOF
# Pune warehouse visitor rules

Synthetic note for lesson 6.4, uploaded through the DocuMind UI. Every fact is invented.

## VR-01 - Badges

Every visitor to the Pune warehouse wears an amber badge, issued at gate 2 against a photo identity card and returned at the same gate.

## VR-02 - Escorts

A visitor is escorted at all times by the host who signed them in, and visitors do not enter the loading dock.

Uploaded through the UI for lesson 6.4 by $ME on $(date -u +%F).
EOF
sha256sum "$HOME/pune_visitor_rules.md" | cut -c1-12; cat "$HOME/pune_visitor_rules.md"
"""


def demonstrate(session):
    """Run Do it: write the note, upload it in the browser, follow it at this checkpoint.

    First write the note on the operator machine. The page's file picker opens the computer your browser runs on, so the note has to get there. In a Cloud Workstation or the Cloud Shell editor, right-click the file in the explorer and choose Download. In a plain terminal, paste the printed text into a new file with any editor. A pasted copy can differ in its line endings, and then its hash differs from the one printed here. That is the version contract from lesson 3.1 at work, not a fault.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (writes one small file in your home directory).
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
