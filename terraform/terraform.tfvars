// Change these information as your GCP ProjectId, region and zone setting
//project_id          = ""
//region              = "us-east1"
//zone                = "us-east1-b"

data_lake_bucket    = "crime_trends_explorer_data_lake"
storage_class       = "STANDARD"
raw_bq_dataset      = "raw_crime_reports"
dev_bq_dataset      = "dev_crime_reports"
prod_bq_dataset     = "prod_crime_reports"
spark_cluster_name  = "crime-trends-explorer-cluster"