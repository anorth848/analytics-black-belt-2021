import argparse
import json
import logging
import os
from pyspark.sql import SparkSession

source_location_uri = os.path.join(os.environ['SILVER_LAKE_S3URI'], '')
destination_location_ur = os.path.join(os.environ['GOLD_LAKE_S3URI'], '')
log_level = os.environ.get('LOG_LEVEL', 'INFO')

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--not_implemented', default='not_yet')
    args = parser.parse_args()
    return args

def get_hudi_options(instant_time):
    hudi_options = {
        'hoodie.datasource.query.type': 'incremental',
        'hoodie.datasource.read.begin.instanttime': instant_time
    }
    return hudi_options

def main():
    args = get_args()
    table_name = args.not_implemented
    f = open('/mnt/var/lib/instance-controller/public/runtime_configs/configs.json')
    config_dict = json.load(f)
    logging.info(json.dumps(config_dict, indent=4))

    database_config = config_dict['DatabaseConfig']
    db_name = database_config['target_db_name']
    print(database_config)
    step = config_dict['StepConfigs']['denormalize_order_line']

    spark = SparkSession \
        .builder \
        .appName(f'{db_name}_denormalize') \
        .getOrCreate()

    hudi_opts = get_hudi_options(20220207202729)
    count = spark.read.format('org.apache.hudi').options(**hudi_opts).load(os.path.join(source_location_uri, 'hammerdb_public_order_line', '')).count()
    print(count)


if __name__ == "__main__":
    main()