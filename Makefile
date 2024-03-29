SHELL := /bin/bash

include .env

# Activate service account
activate-sa:
	bash ./setup/activate_service_account.sh


# Terraform
# Initialize terraform
terraform-init:
	terraform -chdir="./terraform" init -var="region=${REGION}" -var="zone=${ZONE}"

# Build a deployment plan
terraform-plan:
	terraform -chdir="./terraform" plan -var="project_id=${PROJECT_ID}" -var="region=${REGION}" -var="zone=${ZONE}"

# Deploy the infrastructure
terraform-apply:
	terraform -chdir="./terraform" apply -var="project_id=${PROJECT_ID}" -var="region=${REGION}" -var="zone=${ZONE}" -auto-approve
	$(MAKE) update-env-temp-bucket
	$(MAKE) update-env-gcs-name

# Delete infrastructure
terraform-destroy:
	terraform -chdir="./terraform" destroy -var="project_id=${PROJECT_ID}" -var="region=${REGION}" -var="zone=${ZONE}" -auto-approve


# Update a value of the DATAPROC_TEMP_BUCKET variable in the .env file
update-env-temp-bucket:
	@MY_VARIABLE=$$(terraform -chdir="./terraform" output temp_bucket) && \
	sed -i '/^DATAPROC_TEMP_BUCKET=/d' .env && \
	echo "DATAPROC_TEMP_BUCKET=$$MY_VARIABLE" >> .env

# Update a value of the DATA_LAKE_BUCKET_NAME variable in the .env file
update-env-gcs-name:
	@MY_VARIABLE=$$(terraform -chdir="./terraform" output gcs_name) && \
	sed -i '/^DATA_LAKE_BUCKET_NAME=/d' .env && \
	echo "DATA_LAKE_BUCKET_NAME=$$MY_VARIABLE" >> .env


# Build docker image for Data Pipeline
docker-build:
	docker build -t crime-trends:v001 .

# Build docker image for Data Pipeline without caching
docker-build-no-cache:
	docker build -t crime-trends:v001 --no-cache --progress plain .


# Start docker-compose
docker-up:
	docker-compose up -d

# Stop docker-compose
docker-down:
	docker-compose down

# To watch agent's logs
docker-agent-logs:
	docker logs -f my-crime-trends-agent

# Run python script to create blocks for Prefect
create-block:
	docker-compose exec my-crime-trends-container \
		python flows/blocks/make_gcp_blocks.py

# Create a Prefect Flow deployment to ingest data
ingest-data:
	docker-compose exec my-crime-trends-container \
		python flows/deploy_ingest.py \
		--name crime-trends-explorer \
		--params="{\"aus_url\": \"https://data.austintexas.gov/api/views/fdj4-gpfu/rows.csv\", \
		\"la_url_1\": \"https://data.lacity.org/api/views/63jg-8b9z/rows.csv\", \
		\"la_url_2\": \"https://data.lacity.org/api/views/2nrs-mtv8/rows.csv\", \
		\"sd_url\": \"https://seshat.datasd.org/pd/pd_calls_for_service\", \
		\"temp_gcs_bucket\": \"${DATAPROC_TEMP_BUCKET}\", \
		\"input_path_aus\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/aus/aus_2003_2023.csv\", \
		\"output_path_aus\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/pq/aus/\", \
		\"output_bq_aus\": \"raw_crime_reports.austin_crimedata\", \
		\"input_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/la/*.csv\", \
		\"input_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/la/*.csv\", \
		\"output_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/pq/la/\", \
		\"output_bq_la\": \"raw_crime_reports.la_crimedata\", \
		\"input_path_sd\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/sd/\", \
		\"output_path_sd\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/pq/sd/\", \
		\"output_bq_sd\": \"raw_crime_reports.sd_crimedata\"}"

# Create a Prefect Flow deployment to ingest data by schedule
ingest-data-schedule:
	docker-compose exec my-crime-trends-container \
		python flows/deploy_ingest.py \
		--name crime-trends-explorer \
		--params="{\"aus_url\": \"https://data.austintexas.gov/api/views/fdj4-gpfu/rows.csv\", \
		\"la_url_1\": \"https://data.lacity.org/api/views/63jg-8b9z/rows.csv\", \
		\"la_url_2\": \"https://data.lacity.org/api/views/2nrs-mtv8/rows.csv\", \
		\"sd_url\": \"https://seshat.datasd.org/pd/pd_calls_for_service\", \
		\"temp_gcs_bucket\": \"${DATAPROC_TEMP_BUCKET}\", \
		\"input_path_aus\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/aus/aus_2003_2023.csv\", \
		\"output_path_aus\": \"gs://${DATA_LAKE_BUCKET_NAME}r/data/pq/aus/\", \
		\"output_bq_aus\": \"raw_crime_reports.austin_crimedata\", \
		\"input_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/la/*.csv\", \
		\"input_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/la/*.csv\", \
		\"output_path_la\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/pq/la/\", \
		\"output_bq_la\": \"raw_crime_reports.la_crimedata\", \
		\"input_path_sd\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/raw/sd/\", \
		\"output_path_sd\": \"gs://${DATA_LAKE_BUCKET_NAME}/data/pq/sd/\", \
		\"output_bq_sd\": \"raw_crime_reports.sd_crimedata\"}" \
		--cron "0 2 * * *"

dbt-dev:
	docker-compose exec \
		-w /app/dbt_crime \
		my-crime-trends-container \
		dbt build --profiles-dir /app/

dbt-prod:
	docker-compose exec \
		-w /app/dbt_crime \
		my-crime-trends-container \
		dbt build -t prod \
		--vars 'is_test_run: false' \
		--profiles-dir /app/