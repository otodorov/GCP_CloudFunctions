from google.cloud import container_v1

project = 'netomedia2'
label = ('env', 'qa')

client = container_v1.ClusterManagerClient()


def list_gke_clusters(client):
    request = container_v1.ListClustersRequest(
        parent=f"projects/{project}/locations/-"
    )

    response = client.list_clusters(request=request)

    cluster_dict = {}
    for cluster in response.clusters:
        if (label) in cluster.resource_labels.items():
            cluster_dict[cluster.name] = [
                cluster.locations,
                cluster.resource_labels
            ]

    return cluster_dict


def list_gke_node_pools(client, cluster):

    request = container_v1.ListNodePoolsRequest(
        #response = client.list_node_pools(parent="projects/netomedia2/locations/europe-west1-b/clusters/qa-karma-cluster/*")
        parent=f"projects/{project}/locations/-/clusters/{cluster}/*"
    )

    # Make the request
    response = client.list_node_pools(request=request)

    # Handle the response
    print(response)


def main():
    print(list_gke_clusters(client))

    for i in list_gke_clusters(client):
        print(f"TEST - {i}")


main()
