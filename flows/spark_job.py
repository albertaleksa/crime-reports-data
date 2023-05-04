import argparse

import pyspark
from pyspark.sql import SparkSession, DataFrame, types
from pyspark.sql import functions as F
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
import os


def read_csv(spark: SparkSession, schema: types.StructType, input_path: str) -> DataFrame:
    """Read csv data using schema"""
    print(f"Read csv data {input_path}")
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "false") \
        .schema(schema) \
        .csv(input_path)
    return df


def read_parquet(spark: SparkSession, input_path: str) -> DataFrame:
    """Read parquet file"""
    print(f"Read parquet data {input_path}")
    df = spark.read \
        .parquet(input_path)
    return df


def write_parquet(df: DataFrame, output_path: str, partitions_num: int) -> None:
    """Write data to parquet with repartitioning"""
    print(f"Write parquet data {output_path}")
    df \
        .repartition(partitions_num) \
        .write.parquet(output_path, mode='overwrite')


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


def csv_to_parquet_aus(spark: SparkSession, input_path: str, output_path: str) -> None:
    """Read data from csv and save to parquet for Austin"""
    print(f"Processing data for AUSTIN")
    # Schema for Austin Crtime data
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

    df_aus = read_csv(spark, df_aus_schema, input_path)
    write_parquet(df_aus, output_path, 24)


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


def csv_to_parquet_la(spark: SparkSession, input_path: str, output_path: str) -> None:
    """Read data from csv and save to parquet for Los Angeles"""
    print(f"Processing data for LOS ANGELES")
    # Schema for Los Angeles Crtime data
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

    df_la = read_csv(spark, df_la_schema, input_path)
    write_parquet(df_la, output_path, 24)


