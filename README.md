# CrimeTrendsExplorer: A Multi-City Crime Analysis Project
Final Project for Data Engineering Zoomcamp Course

![dashboard.png](/images/dashboard.png)

## Table of contents

- [Problem Description](#problem-description):
  - [Objective](#objective)
  - [Data Sources](#data-sources)
  - [Data Processing](#data-processing)
  - [Data Storage](#data-storage)
  - [Analysis and Visualization](#analysis-and-visualization)
- [Technologies & Tools](#technologies--tools)
- [Data Pipeline Architecture diagram](#data-pipeline-architecture-diagram)
- [Pipeline explanation](#pipeline-explanation)
- [Dashboard & Results](#dashboard--results)
- [How to reproduce](#how-to-reproduce)
  - [Step 1. Set Up Cloud Environment. Using Google Console and local terminal](#step-1-set-up-cloud-environment-using-google-console-and-local-terminal)
  - [Step 2. Set Up Cloud Environment. Using VM Terminal](#step-2-set-up-cloud-environment-using-vm-terminal)
  - [Step 3. Run Terraform to deploy your infrastructure to your Google Cloud Project **(In Remote VM)**](#step-3-run-terraform-to-deploy-your-infrastructure-to-your-google-cloud-project-in-remote-vm)
  - [Step 4. Install Spark in VM (Optional. Data pipeline will work in Docker container)](#step-4-install-spark-in-vm--optional-data-pipeline-will-work-in-docker-container--)
  - [Step 5. Run pipeline using Prefect](#step-5-run-pipeline-using-prefect-for-orchestration-in-docker-container-which-copy-datasets-from-web-to-google-cloud-storage-then-save-in-parquet-save-to-big-query-and-process-using-dbt-in-remote-vm)
  - [Step 6. dbt transformation data in BigQuery](#step-6-dbt-transformation-data-in-bigquery-in-remote-vm)
- [Future Improvements](#future-improvements)
- [Credits](#credits)

---

## Problem Description: CrimeTrendsExplorer - A Multi-City Crime Analysis Project

The CrimeTrendsExplorer is a comprehensive data engineering project aimed at processing, analyzing, and exploring crime records data for three major cities in the United States: Austin, Los Angeles, and San Diego. The project covers several years of data, providing valuable insights and trends that can help law enforcement agencies, city planners, researchers, and the general public make informed decisions.

### Objective
The primary goal of the CrimeTrendsExplorer project is to build a robust data pipeline that ingests, processes, and transforms raw crime data from multiple sources, and stores the results in a highly accessible, structured, and queryable format. The project will involve various data engineering tasks, including data ingestion, data cleaning, data validation, data transformation, and data storage.

### Data Sources
The crime records data will be obtained from the following sources:

1. Austin: Austin Police Department's Public Data Portal (https://data.austintexas.gov/)
2. Los Angeles: Los Angeles Open Data Portal (https://data.lacity.org/)
3. San Diego: San Diego Data Portal (https://data.sandiego.gov/)

### Data Processing
The raw crime data will be processed using Apache Spark, which provides a highly scalable and distributed computing framework for big data processing. The pipeline will involve the following steps:

1. Ingest raw crime data from multiple sources in various formats (CSV, JSON, etc.).
2. Perform data cleaning, validation, and preprocessing to ensure data consistency and integrity.
3. Transform and enrich the data, extracting relevant features and aggregating the data as needed.
4. Write the processed data to a partitioned and clustered table in Google BigQuery for efficient querying and analysis.

### Data Storage
The processed crime data will be stored in Google BigQuery, a highly-scalable and fully-managed data warehouse solution that enables fast and efficient querying and analysis. The data will be partitioned and clustered to optimize query performance, and the schema will be designed to support easy exploration and analysis of the data.

# Analysis and Visualization
The CrimeTrendsExplorer project will provide a foundation for further analysis and visualization of the crime data. The processed data can be used to generate insights and trends, such as identifying high-crime areas, understanding seasonal patterns, and exploring the relationship between different types of crimes. 

For visualization purposes, the project will utilize Looker (Google Data Studio), a powerful and user-friendly data visualization tool that integrates seamlessly with Google BigQuery. Looker enables users to create interactive charts, dashboards, and reports, allowing them to explore the data and derive actionable insights without the need for extensive technical expertise. Users can customize and share their visualizations, making it easy for stakeholders to access and interpret the data.

By leveraging modern data engineering technologies and best practices, the CrimeTrendsExplorer project aims to create a powerful platform for understanding and exploring crime patterns in major cities, ultimately contributing to a safer and more informed society.

_[Back to the top](#table-of-contents)_

## Technologies & Tools

1. **Apache Spark**: A highly scalable and distributed computing framework for big data processing, used for data ingestion, cleaning, transformation, and enrichment.
2. **Docker**: A platform for developing, shipping, and running applications in containers, enabling consistent and portable deployment across environments.
3. **Docker Compose**: A tool for defining and running multi-container Docker applications, simplifying the management and orchestration of containers.
4. **Google BigQuery**: A highly-scalable and fully-managed data warehouse solution that provides fast and efficient querying and analysis.
5. **Google Cloud Storage**: A highly-durable and scalable object storage service for storing and managing data.
6. **Google Cloud DataProc**: A fully-managed service for running Apache Spark and other big data processing tools on Google Cloud.
7. **Prefect**: A workflow management system for building, scheduling, and monitoring data pipelines, used for orchestrating the various tasks in the project.
8. **dbt (Data Build Tool)**: A modern data transformation tool for data warehouses, used for transforming and modeling data in BigQuery.
9. **Python**: A versatile programming language used for various data engineering tasks, such as writing Apache Spark jobs and Prefect flows.
10. **Looker (Google Data Studio)**: A powerful and user-friendly data visualization tool that integrates with Google BigQuery for creating interactive charts, dashboards, and reports.
11. **Terraform**: An infrastructure-as-code tool for provisioning and managing cloud resources, used for automating the creation and configuration of Google Cloud resources.

These technologies and tools were employed throughout the CrimeTrendsExplorer project to create a robust, efficient, and scalable data pipeline, as well as to enable effective analysis and visualization of the processed crime data.


_[Back to the top](#table-of-contents)_

## Data Pipeline Architecture diagram

![data_engineering_architecture.png](/images/data_engineering_architecture.png)


_[Back to the top](#table-of-contents)_

## Pipeline explanation

This project processes crime records data for 3 cities (Austin, Los Angeles, and San Diego) for several years, providing insights and analysis of crime trends across these cities.

1. **Data Ingestion**: In this stage, the raw crime data from the respective cities is fetched from various web sources as CSV files. The raw data is then stored in Google Cloud Storage, along with the Python file containing the Apache Spark job.

2. **Data Transformation**: The raw data is processed using Apache Spark, running on a DataProc Cluster. The Spark job performs tasks such as data cleaning, transformation, enrichment, and partitioning. The transformed data is then directly loaded into Google BigQuery, a fully-managed data warehouse solution.

3. **Data Modeling**: The transformed data is further processed using dbt (Data Build Tool) to create meaningful and structured data models in Google BigQuery.

4. **Data Partitioning & Clustering**: The data is partitioned and clustered in BigQuery to optimize query performance and storage efficiency. Partitioning is done on a monthly basis, while clustering is done on a daily basis.

5. **Data Visualization**: The processed and modeled data in BigQuery is then used to create interactive visualizations, charts, and dashboards in Looker (Google Data Studio), enabling users to explore and analyze crime trends across cities.

6. **Pipeline Orchestration**: The entire pipeline is orchestrated using Prefect, a workflow management system that schedules, manages, and monitors the various tasks in the pipeline, ensuring the smooth and efficient operation of the data pipeline.

7. **Dockerization**: All components of the project, including the Spark job, Prefect pipeline, and dbt, are dockerized to ensure a consistent and portable environment for development, testing, and deployment.

This pipeline allows for the efficient processing and analysis of large-scale crime data, enabling users to explore trends, patterns, and insights across multiple cities and timeframes.

_[Back to the top](#table-of-contents)_

## Dashboard & Results

![dashboard.png](/images/dashboard.png)

### Results:
- Over the last 4 years, the number of crimes per month has remained relatively stable.
- The number of crimes in Austin has not shown any significant increase or decrease over the analyzed period.
- In Los Angeles, there has been an increase in the number of crimes in the last 2 years.
- Conversely, San Diego has experienced a decrease in the number of crimes over the past 2 years.
- The raw data for Austin and Los Angeles have similar types, which allows for a comparison between the two cities.
- However, the raw data for San Diego is of a different type compared to the other cities, making a direct comparison with Austin and Los Angeles not feasible.

_[Back to the top](#table-of-contents)_

## How to reproduce

### Step 1. Set Up Cloud Environment. Using Google Console and local terminal
1. Create an **account** on **Google's Cloud platform** with your Google email ID (if you don't have one).
2. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a **new project**.
Copy Project ID (in my case it was: `crime-trends-explorer`) and press `Create`.

    ![create_project](/images/01_create_project.png)

    Then choose to use your new project:
![change_project](/images/01_change_project.png)
3. Create **Service Account** for this project:
   * Go to `IAM & Admin` -> `Service accounts` -> `Create Service Account`
   * Name: **crime-trends-explorer-user**
   * Grant those roles to this account:
     * `Viewer`
     * `BigQuery Admin`
     * `Storage Admin`
     * `Storage Object Admin`
     * `Dataproc Administrator`
     * `Service Account User`
   * After pressing `Done` click Actions on created account and choose `Manage keys`:
     * `Add key` -> `Create new key` -> `JSON` -> `Create`
     * Create New Key for this account (json)
   * Download created service-account-key, rename it to `crime-trends-explorer-user-key.json` and put it in `~/.gc` dir (create folder if needed). It's for convenient. Then we'll put it into our VM.
4. Enable these **APIs** for your project:
   * [Identity and Access Management (IAM) API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
   * [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)
   * Compute Engine API (You'll find it when choose `Compute Engine` menu)
   * [Cloud Dataproc API](https://console.cloud.google.com/marketplace/product/google/dataproc.googleapis.com)
5. Generate **SSH keys** to login to VM instances. This will generate a 2048 bit rsa ssh keypair, named `gcp` and a comment of `de_user`. The comment (`de_user`) will be the user on VM :
   * In terminal:
   ```
   cd ~/.ssh
   ssh-keygen -t rsa -f ~/.ssh/gcp -C de_user -b 2048
   ```
   * Put generated public key to google cloud:
    (`Compute Engine` -> `Metadata` -> `SSH Keys` -> `Add ssh key`) and copy all from file `gcp.pub`. If you already have SSH key to work with your gcp, you can use it.

6. Create **Virtual Machine** Instance (`Compute Engine` -> `VM Instances` -> `Create Instance`).
    ```
    Name: whatever name you would like to call this VM (crime-vm)
    Region, Zone: select a region near you, same with Zone (us-east1-b)
    Machine type: Standard, 4vCPu, 16 GB Memory (e2-standard-4)
    Operating system: Ubuntu
    Version: Ubuntu 20.04 LTS
    Boot disk size: 30Gb.
    ```
    ![vm_name](/images/01_vm_name.png)
    ![vm_disk](/images/01_vm_disk.png)

    When VM is created, note the external IP address.

7. Connect to created VM from terminal (Copy an external ip of created VM): 
    ```
    ssh -i ~/.ssh/gcp de_user@<external_ip_you_copied>
    ```
   You can also update or create a **config file** in your ~/.ssh folder, inputing the external IP address of your VM. This will allow you to just do `ssh crime-vm` to login to your VM
   ```
   $ cd ~/.ssh/
   # Create config file (or open if exists)
   $ touch config
   ```
   Add:
   ```
   Host crime-vm
    Hostname <external_ip_you_copied>
    User de_user
    IdentityFile ~/.ssh/gcp
   ```
   Then you can run `ssh crime-vm` to connect to this VM.

### Step 2. Set Up Cloud Environment. Using VM Terminal
1. **Connect** to remote VM:
   ```
   ssh crime-vm
   ```
2. In VM **clone** repository and `cd` into it:
    ```
    git clone https://github.com/albertaleksa/crime-reports-data.git
    cd crime-reports-data
    ```
3. Run bash script to install software in VM:
    ```
    bash ./setup/setup.sh
    ```
   This will :
   * **update** system
   * download and install **Anaconda**. 
   * install **Docker**
   * Give permission to run **docker** commands **without sudo** in VM
   * Install **docker-compose**
   * Install **Terraform**
   * Install **make**

4. **IMPORTANT**: Log out and log back in so that your group membership is re-evaluated.

5. **Check** if **docker** works:
    ```
    docker run hello-world
    ```
    Check docker-compose version:
    ```
    docker-compose version
    ```
6. **(From local terminal)** Copy service-account-key `crime-trends-explorer-user-key.json` from `~/.gc` to our VM. It'll make possible to work with our Google Cloud from VM using this service account: 
    ```
    scp ~/.gc/crime-trends-explorer-user-key.json de_user@crime-vm:~/.gc/
    ```
   Also copy this key to your folder with project in VM.
7. **(In Remote VM)** Configure gcloud with your service account .json file:
   - If needed change **<path-to-your-key-file>** in file `setup/activate_service_account.sh` to your value
   - Run command:
       ```
      bash ./setup/activate_service_account.sh
      ```
   - Log out and log back

### Step 3. Run Terraform to deploy your infrastructure to your Google Cloud Project **(In Remote VM)**

0) If needed you can change variables in `terraform.tfvars` (change region,..)

1) Initialize terraform:
    ```
    terraform -chdir="./terraform" init
    ```
2) Build a deployment plan (change `crime-trends-explorer` to your `project_id` if needed):
    ```
    terraform -chdir="./terraform" plan -var="project_id=crime-trends-explorer"
    ```
3) Apply the deployment plan and deploy the infrastructure (change `crime-trends-explorer` to your `project_id` if needed). If needed type `yes` to accept actions:
    ```
    terraform -chdir="./terraform" apply -var="project_id=crime-trends-explorer"
    ```
4) Go to Google Cloud Console to make sure that infrastructure is created:
    - Google Cloud Storage:
   ![03_bucket.png](/images/03_bucket.png)
    - BigQuery:
   ![03_bigquery.png](/images/03_bigquery.png)
    - DataProc:
   ![03_dataproc.png](/images/03_dataproc.png)
5) Copy a Dataproc temp bucket name from gcs buckets to file `.env` in field `DATAPROC_TEMP_BUCKET`.

### Step 4. Install Spark in VM (Optional. Data pipeline will work in Docker container).
1. In VM Remote run:
    ```
    bash ./crime-reports-data/setup/install_spark.sh
    ```
2. **IMPORTANT**: Log out and log back in.
3. Go to work dir and create `lib` folder and download GCS connector:
```
cd ~/crime-reports-data/flows/
mkdir lib
cd lib
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar
```

### Step 5. Run pipeline using Prefect for orchestration in Docker Container which copy datasets from web to Google Cloud Storage, then save in parquet, save to Big Query and process using dbt **(In Remote VM)**
1) Build Docker image in Remote VM:
    ```
    make docker-build
    ```
2) Run docker-compose in background. It starts Prefect Orion Server, Prefect Agent, Prefect db and container which will execute pipeline:
    ```
    make docker-up
    ```
   To stop:
    ```
    make docker-down
    ```
3) For monitoring and run/schedule pipelines using Prefect UI it's necessary to forward port `4200` (I used PyCharm Pro for this) and open url: `http://127.0.0.1:4200/` on local machine.
    ![05_orion_ui.png](/images/05_orion_ui.png)

4) Run python script to create blocks for Prefect:
    ```
    make create-block
    ```
   You can check in UI that blocks for `GCP Credentials` and `GCS Bucket` are created:
    ![05_orion_blocks.png](/images/05_orion_blocks.png)

5) Create a Prefect Flow deployment to:
    - download datasets from web
    - upload them into Goggle Cloud Storage
    - upload spark_job file to Goggle Cloud Storage
    - submit spark job to DataProcCluster. Spark job will do:
      - read csv files
      - modify columns
      - save to parquet
      - save to Big Query with daily **partitioning** by `crime_date` column. This type of partitioning is used to improve performance because I will make aggregation by this field to analyse data. 
    ```
    make ingest-data
    ```
6) Schedule a deployment in prefect to run daily at 02:00 am (if needed):
    ```
    make ingest-data-schedule
    ```
   ![05_deployments.png](/images/05_deployments.png)
   
7) To check Agent's logs (interactively):
    ```
    make docker-agent-logs
    ```

### Step 6. dbt transformation data in BigQuery **(In Remote VM)**
At this moment dbt transformation is working directly from docker container
1) Build dbt for dev:
    ```
    make dbt-dev
    ```
2) Build dbt for production:
    ```
    make dbt-prod
    ```
3) Go to the Looker and create visualization from Big Query table `crime-trends-explorer.prod_crime_reports.fact_crimedata`

### Delete (Optional)
1) Stop docker-compose:
    ```
    make docker-down
    ```
2) Delete infrastructure:
    ```
    terraform -chdir="./terraform" destroy -var="project_id=crime-trends-explorer"
    ```
3) Delete manually temp storage buckets created by the Dataproc cluster.
4) Delete VM instance (if needed).
_[Back to the top](#table-of-contents)_

## Future Improvements

- Create tests for all code and sql
- Move other commands to Make-file to make a reproducibility in less commands
- Implement CI/CD
- Add API for extracting data from web 

_[Back to the top](#table-of-contents)_

## Credits

A special thanks to the instructors for their guidance and support throughout this incredible course. Their expertise and insights have been invaluable in the development of the CrimeTrendsExplorer project. I've learned a lot of useful skills and techniques that have greatly enhanced my knowledge as a data engineer.

- [Alexey Grigorev](https://linkedin.com/in/agrigorev)
- [Ankush Khanna](https://linkedin.com/in/ankushkhanna2)
- [Jeff Hale](https://www.linkedin.com/in/-jeffhale/)
- [Kalise Richmond](https://www.linkedin.com/in/kaliserichmond/)
- [Sejal Vaidya](https://linkedin.com/in/vaidyasejal)
- [Victoria Perez Mola](https://www.linkedin.com/in/victoriaperezmola/)

Thank you for providing such a comprehensive and engaging course experience!


_[Back to the top](#table-of-contents)_