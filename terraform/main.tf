terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${var.data_lake_bucket}_${var.project_id}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id = var.raw_bq_dataset
  project    = var.project_id
  location   = var.region
}

resource "google_bigquery_dataset" "dev_dataset" {
  dataset_id = var.dev_bq_dataset
  project    = var.project_id
  location   = var.region
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id = var.prod_bq_dataset
  project    = var.project_id
  location   = var.region
}

resource "google_dataproc_cluster" "dataproc-cluster" {
  name = var.spark_cluster_name
  project = var.project_id
  region = var.region

  cluster_config {

    master_config {
      num_instances = 1
      machine_type = "n1-standard-4"
      disk_config {
        boot_disk_type = "pd-standard"
        boot_disk_size_gb = 500
      }
    }

    # Override or set some custom properties
    software_config {
      image_version = "2.0-debian10"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
    }


  }
}