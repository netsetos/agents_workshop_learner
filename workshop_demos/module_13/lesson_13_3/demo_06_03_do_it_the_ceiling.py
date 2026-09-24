"""Lesson 13.3 / s6: Off at night, and the ceiling under it

Summary and purpose:
make gpu-cap writes a consumer quota override on the L4 quotas in us-central1, capping them at one card. --max-instances belongs to one service. The quota belongs to the project, so a second GPU service, a GPU candidate or a typo cannot allocate a second card. Lowering a quota needs no approval; raising it again does.

HTML instruction: bash — run in the operator shell, in the kit (lowers one quota; make gpu-cap-off takes it back)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it_the_instances_after_fifteen_minutes
Expected observation: python services/slm/gpu_quota.py --project documind-ai-YOUR-ID --region us-central1 --cap 1

Total NVIDIA L4 GPU allocation without zonal redundancy
  run.googleapis.com/nvidia_l4_gpu_allocation_no_zonal_redundancy
  1/{project}/{region}         us-central1  effective 3 (default 3)
                               -> capped at 1

1 override(s) written. Read back:
  Total NVIDIA L4 GPU allocation without zonal red 1/{project}/{region}       effective 1 (default 3, override 1)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L722

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make gpu-cap PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it: the ceiling at this checkpoint.

    make gpu-cap writes a consumer quota override on the L4 quotas in us-central1, capping them at one card. --max-instances belongs to one service. The quota belongs to the project, so a second GPU service, a GPU candidate or a typo cannot allocate a second card. Lowering a quota needs no approval; raising it again does.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (lowers one quota; make gpu-cap-off takes it back).
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
