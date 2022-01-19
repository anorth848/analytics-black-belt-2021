import argparse
import json
import logging
import os
from datetime import datetime
from hudi import get_hudi_options
from jdbc import get_spark_jdbc
from pyspark.sql.functions import lit

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
    f = open('/mnt/var/lib/instance-controller/public/runtime_configs/full_load_configs.json')
    config_dict = json.load(f)
    logging.debug(json.dumps(config_dict, indent=4))

    database_config = config_dict['DatabaseConfig']
    table_config = config_dict['TableConfigs'][table_name]
    secret_id = database_config['secret']
    glue_database = database_config['target_db_name']
    glue_table_name = f"{database_config['identifier']}_{table_name.replace('.','_')}"
    trx_seq = None
    spark_jdbc_config = table_config['spark_jdbc_config'] if 'spark_jdbc_config' in table_config else None

    hudi_options = get_hudi_options(glue_table_name, glue_database, table_config['hudi_config'], 'FULL')
    spark_jdbc = get_spark_jdbc(secret_id, table_name, spark_jdbc_config)
    precombine_field = hudi_options['hoodie.datasource.write.precombine.field']

    if precombine_field == 'trx_seq':
        # Downstream we will merge CDC using AR_H_CHANGE_SEQ as the key if trx_seq is the precombine field
        # https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.SelectionTransformation.Expressions.html#CHAP_Tasks.CustomizingTasks.TableMapping.SelectionTransformation.Expressions-Headers
        # Generate this field for the full load
        trx_seq = datetime.now().strftime('%Y%m%d%H%M%S000000000000000000000')

    jdbc_df = spark_jdbc.load() \
        .withColumn('trx_op', lit('INSERT'))

    if trx_seq is not None:
        final_df = jdbc_df.withColumn('trx_seq', lit(trx_seq))
    else:
        final_df = jdbc_df

    final_df.write \
        .format('org.apache.hudi') \
        .options(**hudi_options) \
        .mode('overwrite') \
        .save(os.path.join(lake_location_uri, glue_table_name, ''))


if __name__ == "__main__":
    main()
