import logging
from util import get_secret
from pyspark.sql import SparkSession


def get_parquet_df(table_name, file_list):
    spark = SparkSession \
        .builder \
        .appName(f'{table_name}_HudiLake_upsert') \
        .getOrCreate()

    sc = spark.sparkContext()

    df = sc.read.format('parquet')

    for file in file_list:
        df.load(file)

    return df
