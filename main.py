from googleapiclient import discovery
# from google.cloud import compute_v1

# instance_client = compute_v1.InstancesClient()
# instance_request = compute_v1.ListInstancesRequest(
#     project="anakatech", zone="europe-west1-d")


def list_instances(compute, project="anakatech", zone="europe-west1-d"):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    compute = discovery.build("compute", "v1")
    # print(instance_client.list(instance_request))
    # a = instance_client.list(instance_request)

    # print(a)
    instances = list_instances(compute, project, zone)
    # instances = instance_client.list(
    #     project="anakatech", zone="europe-west1-d")

    # list_items = []
    # for i in instances.items():
    #     list_items.append(i)
    a = str(instances.items[0])
    print(type(a))
    return(a)

    list_instance

    # str_instances = len(str(instances.items))
    # return str(str_instances)
    # for x in str_instances:
    #     print(str_instances[x])
    # return str(instances.items[0])
