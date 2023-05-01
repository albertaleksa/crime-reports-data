import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import types
import os

credentials_location = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('crime-reports-data-app') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
# for logging
    # .set("spark.eventLog.enabled", "true")

sc = SparkContext(conf=conf)
# for logging
# sc.setLogLevel("INFO")


hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

# Schema for Austin Crtime data
df_aus_schema = types.StructType([
    types.StructField('Incident Number', types.LongType(), True),
    types.StructField('Highest Offense Description', types.StringType(), True),
    types.StructField('Highest Offense Code', types.IntegerType(), True),
    types.StructField('Family Violence', types.StringType(), True),
    types.StructField('Occurred Date Time', types.StringType(), True),
    types.StructField('Occurred Date', types.StringType(), True),
    types.StructField('Occurred Time', types.StringType(), True),
    types.StructField('Report Date Time', types.StringType(), True),
    types.StructField('Report Date', types.StringType(), True),
    types.StructField('Report Time', types.StringType(), True),
    types.StructField('Location Type', types.StringType(), True),
    types.StructField('Address', types.StringType(), True),
    types.StructField('Zip Code', types.IntegerType(), True),
    types.StructField('Council District', types.IntegerType(), True),
    types.StructField('APD Sector', types.StringType(), True),
    types.StructField('APD District', types.StringType(), True),
    types.StructField('PRA', types.IntegerType(), True),
    types.StructField('Census Tract', types.DoubleType(), True),
    types.StructField('Clearance Status', types.StringType(), True),
    types.StructField('Clearance Date', types.StringType(), True),
    types.StructField('UCR Category', types.StringType(), True),
    types.StructField('Category Description', types.StringType(), True),
    types.StructField('X-coordinate', types.IntegerType(), True),
    types.StructField('Y-coordinate', types.IntegerType(), True),
    types.StructField('Latitude', types.DoubleType(), True),
    types.StructField('Longitude', types.DoubleType(), True),
    types.StructField('Location', types.StringType(), True)
])

# Read AUS data in .csv and save in .parquet format with repartitioning

print(f"processing data for AUSTIN")

input_path = f"gs://crime_trends_explorer_data_lake_crime-trends-explorer/data/aus/aus_2003_2023.csv"
output_path = f"gs://crime_trends_explorer_data_lake_crime-trends-explorer/data/pq/aus/"

# read data using schema
df_aus = spark.read \
    .option("header", "true") \
    .schema(df_aus_schema) \
    .csv(input_path)

df_aus \
    .repartition(24) \
    .write.parquet(output_path, mode='overwrite')
