import asyncio
import google.auth
from googleapiclient.discovery import build
from google.api_core import retry_async
from google.api_core import exceptions

# authenticate and build the Cloud SQL API client
creds, project_id = google.auth.default()
sql_client = build('sqladmin', 'v1beta4', credentials=creds)

# function that lists all SQL instances with the given labels
def list_sql_instances(label: str, policy_filter: str) -> list:
    """
    Returns list of SQL instance filtered by the given labels and running state.
    Each label should be in the format 'key=value'.

    Args:
        label (string): String representing SQL instance labels in format key=value
        policy_filter (string): String representing instance state start/stop

    Return:
        sql_instance_list (list): List of strings representing SQL instances'
    """

    # list all SQL instances in the project
    sql_instances = sql_client.instances().list(project=project_id, filter=f"state:RUNNABLE {policy_filter}").execute()

    # filter the instances by the given labels
    sql_instance_list = []
    if sql_instances:
        for instance in sql_instances['items']:
            if (label) in instance['settings']['userLabels'].items():
                sql_instance_list.append(instance['name'])
    return sql_instance_list

@retry_async.AsyncRetry(initial=1.0, deadline=900.0, predicate=retry_async.if_exception_type(exceptions.FailedPrecondition))
async def start_stop_instance(label: str, action: str) -> None:
    """
    Starts or stops a Cloud SQL instance based on the given event.

    Args:
        label (string): String representing SQL instance labels in format key=value
        action (string): String representing instance state start/stop

    Return:
        None
    """
    label_key = label.split('=')[0]
    label_value = label.split('=')[1]
    label = (label_key, label_value)

    if action == 'start':
        policy = 'ALWAYS'
        policy_filter = 'settings.activationPolicy:NEVER'
    elif action == 'stop':
        policy = 'NEVER'
        policy_filter = 'settings.activationPolicy:ALWAYS'

    sql_instances = list_sql_instances(label, policy_filter)
    print(f"List of SQL instances for {action}:", sql_instances)

    database_instance_body = {
        "settings": {
            "activationPolicy": policy
        }
    }

    # perform the start or stop action on each instance
    for instance in sql_instances:
        sql_client.instances().patch(project=project_id, instance=instance, body=database_instance_body).execute()
        print(f"{action} SQL instance: \"{instance}\"")

async def execute(event: dict) -> None:
    """
    Executes the start_stop_instance function
    Args:
        event: dict with keys 'attributes' (dict) and 'action' (string)
    Return:
        None
    """
    if 'attributes' in event:
        # SQL Instances that have this labels will be targeted
        label = event['attributes']['label']
        action = event['attributes']['action']
    await start_stop_instance(label, action)

def main(event, context):
    asyncio.run(execute(event))

if __name__ == '__main__':
    event = {
        "attributes": {
            "label": "scale=true",
            "action": "stop"
        }
    }
    main(event, None)
