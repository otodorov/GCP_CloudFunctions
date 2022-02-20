# import googleapiclient.discovery
from google.cloud import container_v1

# http://localhost:8080?project=anakatech&zone=europe-west1-d

client = container_v1.ClusterManagerClient()


def list_gke_clusters(client):
    # Create a client

    # Initialize request argument(s)
    request = container_v1.ListClustersRequest(
        # projects/netomedia2/locations/-.
        parent="projects/netomedia2/locations/-"
    )

    # Make the request
    response = client.list_clusters(request=request)

    # cluster_list = []
    # for cluster in response.clusters:
    #   cluster_list.append(cluster.name)

    cluster_list = [cluster_list.name for cluster_list in response.clusters]

    # Handle the response
    return cluster_list


def main():
    print(list_gke_clusters(client))

    for i in list_gke_clusters(client):
        print(f"TEST - {i}")


main()
