from pyspark.sql import SparkSession
import argparse
import json
import logging
import os
import boto3

log_level = os.environ.get('LOG_LEVEL', logging.INFO)

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level)


def get_lake_prefix(database_name):
    client = boto3.client('glue')
    response = client.get_database(Name=database_name)
    return response['Database']['LocationUri']


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', default='public.customer')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    table_name = args.table_name
    short_table_name = table_name.split('.')[-1]
    f = open('/mnt/var/lib/instance-controller/public/runtime_configs/full_load_configs.json')
    config_dict = json.load(f)
    glue_database = config_dict['DatabaseConfig']['target_db_name']
    lake_location_uri = get_lake_prefix(glue_database)
    table_config = config_dict['TableConfigs'][table_name]
    primary_key = table_config['primary_key']
    precombine_field = table_config['watermark']
    print(config_dict)

    spark = SparkSession\
        .builder\
        .appName("JdbcToHudi")\
        .getOrCreate()

    df = spark.read.format('jdbc') \
        .option("url", "jdbc:postgresql://pg-hammerdb.cob4psnojwdw.us-east-1.rds.amazonaws.com:5432/hammerdb") \
        .option('dbtable', table_name) \
        .option('user', 'postgres') \
        .option('password', 'WQ6psvDWVLA8myZ') \
        .option("driver", "org.postgresql.Driver") \
        .load()

    hudi_options = {
        'hoodie.table.name': short_table_name,
        'hoodie.datasource.write.recordkey.field': primary_key,
        'hoodie.datasource.write.precombine.field': precombine_field,
        'hoodie.datasource.hive_sync.database': 'hammerdb',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.table': short_table_name,
        'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.NonPartitionedExtractor',
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.ComplexKeyGenerator',
        'hoodie.datasource.write.operation': 'bulk_insert',
        'hoodie.bulkinsert.sort.mode': 'NONE'
    }

    df.write \
        .format('org.apache.hudi') \
        .options(**hudi_options) \
        .mode('overwrite') \
        .save(os.path.join(lake_location_uri, short_table_name, ''))


if __name__ == "__main__":
    main()