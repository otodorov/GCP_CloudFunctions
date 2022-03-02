import asyncio
from google.cloud import container_v1
from google.api_core import retry
from google.api_core import exceptions


project = 'netomedia2'      # Project where the function will operate

client = container_v1.ClusterManagerClient()


def list_gke_clusters(label: str) -> dict:
    '''
    Args:
        label (str) = String in format <key=value> label used to match the cluster

    Return:
        all clusters with labels and their node pools as a map that have specific label
        e.g.: {
            '<cluster_name>-<node_pool_name>': {
                "cluster_name": "<cluster_name>",
                "location": "<location>",
                "labels": "{'key1': 'val1', 'key2': 'val2'}",
                "node_pool": "<node_pool_name>"
            }
        }
    '''

    request = container_v1.ListClustersRequest(
        parent=f"projects/{project}/locations/-"
    )

    response = client.list_clusters(request=request)

    label_key = label.split('=')[0]
    label_value = label.split('=')[1]
    label = (label_key, label_value)

    cluster_dict = {}
    for cluster in response.clusters:
        if (label) in cluster.resource_labels.items():
            for node_pool in cluster.node_pools:
                cluster_dict[f"{cluster.name}({node_pool.name})"] = {
                    "cluster_name": cluster.name,
                    "location": cluster.location,
                    "labels": cluster.resource_labels,
                    "node_pool": node_pool.name
                }

    return cluster_dict


async def resize_gke_node_pool(cluster_dict: dict, node_number: int):
    '''
    Args:
        cluster_name (string): The name of the cluster that owns the node pool
        location (string): The name of the Google Compute Engine zone|region
        pool (string): The name of the node pool to set size
        node_number (intiger): The desired node count for the pool.

    Return:
        cluster_name (string): The name of the cluster that owns the node pool
        node pool (string): The name of the node pool size
        location (string): The name of the Google Compute Engine zone|region
        time (string): The time when the execution started

    name string format: "projects/<project>/locations/<location>/clusters/<cluster_name>/nodePools/<node_pool>"
    '''

    @ retry.Retry(
        initial=1.0,
        deadline=900.0,
        predicate=retry.if_exception_type(exceptions.FailedPrecondition)
    )
    def wrapper(resize_gke_node_pool) -> container_v1.types.Operation:

        request = container_v1.SetNodePoolSizeRequest(
            name=f"projects/{project}/locations/{cluster_dict['location']}/clusters/{cluster_dict['cluster_name']}/nodePools/{cluster_dict['node_pool']}",
            node_count=node_number,
        )

        response = client.set_node_pool_size(
            request=request,
        )

        print(f"""
        cluster_name: {cluster_dict['cluster_name']}
        node pool: {cluster_dict['node_pool']} is set to {node_number}
        location: {cluster_dict['location']}
        time: {response.start_time}
        """)

        return response
    return wrapper(resize_gke_node_pool)


async def main(event, context):
    if 'attributes' in event:
        # CLusters that have this labels will be targeted
        label = event['attributes']['label']
        # Set desrired number for each Cluster Node Pool
        node_number = int(event['attributes']['node_number'])

    for cluster in list_gke_clusters(label):
        task = asyncio.create_task(resize_gke_node_pool(
            list_gke_clusters(label)[cluster], node_number))

    await task


if __name__ == '__main__':
    event = {
        "attributes": {
            "label": "scale=true",
            "node_number": "0"
        }
    }
    asyncio.run(main(event, context=None))
