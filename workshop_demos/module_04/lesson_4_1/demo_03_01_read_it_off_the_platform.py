"""Lesson 4.1 / s3: The plumbing: read the notification, the topic and the subscription off your lane

Summary and purpose:
Read it off the platform

HTML instruction: bash — run in the operator shell (all read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: ---
event_types:
- OBJECT_FINALIZE
id: '1'
payload_format: JSON_API_V1
topic: //pubsub.googleapis.com/projects/documind-ai-YOUR-ID/topics/documind-ingest
ackDeadlineSeconds: 600
deadLetterPolicy:
  deadLetterTopic: projects/documind-ai-YOUR-ID/topics/documind-ingest-dlq
  maxDeliveryAttempts: 12
pushConfig:
  oidcToken:
    serviceAccountEmail: documind-ingest-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
  pushEndpoint: https://documind-ingest-NUMBER.asia-south1.run.app
retryPolicy:
  maximumBackoff: 600s
  minimumBackoff: 10s
projects/documind-ai-YOUR-ID/topics/documind-ingest-dlq
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: '30'
        run.googleapis.com/execution-environment: gen2
    spec:
      containerConcurrency: 1
      timeoutSeconds: 600

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.1-upload-events/Netsetos_GCP_Capstone_4.1_Upload_Events_WIX.html#L448

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud storage buckets notifications list "gs://$PROJECT-uploads" --project "$PROJECT"

gcloud pubsub subscriptions describe documind-ingest-push --project "$PROJECT" \\
  --format='yaml(pushConfig.pushEndpoint,pushConfig.oidcToken.serviceAccountEmail,ackDeadlineSeconds,retryPolicy,deadLetterPolicy)'

gcloud pubsub subscriptions describe ingest-dlq-sub --project "$PROJECT" --format='value(topic)'

gcloud run services describe documind-ingest --region "$REGION" --project "$PROJECT" \\
  --format='yaml(spec.template.spec.timeoutSeconds,spec.template.spec.containerConcurrency,spec.template.metadata.annotations)'
"""


def demonstrate(session):
    """Run Read it off the platform at this checkpoint.

    Read it off the platform

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (all read-only).
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
