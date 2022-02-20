import googleapiclient.discovery

# http://localhost:8080?project=anakatech&zone=europe-west1-d


def list_instances(compute, project, zone):
    # result = compute.instances().list(project, zone).execute()
    result = compute.instances().list(project=project, zone=zone).execute()
    # return result['items'] if 'items' in result else None
    # result = f"A compute={compute} project={project} zone={zone}"
    return result


def main(request):
    compute = googleapiclient.discovery.build('compute', 'v1')
    project = "netomedia2"
    zone = "europe-west1-d"

    # instances = compute.instances().list(
    #     project=project, zone=zone).execute()


#     # return str(instances_list)

    instances = list_instances(compute, project, zone)
    instances_list = []
    for instance in instances['items']:
        instances_list.append(instance['name'])

    return str(instances_list)
