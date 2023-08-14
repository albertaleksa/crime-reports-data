output "temp_bucket" {
  value =google_dataproc_cluster.dataproc-cluster.cluster_config[0].temp_bucket
}