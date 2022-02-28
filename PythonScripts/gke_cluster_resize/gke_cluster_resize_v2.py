from multiprocessing.pool import ThreadPool as Pool
from threading import current_thread
from google.cloud import container_v1
from google.api_core import retry
from google.api_core import exceptions


project = 'netomedia2'      # Project where the function will operate
label = ('scale', 'true')   # CLusters that have this labels will be targeted
node_number = 0             # Set desrired number for each Cluster Node Pool
# How many clusters at a time will be scheduled (Default: pool_size = CPU threads)
pool_size = None


client = container_v1.ClusterManagerClient()


def list_gke_clusters():
    f'''
    Args:
        label (dict) = A JSON formated label used to match the cluster

    Return:
        all clusters with labels and their node pools as a map that have specific label {label}
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
def resize_gke_node_pool(cluster_name, cluster_info):
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

    for pool in cluster_info['node_pool']:
        location = cluster_info['location']

        print(f"Current_thread 1111: {current_thread()}")
        request = container_v1.SetNodePoolSizeRequest(
            name=f"projects/{project}/locations/{location}/clusters/{cluster_name}/nodePools/{pool}",
            node_count=node_number,
        )

        print(request)
        response = client.set_node_pool_size(
            request=request,
        )

        # print(f"""
        # Cluster name: {cluster_name}
        # Node pool: {pool} is set to {node_number}
        # Location: {location}
        # Time: {response.start_time}
        # """)
        # Current_thread: {current_thread()}

        return response


def callback(callback):
    print(callback)
    # print(f"""
    # Cluster name: {cluster_name}
    # Node pool: {pool} is set to {node_number}
    # Location: {location}
    # Time: {callback.start_time}
    # """)
    # Current_thread: {current_thread()}


def error_callback(exception):
    print(exception)


def main():

    thread_pool = Pool()
    for cluster in list_gke_clusters():
        #     # resize_gke_node_pool(cluster, list_gke_clusters()[cluster])

        # Process(target=resize_gke_node_pool, args=(
        #     cluster, list_gke_clusters()[cluster]))
        thread_pool.apply_async(resize_gke_node_pool, (cluster, list_gke_clusters()[cluster]),
                                callback=callback,
                                error_callback=error_callback)
        # print(a)

    thread_pool.close()
    thread_pool.join()


main()
