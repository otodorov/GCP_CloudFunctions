from google.cloud import container_v1

# http://localhost:8080?project=anakatech&zone=europe-west1-d

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
                cluster.resource_labels,
                # cluster.node_pools[0].name,
                cluster.node_pools,
                # cluster.node_pools = [ cluster.node_pools for cluster.node_pools ]
            ]

    return cluster_dict


def main():
    print(list_gke_clusters(client))


main()
