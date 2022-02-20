
def list_instances(compute, project, zone):
    result = f"compute={compute} project={project} zone={zone}"
    print(compute)
    print(project)
    print(zone)
    return result


def main():
    compute = "test"
    project = "anakatech"
    zone = "europe-west1-d"

    instances = list_instances(compute, project, zone)
    print("TEST", instances)


main()
