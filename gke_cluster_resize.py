from multiprocessing.pool import ThreadPool as Pool
from google.cloud import container_v1
from google.api_core import retry
from google.api_core import exceptions


project = 'netomedia2'      # Project where the function will operate
label = ('scale', 'true')   # CLusters that have this labels will be targeted
node_number = 0             # Set desrired number for each Cluster Node Pool
pool_size = 5               # How many clusters at a time will be scheduled

client = container_v1.ClusterManagerClient()


def list_gke_clusters():
    f'''
    Return all clusters with labels and their node pools as a map that have specific label {label}
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
                "location": cluster.location,
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

    request = container_v1.SetNodePoolSizeRequest(
        name=f"projects/{project}/locations/{location}/clusters/{cluster_name}/nodePools/{pool}",
        node_count=node_number,
    )

    response = client.set_node_pool_size(
        request=request,
    )

    print(f"""
    cluster_name: {cluster_name}
    node pool: {pool} is set to {node_number}
    location: {location}
    time: {response.start_time}
    """)
    return response


def main():

    thread_pool = Pool(pool_size)

    for cluster in list_gke_clusters():
        for pool in list_gke_clusters()[cluster]['node_pool']:
            cluster_name = cluster
            location = list_gke_clusters()[cluster]['location']
            node_pool = pool

            thread_pool.apply_async(resize_gke_node_pool, (cluster_name, location,
                                                           node_pool, node_number))

    thread_pool.close()
    thread_pool.join()


main()
