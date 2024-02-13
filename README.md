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

1. Austin: Austin Police Department's Public Data Portal (https://data.austintexas.gov/). <br>
   Dataset: [Crime Reports](https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu)
2. Los Angeles: Los Angeles Open Data Portal (https://data.lacity.org/).  <br>
   Datasets: [Crime Data from 2010 to 2019](https://data.lacity.org/Public-Safety/Crime-Data-from-2010-to-2019/63jg-8b9z), [Crime Data from 2020 to Present](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8)
3. San Diego: San Diego Data Portal (https://data.sandiego.gov/). <br>
   Dataset: [Police Calls for Service](https://data.sandiego.gov/datasets/police-calls-for-service/)

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

1. **Data Ingestion**: In this stage, raw crime data from various cities is collected from different web sources in the form of *CSV* files. The data is then stored in *Google Cloud Storage*, along with the *Python file* that contains the *Apache Spark job*. <br><br>
 For each dataset, a *Prefect Flow* (`"Ingest Flow"`) is utilized. This flow consists of two tasks:
   * Downloading the dataset *from the web into local storage*
   * Uploading the *local file to Google Cloud Storage* (GCS).
   <br><br>
   <details>
     <summary>Ingest Flow</summary>
   
    ```python
    @flow(name="Ingest Flow")
    def web_to_gcs(url: str, csv_name: str) -> None:
        """Download data in csv and upload to GCS"""
        downloaded_file = download_file(url, csv_name)
        upload_to_gcs(downloaded_file)
   ```
   </details>

   <details>
     <summary>Web -> Local storage</summary>
   
    ```python
    @task(log_prints=True, retries=3, retry_delay_seconds=60)
    def download_file(url: str, csv_name: str) -> Path:
        """Download data from web into local storage"""
        city = csv_name.split("_")[0]
        path = Path(f"data/{city}/{csv_name}")
        print(f"Downloading file {csv_name} for {city}")
    
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            downloaded_size = 0
            size = 0
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        downloaded_size_mb = downloaded_size / (1024 * 1024)
    
                        if int(downloaded_size_mb) % 5 == 0 and size != int(downloaded_size_mb):
                            print(f"\rDownloaded size: {int(downloaded_size_mb)} MB", end="")
                            size = int(downloaded_size_mb)
            print(f"File {csv_name} downloaded successfully. Full size is {downloaded_size_mb:.2f} MB")
        else:
            print("Error downloading the file.")
        return path
   ```
   </details>

   <details>
     <summary>Local file -> GCS</summary>
   
    ```python
    @task(log_prints=True)
    def upload_to_gcs(path: Path) -> None:
        """Upload local file to GCS"""
        bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
        gcs_block = GcsBucket.load(bucket_block_name)
        path_1 = path.parts[0]
        path_rest = "/".join(path.parts[1:])
    
        # Check if the file exists
        if os.path.exists(path):
            # If the file exists, upload it to GCS
            gcs_block.upload_from_path(from_path=f"{path}", to_path=f"{path_1}/raw/{path_rest}", timeout=300)
            os.remove(path)
        else:
            print(f"The file '{path}' does not exist.")
    
        return
   ```
   </details>
   
   <br>
    
   Another *Prefect Flow* (`"Submit Spark Job"`) that is utilized is the Flow for submitting a Spark job to the Dataproc Cluster. This Flow consists of two tasks: 
   * Uploading the Python file containing the *Spark job* to Google Cloud Storage (GCS)
   * *Submitting the Spark* job to the DataProc Cluster.    
   <br>
   <details>
     <summary>Spark job file -> GCS</summary>
   
    ```python
    @task(log_prints=True)
    def upload_job_to_gcs() -> Path:
        """Upload python-file with Spark job to gcs"""
        bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
        spark_job_file = os.getenv("SPARK_JOB_FILE")
        spark_job_file_path = f'flows/{os.getenv("SPARK_JOB_FILE")}'
        gcs_block = GcsBucket.load(bucket_block_name)
        path = Path(f"code/{spark_job_file}")
    
        # Check if the file exists
        if os.path.exists(spark_job_file_path):
            # If the file exists, upload it to GCS
            gcs_block.upload_from_path(from_path=spark_job_file_path, to_path=path, timeout=300)
        else:
            print(f"The file '{spark_job_file_path}' does not exist.")
    
        return path
   ```
   </details>

   <details>
     <summary>Submit Spark job</summary>
   
    ```python
    @task(log_prints=True)
    def submit_dataproc_job(spark_job_file: Path, temp_gcs_bucket: str,
                            input_path_aus: str, output_path_aus: str, output_bq_aus: str,
                            input_path_la: str, output_path_la: str, output_bq_la: str,
                            input_path_sd: str, output_path_sd: str, output_bq_sd: str):
        """Submit Spark job to DataProc Cluster"""
        project_id = os.getenv("PROJECT_ID")
        region = os.getenv("REGION")
        cluster_name = os.getenv("DATAPROC_CLUSTER_NAME")
        bucket_name = os.getenv("DATA_LAKE_BUCKET_NAME")
    
        # Use Prefect GcpCredentials Block which stores credentials
        credentials_block_name = os.getenv("CREDS_BLOCK_NAME")
        gcp_credentials_block = GcpCredentials.load(credentials_block_name)
        credentials = gcp_credentials_block.get_credentials_from_service_account()
    
        # Set up DataProc client and cluster information
        dataproc_client = dataproc.JobControllerClient(
            credentials=credentials,
            client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
        )
    
        # Define the PySpark job
        job_details = {
            "reference": {"job_id": str(uuid.uuid4())},
            "placement": {"cluster_name": cluster_name},
            "pyspark_job": {
                "main_python_file_uri": f"gs://{bucket_name}/{spark_job_file}",
                # "args": [input_file, output_file],
                "args": [
                    "--temp_gcs_bucket", temp_gcs_bucket,
                    "--input_path_aus", input_path_aus,
                    "--output_path_aus", output_path_aus,
                    "--output_bq_aus", output_bq_aus,
                    "--input_path_la", input_path_la,
                    "--output_path_la", output_path_la,
                    "--output_bq_la", output_bq_la,
                    "--input_path_sd", input_path_sd,
                    "--output_path_sd", output_path_sd,
                    "--output_bq_sd", output_bq_sd
                ],
                "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
                "python_file_uris": [],
                "file_uris": [],
                "archive_uris": [],
            },
        }
    
        print(f"job_details = {job_details}")
    
        # Submit the job
        operation = dataproc_client.submit_job_as_operation(
            request={
                "project_id": project_id,
                "region": region,
                "job": job_details
            }
        )
        response = operation.result()
        print(f"response = {response}")
        print(f"response.reference.job_id = {response.reference.job_id}")
    
        # Return the job ID
        return response.reference.job_id
   ```
   </details>
   <br>

2. **Data Transformation**: The raw data is processed using *Apache Spark*, running on a *DataProc Cluster*. The Spark job performs tasks such as data cleaning, transformation, enrichment, and partitioning. The following steps outline the process for each city's data:

   * **Read CSV Dataset:** The Spark job reads the *CSV* dataset from *Google Cloud Storage (GCS)* using a specific schema.
      <details>
        <summary>Read csv data using schema</summary>
   
       ```python
        def read_csv(spark: SparkSession, schema: types.StructType, input_path: str) -> DataFrame:
        """Read csv data using schema"""
        print(f"Read csv data {input_path}")
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "false") \
            .schema(schema) \
            .csv(input_path)
        return df
       ```
      </details>

      <details>
        <summary>Austin Dataset Description</summary>
    
      | Column Name                    | Description                                                  | Type         |
      |--------------------------------|--------------------------------------------------------------|--------------|
      | Incident Number                | Incident report number                                       | Number       |
      | Highest Offense Description    | Description                                                  | Plain Text   |
      | Highest Offense Code           | Code                                                         | Number       |
      | Family Violence                | Incident involves family violence? Y = yes, N = no           | Plain Text   |
      | Occurred Date Time             | Date and time (combined) incident occurred                   | Date & Time  |
      | Occurred Date                  | Date the incident occurred                                   | Date & Time  |
      | Occurred Time                  | Time the incident occurred                                   | Number       |
      | Report Date Time               | Date and time (combined) incident was reported               | Date & Time  |
      | Report Date                    | Date the incident was reported                               | Date & Time  |
      | Report Time                    | Time the incident was reported                               | Number       |
      | Location Type                  | General description of the premise where the incident occurred| Plain Text   |
      | Address                        | Incident location                                            | Plain Text   |
      | Zip Code                       | Zip code where incident occurred                             | Number       |
      | Council District               | Austin city council district where incident occurred          | Number       |
      | APD Sector                     | Austin Police Department sector where incident occurred       | Plain Text   |
      | APD District                   | Austin Police Department district where incident occurred     | Number       |
      | PRA                            | Police Reporting Area where incident occurred                 | Number       |
      | Census Tract                   | Census tract where incident occurred                         | Number       |
      | Clearance Status               | How the incident was cleared. C, N, O                        | Plain Text   |
      | Clearance Date                 | Date the incident was cleared                                | Date & Time  |
      | UCR Category                   | UCR category of the highest offense                           | Plain Text   |
      | Category Description           | UCR category description of the highest offense               | Plain Text   |
      | X-coordinate                   | X-coordinate of the incident location                        | Number       |
      | Y-coordinate                   | Y-coordinate of the incident location                        | Number       |
      | Latitude                       | Latitude of the incident location                            | Number       |
      | Longitude                      | Longitude of the incident location                           | Number       |
      | Location                       | Location as a (latitude, longitude) pair                     | Location     |
    
      </details>    
   
      <details>
        <summary>Schema for Austin Crime data</summary>

       ```python
       df_aus_schema = types.StructType([
            types.StructField('Incident_Number', types.LongType(), True),
            types.StructField('Highest_Offense_Description', types.StringType(), True),
            types.StructField('Highest_Offense_Code', types.IntegerType(), True),
            types.StructField('Family_Violence', types.StringType(), True),
            types.StructField('Occurred_Date_Time', types.StringType(), True),
            types.StructField('Occurred_Date', types.StringType(), True),
            types.StructField('Occurred_Time', types.StringType(), True),
            types.StructField('Report_Date_Time', types.StringType(), True),
            types.StructField('Report_Date', types.StringType(), True),
            types.StructField('Report_Time', types.StringType(), True),
            types.StructField('Location_Type', types.StringType(), True),
            types.StructField('Address', types.StringType(), True),
            types.StructField('Zip_Code', types.IntegerType(), True),
            types.StructField('Council_District', types.IntegerType(), True),
            types.StructField('APD_Sector', types.StringType(), True),
            types.StructField('APD_District', types.StringType(), True),
            types.StructField('PRA', types.IntegerType(), True),
            types.StructField('Census_Tract', types.DoubleType(), True),
            types.StructField('Clearance_Status', types.StringType(), True),
            types.StructField('Clearance_Date', types.StringType(), True),
            types.StructField('UCR_Category', types.StringType(), True),
            types.StructField('Category_Description', types.StringType(), True),
            types.StructField('X-coordinate', types.IntegerType(), True),
            types.StructField('Y-coordinate', types.IntegerType(), True),
            types.StructField('Latitude', types.DoubleType(), True),
            types.StructField('Longitude', types.DoubleType(), True),
            types.StructField('Location', types.StringType(), True)
       ])
       ```
      </details>
      <details>
        <summary>Los Angeles Dataset Description</summary>
        
        | Column Name | Description | Type |
        | ----------- | ----------- | ---- |
        | DR_NO | Division of Records Number: Official file number made up of a 2 digit year, area ID, and 5 digits | Plain Text |
        | Date Rptd | MM/DD/YYYY | Date & Time |
        | DATE OCC | MM/DD/YYYY | Date & Time |
        | TIME OCC | In 24 hour military time. | Plain Text |
        | AREA | The LAPD has 21 Community Police Stations referred to as Geographic Areas within the department. These Geographic Areas are sequentially numbered from 1-21. | Plain Text |
        | AREA NAME | The 21 Geographic Areas or Patrol Divisions are also given a name designation that references a landmark or the surrounding community that it is responsible for. For example 77th Street Division is located at the intersection of South Broadway and 77th Street, serving neighborhoods in South Los Angeles. | Plain Text |
        | Rpt Dist No | A four-digit code that represents a sub-area within a Geographic Area. All crime records reference the "RD" that it occurred in for statistical comparisons. Find LAPD Reporting Districts on the LA City GeoHub athttp://geohub.lacity.org/datasets/c4f83909b81d4786aa8ba8a74a4b4db1_4 | Plain Text |
        | Part 1-2 |  | Number |
        | Crm Cd | Indicates the crime committed. (Same as Crime Code 1) | Plain Text |
        | Crm Cd Desc | Defines the Crime Code provided. | Plain Text |
        | Mocodes | Modus Operandi: Activities associated with the suspect in commission of the crime.See attached PDF for list of MO Codes in numerical order.https://data.lacity.org/api/views/y8tr-7khq/files/3e0aca2a-ef30-4f3e-8f57-d84a916a3a1b | Plain Text |
        | Vict Age | The victim's age at the time the incident occurred. | Number |
        | Vict Sex | Gender of Victim | Plain Text |
        | Vict Descent | Descent of Victim | Plain Text |
        | Premis Cd | The type of structure, vehicle, or location where the crime took place. | Plain Text |
        | Premis Desc | Defines the Premise Code provided. | Plain Text |
        | Weapon Used Cd | The type of weapon used in the crime. | Plain Text |
        | Weapon Desc | Defines the Weapon Used Code provided. | Plain Text |
        | Status | Status of the case. (IC is the default) | Plain Text |
        | Status Desc | Defines the Status Code provided. | Plain Text |
        | Crm Cd 1 | Indicates the crime committed. Crime Code 1 is the primary and most serious one. Crime Code 2, 3, and 4 are respectively less serious offenses. Lower crime class numbers are more serious. | Plain Text |
        | Crm Cd 2 | May contain a code for an additional crime, less serious than Crime Code 1. | Plain Text |
        | Crm Cd 3 | May contain a code for an additional crime, less serious than Crime Code 1. | Plain Text |
        | Crm Cd 4 | May contain a code for an additional crime, less serious than Crime Code 1. | Plain Text |
        | LOCATION | Street address of crime incident rounded to the nearest hundred block to maintain anonymity. | Plain Text |
        | Cross Street | Cross Street of rounded Address | Plain Text |
        | LAT | Latitude | Number |
        | LON | Longtitude | Number |
      </details>
      <details>
        <summary>Schema for Los Angeles Crime data</summary>
   
       ```python
       df_la_schema = types.StructType([
            types.StructField('DR_NO', types.IntegerType(), True),
            types.StructField('Date_Rptd', types.StringType(), True),
            types.StructField('DATE_OCC', types.StringType(), True),
            types.StructField('TIME_OCC', types.StringType(), True),
            types.StructField('AREA', types.IntegerType(), True),
            types.StructField('AREA_NAME', types.StringType(), True),
            types.StructField('Rpt_Dist_No', types.IntegerType(), True),
            types.StructField('Part_1-2', types.IntegerType(), True),
            types.StructField('Crm_Cd', types.IntegerType(), True),
            types.StructField('Crm_Cd_Desc', types.StringType(), True),
            types.StructField('Mocodes', types.StringType(), True),
            types.StructField('Vict_Age', types.IntegerType(), True),
            types.StructField('Vict_Sex', types.StringType(), True),
            types.StructField('Vict_Descent', types.StringType(), True),
            types.StructField('Premis_Cd', types.IntegerType(), True),
            types.StructField('Premis_Desc', types.StringType(), True),
            types.StructField('Weapon_Used_Cd', types.IntegerType(), True),
            types.StructField('Weapon_Desc', types.StringType(), True),
            types.StructField('Status', types.StringType(), True),
            types.StructField('Status_Desc', types.StringType(), True),
            types.StructField('Crm_Cd_1', types.IntegerType(), True),
            types.StructField('Crm_Cd_2', types.IntegerType(), True),
            types.StructField('Crm_Cd_3', types.IntegerType(), True),
            types.StructField('Crm_Cd_4', types.IntegerType(), True),
            types.StructField('LOCATION', types.StringType(), True),
            types.StructField('Cross_Street', types.StringType(), True),
            types.StructField('LAT', types.DoubleType(), True),
            types.StructField('LON', types.DoubleType(), True)
       ])
       ```
      </details>
      <details>
        <summary>San Diego Dataset Description</summary>

        | Field                    | Description                             | Possible_values                                          |
        |--------------------------|-----------------------------------------|----------------------------------------------------------|
        | incident_num             | Unique Incident Identifier              |                                                           |
        | date_time                | Date / Time in 24 Hour Format           |                                                           |
        | day                      | Day of the week                         | (1 = Sunday, 2 = Monday ...)                              |
        | address_number_primary   | Street Number of Incident, Abstracted to block level|                                         |
        | address_dir_primary      | Direction of street in address          | ex: 123 W El Cajon Bl                                    |
        | address_road_primary     | Name of Street                          |                                                           |
        | address_sfx_primary      | Street Type                             | ST, Av, etc                                              |
        | address_pd_intersecting  | If intersecting street available, direction of that street|                                 |
        | address_road_intersecting| If intersecting street available, street name|                                               |
        | address_sfx_intersecting | If intersecting street available, street type|                                               |
        | call_type                | Type of call                            | [Call Types](http://seshat.datasd.org/pd/pd_cfs_calltypes_datasd.csv)|
        | disposition              | Classification                          | [Disposition Codes](http://seshat.datasd.org/pd/pd_dispo_codes_datasd.csv)|
        | beat                     | San Diego PD Beat                       | [Beat Neighborhoods](http://seshat.datasd.org/pd/pd_beat_neighborhoods_datasd.csv)|
        | priority                 | Priority assigned by dispatcher         | [Priority Definitions](http://seshat.datasd.org/pd/pd_cfs_priority_defs_datasd.pdf)|
      </details>
      <details>
        <summary>Schema for San Diego Crime data</summary>
   
       ```python
       df_sd_schema = types.StructType([
            types.StructField('incident_num', types.StringType(), True),
            types.StructField('date_time', types.TimestampType(), True),
            types.StructField('day_of_week', types.IntegerType(), True),
            types.StructField('address_number_primary', types.IntegerType(), True),
            types.StructField('address_dir_primary', types.StringType(), True),
            types.StructField('address_road_primary', types.StringType(), True),
            types.StructField('address_sfx_primary', types.StringType(), True),
            types.StructField('address_dir_intersecting', types.StringType(), True),
            types.StructField('address_road_intersecting', types.StringType(), True),
            types.StructField('address_sfx_intersecting', types.StringType(), True),
            types.StructField('call_type', types.StringType(), True),
            types.StructField('disposition', types.StringType(), True),
            types.StructField('beat', types.DoubleType(), True),
            types.StructField('priority', types.DoubleType(), True)
       ])
       ```
      </details>
        <br>
   * **Write to Parquet Format:** The data is written to *Parquet* format, and repartitioning is performed to optimize storage and access.
      <details>
        <summary>Write data to parquet with repartitioning</summary>
   
       ```python
       def write_parquet(df: DataFrame, output_path: str, partitions_num: int) -> None:
        """Write data to parquet with repartitioning"""
        print(f"Write parquet data {output_path}")
        df \
            .repartition(partitions_num) \
            .write.parquet(output_path, mode='overwrite')
       ```
      </details>
        <br>
   * **Modify Columns:** The columns are modified for consistency by renaming, changing types, converting formats, and filtering as needed.
      <details>
        <summary>Example of columns modification for Austin dataset</summary>
   
       ```python
       def modify_aus(df: DataFrame) -> DataFrame:
           """Modify columns for AUSTIN"""
           print(f"Modify columns for AUSTIN")
           # To convert fields like 'Occurred_Date_Time' to Timestamp format
           timestamp_format = "MM/dd/yyyy hh:mm:ss a"
           # To convert fields like 'Occurred_Date' to Date format
           date_format = "MM/dd/yyyy"
    
           # for filling field 'clearance_status'
           new_clearance_status = (F.when(F.col("clearance_status") == "C", "Arrested") \
                                   .when(F.col("clearance_status") == "O", "Exception") \
                                   .when(F.col("clearance_status") == "N", "Not cleared") \
                                   .otherwise(None))
    
           df_dt = df \
               .withColumnRenamed("Incident_Number", "incident_num") \
               .withColumnRenamed("Highest_Offense_Description", "crime_description") \
               .withColumnRenamed("Highest_Offense_Code", "crime_code") \
               .withColumnRenamed("Family_Violence", "family_violence") \
               .withColumnRenamed("Location_Type", "location_type") \
               .withColumnRenamed("Address", "address") \
               .withColumnRenamed("Zip_Code", "zip_code") \
               .withColumnRenamed("Council_District", "council_district") \
               .withColumnRenamed("APD_Sector", "apd_sector") \
               .withColumnRenamed("APD_District", "apd_district") \
               .withColumnRenamed("PRA", "pra") \
               .withColumnRenamed("Census_Tract", "census_tract") \
               .withColumnRenamed("Clearance_Status", "clearance_status") \
               .withColumnRenamed("UCR_Category", "ucr_category") \
               .withColumnRenamed("Category_Description", "category_description") \
               .withColumn("crime_datetime", F.to_timestamp("Occurred_Date_Time", timestamp_format)) \
               .withColumn("crime_date", F.to_date("Occurred_Date", date_format)) \
               .withColumn("report_datetime", F.to_timestamp("Report_Date_Time", timestamp_format)) \
               .withColumn("report_date", F.to_date("Report_Date", date_format)) \
               .withColumn("clearance_date", F.to_date("Clearance_Date", date_format)) \
               .withColumn("clearance_status", new_clearance_status) \
               .select("incident_num", "crime_datetime", "crime_date", \
                       "report_datetime", "report_date", "crime_code", \
                       "crime_description", "family_violence", "location_type", \
                       "address", "zip_code", "council_district", \
                       "apd_sector", "apd_district", "pra", \
                       "census_tract", "clearance_status", "clearance_date", \
                       "ucr_category", "category_description")
           return df_dt
       ```
      </details>
        <br>
   * **Save to BigQuery:** The transformed data is saved to Google *BigQuery*, a fully-managed data warehouse solution, using daily partitioning based on the `crime_date` column.
       <details>
        <summary>Saving the data to BigQuery</summary>
    
       ```python
       def write_to_bigquery(df: DataFrame, output: str, partition_column: str) -> None:
           """Saving the data to BigQuery"""
           print(f"Write to BigQuery {output}")
           df.write.format('bigquery') \
               .option('table', output) \
               .option('partitionType', 'MONTH') \
               .option('partitionField', partition_column) \
               .option('clustering', partition_column) \
               .mode("overwrite") \
               .save()
       ```
       </details>
        <br>
      These steps ensure that the raw data is transformed into a structured and consistent format, suitable for further analysis.<br><br>
3. **Data Modeling**: The transformed data is further processed using dbt (Data Build Tool) to create meaningful and structured data models in Google BigQuery.
       <details>
        <summary>Entity Relationship Diagrams of raw data</summary>
        ![raw_erd.png](/images/raw_erd.png)
       </details>
<br>

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
7. **(In Remote VM)** Configure gcloud with your service account .json file:
   - If needed change **KEY_FILE** and **KEY_FILE_PATH** in file `.env` to your values
   - Run command:
     ```
     make activate-sa
     ```
   - Log out and log back

### Step 3. Run Terraform to deploy your infrastructure to your Google Cloud Project **(In Remote VM)**

0) If needed you can change variables in `.env` (change REGION, ZONE, PROJECT_ID..) and `terraform.tfvars` files

1) Initialize terraform:
    ```
    make terraform-init
    ```
2) Build a deployment plan (change `crime-trends-explorer` to your `project_id` in `.env` file if needed):
    ```
    make terraform-plan
    ```
3) Apply the deployment plan and deploy the infrastructure:
    ```
    make terraform-apply
    ```
4) Go to Google Cloud Console to make sure that infrastructure is created:
    - Google Cloud Storage:
   ![03_bucket.png](/images/03_bucket.png)
    - BigQuery:
   ![03_bigquery.png](/images/03_bigquery.png)
    - DataProc:
   ![03_dataproc.png](/images/03_dataproc.png)
5) A Dataproc temp bucket name (from gcs buckets) was copied automatically to file `.env` in field `DATAPROC_TEMP_BUCKET`.


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
    make terraform-destroy
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