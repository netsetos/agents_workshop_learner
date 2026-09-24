"""Lesson 3.4 / s5: Inspect Vector Search: the datapoint, its restricts, and a search for itself

Summary and purpose:
Three things exist: the index, the endpoint, and the deployed index that joins them and is the one that costs money per hour. The kit's make vector-status runs commands/vector-status.sh, which takes the two names from the shell (the variables you exported above) or, failing that, from Terraform's outputs; the two commands below are the same reads by hand.

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_read_all_four_rs_0
Expected observation: displayName: documind-chunks
indexStats:
  shardsCount: 1
  vectorsCount: '1745'
indexUpdateMethod: STREAM_UPDATE
metadata:
  config:
    dimensions: 768
    distanceMeasureType: DOT_PRODUCT_DISTANCE
displayName: documind-endpoint
deployedIndexes:
- dedicatedResources:
    machineSpec:
      machineType: e2-standard-2
  id: documind_chunks_v1
  indexSyncTime: '2026-09-22T10:41:07.000Z'

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L656

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud ai indexes describe "$(basename "$VECTOR_INDEX_NAME")" --region="$REGION" --project="$PROJECT" \\
  --format='yaml(displayName,indexStats.vectorsCount,indexStats.shardsCount,indexUpdateMethod,metadata.config.dimensions,metadata.config.distanceMeasureType)'
gcloud ai index-endpoints describe "$(basename "$VECTOR_INDEX_ENDPOINT")" --region="$REGION" --project="$PROJECT" \\
  --format='yaml(displayName,deployedIndexes[].id,deployedIndexes[].indexSyncTime,deployedIndexes[].dedicatedResources.machineSpec.machineType)'
"""


def demonstrate(session):
    """Run The index and its deployment, as gcloud sees them at this checkpoint.

    Three things exist: the index, the endpoint, and the deployed index that joins them and is the one that costs money per hour. The kit's make vector-status runs commands/vector-status.sh, which takes the two names from the shell (the variables you exported above) or, failing that, from Terraform's outputs; the two commands below are the same reads by hand.

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