def modify_la(df: DataFrame) -> DataFrame:
    """Modify columns for LOS ANGELES"""
    print(f"Modify columns for LOS ANGELES")
    # To convert fields like 'Occurred_Date_Time' to Timestamp format
    timestamp_format = "MM/dd/yyyy hh:mm:ss a"
    # To convert fields like 'crime_datetime' to Timestamp format
    date_time_format = "yyyy-MM-dd HH:mm:ss"

    # for filling field 'vict_sex'
    new_vict_sex = (F.when(F.col("vict_sex") == "F", "Female") \
                    .when(F.col("vict_sex") == "M", "Male") \
                    .when(F.col("vict_sex") == "X", "Unknown") \
                    .otherwise("Unknown"))

    # for filling field 'vict_descent'
    new_vict_descent = (F.when(F.col("vict_descent") == "A", "Other Asian") \
                        .when(F.col("vict_descent") == "B", "Black") \
                        .when(F.col("vict_descent") == "C", "Chinese") \
                        .when(F.col("vict_descent") == "D", "Cambodian") \
                        .when(F.col("vict_descent") == "F", "Filipino") \
                        .when(F.col("vict_descent") == "G", "Guamanian") \
                        .when(F.col("vict_descent") == "H", "Hispanic/Latin/Mexican") \
                        .when(F.col("vict_descent") == "I", "American Indian/Alaskan Native") \
                        .when(F.col("vict_descent") == "J", "Japanese") \
                        .when(F.col("vict_descent") == "K", "Korean") \
                        .when(F.col("vict_descent") == "L", "Laotian") \
                        .when(F.col("vict_descent") == "O", "Other") \
                        .when(F.col("vict_descent") == "P", "Pacific Islander") \
                        .when(F.col("vict_descent") == "S", "Samoan") \
                        .when(F.col("vict_descent") == "U", "Hawaiian") \
                        .when(F.col("vict_descent") == "V", "Vietnamese") \
                        .when(F.col("vict_descent") == "W", "White") \
                        .when(F.col("vict_descent") == "X", "Unknown") \
                        .when(F.col("vict_descent") == "Z", "Asian Indian") \
                        .otherwise("Unknown"))

    df_dt = df \
        .withColumnRenamed("DR_NO", "incident_num") \
        .withColumnRenamed("Crm_Cd_Desc", "crime_description") \
        .withColumnRenamed("Crm_Cd", "crime_code") \
        .withColumnRenamed("AREA", "area_code") \
        .withColumnRenamed("AREA_NAME", "area_name") \
        .withColumnRenamed("Rpt_Dist_No", "rpt_dist_num") \
        .withColumnRenamed("Part_1-2", "part_1_2") \
        .withColumnRenamed("Mocodes", "mocodes") \
        .withColumnRenamed("Vict_Age", "vict_age") \
        .withColumnRenamed("Vict_Sex", "vict_sex") \
        .withColumnRenamed("Vict_Descent", "vict_descent") \
        .withColumnRenamed("Premis_Cd", "premis_code") \
        .withColumnRenamed("Premis_Desc", "premis_description") \
        .withColumnRenamed("Weapon_Used_Cd", "weapon_used_code") \
        .withColumnRenamed("Weapon_Desc", "weapon_description") \
        .withColumnRenamed("Status", "status") \
        .withColumnRenamed("Status_Desc", "status_description") \
        .withColumnRenamed("Crm_Cd_1", "crime_code_1") \
        .withColumnRenamed("Crm_Cd_2", "crime_code_2") \
        .withColumnRenamed("Crm_Cd_3", "crime_code_3") \
        .withColumnRenamed("Crm_Cd_4", "crime_code_4") \
        .withColumnRenamed("LOCATION", "location") \
        .withColumnRenamed("Cross_Street", "cross_street") \
        .withColumnRenamed("LAT", "latitude") \
        .withColumnRenamed("LON", "longtitude") \
        .withColumn("report_date", F.to_date("Date_Rptd", timestamp_format)) \
        .withColumn("crime_date", F.to_date("DATE_OCC", timestamp_format)) \
        .withColumn("crime_datetime", F.concat(F.col("crime_date"), \
                                               F.lit(" "), \
                                               F.col("TIME_OCC").substr(1, 2), \
                                               F.lit(":"), \
                                               F.col("TIME_OCC").substr(3, 2), \
                                               F.lit(":00"))) \
        .withColumn("crime_datetime", F.to_timestamp(F.col("crime_datetime"), date_time_format)) \
        .withColumn("vict_sex", new_vict_sex) \
        .withColumn("vict_descent", new_vict_descent) \
        .select("incident_num", "crime_datetime", "crime_date", \
                "report_date", "crime_code", "crime_description", \
                "area_code", "area_name", "rpt_dist_num", \
                "part_1_2", "mocodes", "vict_age", \
                "vict_sex", "vict_descent", "premis_code", \
                "premis_description", "weapon_used_code", "weapon_description", \
                "status", "status_description", "crime_code_1", \
                "crime_code_2", "crime_code_3", "crime_code_4", \
                "location", "cross_street", "latitude", \
                "longtitude")
    return df_dt


def csv_to_parquet_sd(spark: SparkSession, input_path: str, output_path: str) -> None:
    """Read data from csv and save to parquet for San Diego"""
    print(f"Processing data for SAN DIEGO")
    # Schema for San Diego Crtime data
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

    df_sd = read_csv(spark, df_sd_schema, input_path)
    # Some values have Double type, need to convert
    df_sd = df_sd \
        .withColumn("beat", F.col("beat").cast(types.IntegerType())) \
        .withColumn("priority", F.col("priority").cast(types.IntegerType()))

    write_parquet(df_sd, output_path, 4)


def modify_sd(df: DataFrame) -> DataFrame:
    """Modify columns for SAN DIEGO"""
    print(f"Modify columns for SAN DIEGO")
    # To convert fields like 'crime_date_time' to Date format
    date_time_format = "yyyy-MM-dd HH:mm:ss"

    df_dt = df \
        .withColumnRenamed("date_time", "crime_datetime") \
        .withColumn("incident_num", F.expr("substring(incident_num, 2, length(incident_num) - 1)")) \
        .withColumn("crime_date", F.to_date("crime_datetime", date_time_format)) \
        .select("incident_num", "crime_datetime", "crime_date", \
                "day_of_week", "address_number_primary", "address_dir_primary", \
                "address_road_primary", "address_sfx_primary", "address_dir_intersecting", \
                "address_road_intersecting", "address_sfx_intersecting", "call_type", \
                "disposition", "beat", "priority")
    return df_dt


