import argparse
import json
import logging
import os
import boto3
from hudi import get_hudi_options
from pyspark.sql import SparkSession
from util import get_secret

log_level = os.environ.get('LOG_LEVEL', 'INFO')

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


def get_spark_jdbc(secret, table_name):
    username = secret['username']
    password = secret['password']
    engine = secret['engine']
    host = secret['host']
    port = secret['port']
    dbname = secret['dbname']

    if engine.startswith('postgres'):
        driver = 'org.postgresql.Driver'
        engine = 'postgresql'
        logging.info('Engine is postgresql')
    else:
        raise ValueError(f'Engine {engine} not yet supported.')

    spark = SparkSession\
        .builder\
        .appName(f'{dbname}.{table_name}_to_HudiLake')\
        .getOrCreate()

    jdbc_url = f'jdbc:{engine}://{host}:{port}/{dbname}'
    logging.debug(f'JDBC URL: {jdbc_url}')

    # TODO: Support more options such as query, partitoncColumn etc
    spark_jdbc = spark.read.format('jdbc') \
        .option('url', jdbc_url)\
        .option('dbtable', table_name) \
        .option('user', username) \
        .option('password', password) \
        .option('fetchSize', 10000) \
        .option("driver", driver)

    return spark_jdbc


def main():
    args = get_args()
    table_name = args.table_name
    short_table_name = table_name.split('.')[-1]
    f = open('/mnt/var/lib/instance-controller/public/runtime_configs/full_load_configs.json')
    config_dict = json.load(f)
    logging.debug(json.dumps(config_dict, indent=4))

    database_config = config_dict['DatabaseConfig']
    table_config = config_dict['TableConfigs'][table_name]
    secret_id = database_config['secret']
    glue_database = database_config['target_db_name']

    hudi_options = get_hudi_options(short_table_name, glue_database, table_config, 'FULL')
    lake_location_uri = get_lake_prefix(glue_database)
    spark_jdbc = get_spark_jdbc(get_secret(secret_id), table_name)

    df = spark_jdbc.load()

    df.write \
        .format('org.apache.hudi') \
        .options(**hudi_options) \
        .mode('overwrite') \
        .save(os.path.join(lake_location_uri, short_table_name, ''))


if __name__ == "__main__":
    main()
