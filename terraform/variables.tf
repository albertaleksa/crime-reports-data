variable "data_lake_bucket" {
  description = "data_lake_bucket"
  type        = string
}

variable "project_id" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
}

variable "raw_bq_dataset" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
}

variable "dev_bq_dataset" {
  description = "BigQuery Dataset that development data (from GCS) will be written to"
  type = string
}

variable "prod_bq_dataset" {
  description = "BigQuery Dataset that production data (from GCS) will be written to"
  type = string
}

variable "spark_cluster_name" {
  description = "DataProc cluster name"
}