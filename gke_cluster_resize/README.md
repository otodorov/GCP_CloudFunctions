# How to use it

1) Create a PUB/SUB Topic

   ![Create PUB/SUB Topic](../images/gke_cluster_resize_1.PNG)

2) Create Cloud Function

   ![Create Cloud Function Basics](../images/gke_cluster_resize_2.PNG)

   ![Create Cloud Function Runtime](../images/gke_cluster_resize_3.PNG)

   ![Create Cloud Function Connections](../images/gke_cluster_resize_4.PNG)

3) Create Cloud Scheduler jobs

  Create two jobs. One for start and another one for stop clusters.

  The only difference between these two should be the value on **Key 2**
  For starting the cluster, `node_number` should be `1` or more (depends on how many nodes you want to start)

  The **Key 1** attribute -> Specify here what should be the cluster label. All clusters with that label will be scheduled.

   ![Create Cloud Scheduler job](../images/gke_cluster_resize_5.PNG)

   ![Create Cloud Scheduler job](../images/gke_cluster_resize_6.PNG)