def parquet_to_bq_aus(spark: SparkSession, input_path: str, output_bq: str):
    """Read data from parquet, modify columns and
        save to BigQuery for Austin using daily partitioning by crime_date column"""
    df_aus = read_parquet(spark, input_path)
    df_modify_aus = modify_aus(df_aus)
    write_to_bigquery(df_modify_aus, output_bq, "crime_date")


def parquet_to_bq_la(spark: SparkSession, input_path: str, output_bq: str):
    """Read data from parquet, modify columns and
        save to BigQuery for Los Angeles using daily partitioning by crime_date column"""
    df_la = read_parquet(spark, input_path)
    df_modify_la = modify_la(df_la)
    write_to_bigquery(df_modify_la, output_bq, "crime_date")


def parquet_to_bq_sd(spark: SparkSession, input_path: str, output_bq: str):
    """Read data from parquet, modify columns and
        save to BigQuery for San Diego using daily partitioning by crime_date column"""
    df_sd = read_parquet(spark, input_path)
    df_modify_sd = modify_sd(df_sd)
    write_to_bigquery(df_modify_sd, output_bq, "crime_date")


def main(params):
    # Create a Spark session
    spark = SparkSession.builder \
        .appName('crime-reports-data-app') \
        .getOrCreate()

    # temp bucket for saving to BigQuery
    spark.conf.set('temporaryGcsBucket', params.temp_gcs_bucket)

    # Austin
    input_path_aus = params.input_path_aus
    output_path_aus = params.output_path_aus
    output_bq_aus = params.output_bq_aus
    csv_to_parquet_aus(spark, input_path_aus, output_path_aus)

    # Los Angeles
    input_path_la = params.input_path_la
    output_path_la = params.output_path_la
    output_bq_la = params.output_bq_la
    csv_to_parquet_la(spark, input_path_la, output_path_la)

    # San Diego
    input_path_sd = params.input_path_sd
    output_path_sd = params.output_path_sd
    output_bq_sd = params.output_bq_sd
    for year in range(2015, 2024):
        print(f"processing data for SAN DIEGO for {year}")

        input_path = f"{input_path_sd}sd_{year}.csv"
        output_path = f"{output_path_sd}{year}/"

        csv_to_parquet_sd(spark, input_path, output_path)

    # modify aus and save to BQ
    parquet_to_bq_aus(spark, f"{output_path_aus}*", output_bq_aus)

    # modify la and save to BQ
    parquet_to_bq_la(spark, f"{output_path_la}*", output_bq_la)

    # modify sd and save to BQ
    parquet_to_bq_sd(spark, f"{output_path_sd}*", output_bq_sd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to BigQuery")

    parser.add_argument("--temp_gcs_bucket", type=str, required=True, help="Temp bucket for saving to BigQuery")

    parser.add_argument("--input_path_aus", type=str, required=True, help="Path to raw CSV data for Austin Crime Records")
    parser.add_argument("--output_path_aus", type=str, required=True, help="Output path to parquet data for Austin Crime Records")
    parser.add_argument("--output_bq_aus", type=str, required=True, help="Table name in BigQuery for Austin Crime Records")

    parser.add_argument("--input_path_la", type=str, required=True, help="Path to raw CSV data for Los Angeles Crime Records")
    parser.add_argument("--output_path_la", type=str, required=True, help="Output path to parquet data for Los Angeles Crime Records")
    parser.add_argument("--output_bq_la", type=str, required=True, help="Table name in BigQuery for Los Angeles Crime Records")

    parser.add_argument("--input_path_sd", type=str, required=True, help="Path to raw CSV data for San Diego Crime Records")
    parser.add_argument("--output_path_sd", type=str, required=True, help="Output path to parquet data for San Diego Crime Records")
    parser.add_argument("--output_bq_sd", type=str, required=True, help="Table name in BigQuery for San Diego Crime Records")

    args = parser.parse_args()

    main(args)
