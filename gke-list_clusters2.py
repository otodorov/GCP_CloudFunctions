from google.cloud import container_v1
from google.api_core import retry
from google.api_core import exceptions


# http://localhost:8080?project=anakatech&zone=europe-west1-d

project = 'netomedia2'
# label = ('env', 'qa')
label = ('scale', 'true2')
node_number = 0

client = container_v1.ClusterManagerClient()


def list_gke_clusters():
    f'''
    List all clusters with labels and their node pools as a map that have specific label {label}
    e.g.: {{'<cluster_name>': [['<region>'], {{'key1': 'val1', 'key2': 'val2'}}, '<node_pool_name>']}}
    '''

    request = container_v1.ListClustersRequest(
        parent=f"projects/{project}/locations/-"
    )

    response = client.list_clusters(request=request)

    cluster_dict = {}
    for cluster in response.clusters:
        if (label) in cluster.resource_labels.items():
            cluster_dict[cluster.name] = {
                "location": cluster.locations,
                "labels": cluster.resource_labels,
                "node_pool": [node_pool.name for node_pool in cluster.node_pools],
            }

    return cluster_dict


@retry.Retry(initial=1.0,
             deadline=900.0,
             predicate=retry.if_exception_type(exceptions.FailedPrecondition)
             )
def resize_gke_node_pool(cluster_name, location, pool, node_number):
    '''
    Args:
        cluster_name (string):
        location (list):
        labels (string):
        node_pool (list):
        '<cluster_name>', {
            'location': ['<locations>'],
            'labels': {'<key1>': '<value1>', '<key2>': '<value2>'},
            'node_pool': ['<node_pool_1>', '<node_pool_2>']
            }

    name string format: "projects/<project>/locations/<location>/clusters/<cluster_name>/nodePools/<node_pool>"
    '''

    request = container_v1.SetNodePoolSizeRequest(
        name=f"projects/{project}/locations/{location}/clusters/{cluster_name}/nodePools/{pool}",
        node_count=node_number,
    )

    response = client.set_node_pool_size(
        request=request,
    )

    print(response)
    return response


def main():
    for cluster in list_gke_clusters():
        print("cluster:", cluster)
        for pool in list_gke_clusters()[cluster]['node_pool']:
            cluster_name = cluster
            location = list_gke_clusters()[cluster]['location'][0]
            node_pool = pool

            resize_gke_node_pool(cluster_name, location,
                                 node_pool, node_number)

    # TODO: Fix request retry
    # TODO: Add multithreading for clusters
main()
