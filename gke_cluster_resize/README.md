# How to use it

1) Create a PUB/SUB Topic

   ![Create PUB/SUB Topic](./images/image_1.PNG)

2) Create Cloud Function

   ![Create Cloud Function Basics](./images/image_2.PNG)

   ![Create Cloud Function Runtime](./images/image_3.PNG)

   ![Create Cloud Function Connections](./images/image_4.PNG)


  Paste the content of [gke_cluster_resize.py](./gke_cluster_resize/gke_cluster_resize.py) into the `main.py` file in the console and change the **Entry point** to `main`

  Paste the content of [requirements.txt](./gke_cluster_resize/requirements.txt) into `requirements.txt` file in the console.

   ![Create Cloud Function Connections](./images/image_7.PNG)

   Then click the **Deploy** button.

3) Create Cloud Scheduler jobs

  Create two jobs. One for start and another one for stop clusters.

  The only difference between these two should be the value on **Key 2**
  For starting the cluster, `node_number` should be `1` or more (depends on how many nodes you want to start)

  The **Key 1** attribute -> Specify here what should be the cluster label. All clusters with that label will be scheduled.

   ![Create Cloud Scheduler job](./images/image_5.PNG)

   ![Create Cloud Scheduler job](./images/image_6.PNG)
