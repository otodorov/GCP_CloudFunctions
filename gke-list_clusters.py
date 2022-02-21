from google.cloud import container_v1

# http://localhost:8080?project=anakatech&zone=europe-west1-d

project = 'netomedia2'
# label = ('env', 'qa')
label = ('scale', 'true')
node_count = 0

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


list_gke_clusters()


def resize_gke_node_pool(cluster: tuple, node_count: int):
    '''
    Params:
        cluster: (
            '<cluster_name>', {
                'location': ['<locations>'],
                'labels': {'<key1>': '<value1>', '<key2>': '<value2>'},
                'node_pool': ['<node_pool_1>', '<node_pool_2>']
                }
            )
    name string format: "projects/<project>/locations/<location>/clusters/<cluster_name>/nodePools/<node_pool>"
    '''

    for node_pool in cluster[1]['node_pool']:
        request = container_v1.SetNodePoolSizeRequest(
            name=f"projects/{project}/locations/{cluster[1]['location'][0]}/clusters/{cluster[0]}/nodePools/{node_pool}",
            node_count=node_count,
        )

    response = client.set_node_pool_size(request=request)

    return response


def main():
    for cluster in list_gke_clusters().items():
        resize_gke_node_pool(cluster, node_count)


main()
