import argparse
import json
import logging
import os
from hudi import get_hudi_options
from pyspark.sql.functions import lit
from pyspark.sql import SparkSession

lake_location_uri = os.path.join(os.environ['LAKE_S3URI'], '')
log_level = os.environ.get('LOG_LEVEL', 'INFO')

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', default='public.customer')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    table_name = args.table_name
    f = open('/mnt/var/lib/instance-controller/public/runtime_configs/incremental_configs.json')
    config_dict = json.load(f)
    logging.debug(json.dumps(config_dict, indent=4))

    database_config = config_dict['DatabaseConfig']
    table_config = config_dict['TableConfigs'][table_name]
    glue_database = database_config['target_db_name']
    glue_table_name = f"{database_config['identifier']}_{table_name.replace('.','_')}"

    hudi_options = get_hudi_options(glue_table_name, glue_database, table_config['hudi_config'], 'INCREMENTAL')

    files = table_config['file_list']

    spark = SparkSession \
        .builder \
        .appName(f'{table_name}_HudiLake_upsert') \
        .getOrCreate()
    spark.sparkContext.setLogLevel(log_level)

    #df2 = spark.read.format('org.apache.hudi').options(**hudi_options).load(os.path.join(lake_location_uri, glue_table_name, ''))
    #df2.printSchema()

    spark.read.parquet(*files) \
        .write \
        .format('org.apache.hudi') \
        .options(**hudi_options) \
        .mode('append') \
        .save(os.path.join(lake_location_uri, glue_table_name, ''))


if __name__ == "__main__":
    main()
