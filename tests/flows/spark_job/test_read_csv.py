from pyspark.sql import SparkSession
from pyspark.sql import types
import pytest
import tempfile
import os
from flows.spark_job import read_csv


@pytest.fixture(scope="session")
def spark():
    """
    master = local[1] – specifies that spark is running on a local machine with one thread
    spark.executor.cores = 1 – set number of cores to one
    spark.executor.instances = 1 - set executors to one
    spark.sql.shuffle.partitions = 1 - set the maximum number of partitions to 1
    spark.driver.bindAddress = 127.0.0.1 – (optional) Explicitly specify the driver bind address.
    Useful if your machine also has a live connection to a remote cluster
    :return:
    """
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("local-tests") \
        .config("spark.executor.cores", "1") \
        .config("spark.executor.instances", "1") \
        .config("spark.sql.shuffle.partitions", "1") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .getOrCreate()

    yield spark
    spark.stop()


def test_read_csv_successful(spark):
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write("Name,Age\nAlice,29\nBob,43")
        temp_file_path = f.name

    # Define a sample schema and input data
    schema = types.StructType([
        types.StructField("Name", types.StringType(), True),
        types.StructField("Age", types.IntegerType(), True)
    ])

    # Call the function
    df = read_csv(spark, schema, temp_file_path)

    # Perform some DataFrame assertions
    assert df.count() == 2  # Replace 'expected_count' with the actual expected count of rows
    assert len(df.columns) == 2

    # Clean up the temporary file
    os.remove(temp_file_path)

