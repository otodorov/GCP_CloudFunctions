# import googleapiclient.discovery
from google.cloud import container_v1

# http://localhost:8080?project=anakatech&zone=europe-west1-d

# Create a client
client = container_v1.ClusterManagerClient()


def list_gke_clusters(client):

    # Initialize request argument(s)
    request = container_v1.ListClustersRequest(
        # projects/netomedia2/locations/-.
        parent="projects/netomedia2/locations/-"
    )

    # Make the request
    response = client.list_clusters(request=request)

    # Handle the response
    # gke_clusters = []
    return str(response)


list_gke_clusters(client)

# def list_gke_cluster_node_pools():
#     # Create a client
#     client = container_v1.ClusterManagerClient()

#     # Initialize request argument(s)
#     request = container_v1.ListNodePoolsRequest(
#       # `projects/*/locations/*/clusters/*``.
#       parent = "projects/netomedia2/locations/-"
#     )

#     # Make the request
#     response = client.list_node_pools(request=request)

#     # Handle the response
#     # return str(response)
#     print(response)
