import boto3
import json
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger

logger = Logger()

sfn_arn = os.environ.get('STEPFUNCTION_ARN')
config_table = os.environ.get('CONFIG_TABLE')
runtime_bucket = os.environ.get('RUNTIME_BUCKET')
bronze_lake_uri = os.environ['BRONZE_LAKE_S3URI']
silver_lake_uri = os.environ['SILVER_LAKE_S3URI']


def write_configs(execution_id, data):
    object_prefix = f'runtime/stepfunctions/{sfn_arn.split(":")[-1]}/{execution_id}/'
    s3 = boto3.resource('s3')
    s3.Object(runtime_bucket, os.path.join(object_prefix, "configs.json")).put(Body=data.encode('utf-8'))
    s3_uri = os.path.join('s3://', runtime_bucket, object_prefix)

    return s3_uri


def munge_configs(items, pipeline_type):
    configs = {
        'DatabaseConfig': {},
        'TableConfigs': {},
        'EmrConfigs': {}
    }
    for config in items:
        if config['config'] == 'database::config':
            configs['DatabaseConfig'] = config
        elif config['config'].startswith('table::'):
            configs['TableConfigs'][config['config'].split('::')[-1]] = config
        elif config['config'].startswith('emr::config::'):
            if config['config'].split('::')[-1] == pipeline_type:
                configs['EmrConfigs'] = config
                configs['EmrConfigs']['step_parallelism'] = int(config['step_parallelism'])
                configs['EmrConfigs']['worker']['count'] = int(config['worker']['count'])
                logger.info(f'Pipeline type: {pipeline_type}')
            else:
                pass
        else:
            raise RuntimeError('Unsupported config type')

    return configs


def get_configs(identifier, pipeline_type):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(config_table)
    items = []
    response = table.query(
        KeyConditionExpression=Key('identifier').eq(identifier)
    )
    for item in response['Items']:
        items.append(item)

    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('identifier').eq(identifier),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            items.append(item)

    configs = munge_configs(items, pipeline_type)
    return configs


def get_hudi_configs(source_table_name, target_table_name, database_name, table_config, pipeline_type):
    primary_key = table_config['primary_key']
    precombine_field = table_config['watermark']
    glue_database = database_name

    hudi_conf = {
        'hoodie.table.name': target_table_name,
        'hoodie.datasource.write.recordkey.field': primary_key,
        'hoodie.datasource.write.precombine.field': precombine_field,
        'hoodie.datasource.hive_sync.database': glue_database,
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.table': target_table_name
    }

    if pipeline_type == 'seed_hudi':
        source_s3uri = os.path.join(bronze_lake_uri, 'full', source_table_name.replace('_', '/', 2), '')
        hudi_conf['hoodie.datasource.write.operation'] = 'bulk_insert'
        hudi_conf['hoodie.bulkinsert.sort.mode'] = 'PARTITION_SORT'
    elif pipeline_type in ['incremental_hudi', 'continuous_hudi']:
        source_s3uri = os.path.join(bronze_lake_uri, 'cdc', target_table_name.replace('_', '/', 2), '')
        hudi_conf['hoodie.datasource.write.operation'] = 'upsert'
    else:
        raise ValueError(f'Operation {pipeline_type} not yet supported.')

    hudi_conf['hoodie.deltastreamer.source.dfs.root'] = source_s3uri

    if table_config['is_partitioned'] is False:
        partition_extractor = 'org.apache.hudi.hive.NonPartitionedExtractor'
        key_generator = 'org.apache.hudi.keygen.NonpartitionedKeyGenerator'
    else:
        partition_extractor = table_config['partition_extractor_class']
        hudi_conf['hoodie.datasource.write.hive_style_partitioning'] = 'true'
        hudi_conf['hoodie.datasource.write.partitionpath.field'] = table_config['partition_path']
        hudi_conf['hoodie.datasource.hive_sync.partition_fields'] = table_config['partition_path']
        if len(primary_key.split(',')) > 1:
            key_generator = 'org.apache.hudi.keygen.ComplexKeyGenerator'
        else:
            key_generator = 'org.apache.hudi.keygen.SimpleKeyGenerator'

    hudi_conf['hoodie.datasource.write.keygenerator.class'] = key_generator

    if 'transformer_sql' in table_config:
        hudi_conf['hoodie.deltastreamer.transformer.sql'] = table_config['transformer_sql']

    hudi_conf['hoodie.datasource.hive_sync.partition_extractor_class'] = partition_extractor

    logger.debug(json.dumps(hudi_conf, indent=4))

    return hudi_conf


def generate_sfn_input(identifier, config_s3_uri, configs, pipeline_type):
    tables = []
    for table in configs['TableConfigs'].keys():
        config = configs['TableConfigs'][table]
        logger.debug(json.dumps(config, indent=4))
        if 'enabled' in config and config['enabled'] is True:
            spark_submit_args = ['spark-submit']
            if pipeline_type == 'full_load':
                if 'spark_conf' in config and 'full_load' in config['spark_conf']:
                    for k, v in config['spark_conf']['full_load'].items():
                        spark_submit_args.extend(['--conf', f'{k}={v}'])

                spark_submit_args.extend(['/mnt/var/lib/instance-controller/public/scripts/full_load.py', '--table_name', table])
                entry = {
                    'table_name': table,
                    'jar_step_args': spark_submit_args
                }

            elif pipeline_type in ['seed_hudi', 'continuous_hudi', 'incremental_hudi']:
                target_db_name = configs['DatabaseConfig']['target_db_name']
                source_table_name = '_'.join(
                    [configs['DatabaseConfig']['target_table_prefix'], table.replace('.', '_')])

                # Add the ability to redirect to custom target table names
                if 'override_target_table_name' in config:
                    target_table_name = config['override_target_table_name']
                # Otherwise infer target table name from source
                else:
                    target_table_name = source_table_name

                if 'spark_conf' in config and pipeline_type in config['spark_conf']:
                    for k, v in config['spark_conf'][pipeline_type].items():
                        spark_submit_args.extend(['--conf', f'{k}={v}'])

                spark_submit_args.extend([
                    '--class', 'org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer',
                    '/usr/lib/hudi/hudi-utilities-bundle.jar',
                    '--table-type', 'COPY_ON_WRITE',
                    '--source-class', 'org.apache.hudi.utilities.sources.ParquetDFSSource',
                    '--enable-hive-sync',
                    '--target-table', target_table_name,
                    '--target-base-path', os.path.join(silver_lake_uri, target_table_name, ''),
                    '--source-ordering-field', config['hudi_config']['watermark']
                ])

                if 'transformer_class' in config['hudi_config']:
                    spark_submit_args.extend(['--transformer-class', config['hudi_config']['transformer_class']])

                if pipeline_type == 'seed_hudi':
                    spark_submit_args.extend(['--op', 'BULK_INSERT'])

                if pipeline_type == 'continuous_hudi':
                    spark_submit_args.extend(['--continuous'])

                hudi_configs = get_hudi_configs(source_table_name, target_table_name, target_db_name, config['hudi_config'], pipeline_type)
                for k, v in hudi_configs.items():
                    spark_submit_args.extend(['--hoodie-conf', f'{k}={v}'])

                entry = {
                    'table_name': table,
                    'jar_step_args': spark_submit_args
                }
            else:
                raise RuntimeError('Invalid PipelineType in event. Must be [full_load, seed_hudi, continuous_hudi]')

            tables.append(entry)
            logger.info(f'Table added to stepfunction input: {json.dumps(entry, indent=4)}')
        else:
            logger.info(f'Table {table} is disabled, skipping. To enable, set attribute "enabled": true')
            continue
    sfn_input = {
        'lambda': {
            'identifier': identifier,
            'pipeline_type': pipeline_type,
            'runtime_configs': config_s3_uri,
            'tables': tables,
            'emr': configs['EmrConfigs'],
            'log_level': os.environ.get('LOG_LEVEL', 'INFO')
        }
    }
    return sfn_input


def launch_sfn(execution_id, sfn_input):
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn=sfn_arn,
        name=execution_id,
        input=json.dumps(sfn_input)
    )
    return response


@logger.inject_lambda_context
def handler(event, context=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    identifier = event['Identifier']
    pipeline_type = event['PipelineType']
    execution_id = f'{identifier}-{pipeline_type}-{timestamp}'
    config_dict = get_configs(identifier, pipeline_type)
    config_s3_uri = write_configs(execution_id, json.dumps(config_dict, indent=4))
    logger.info(f'Runtime config written to: {config_s3_uri}.')
    sfn_input = generate_sfn_input(identifier, config_s3_uri, config_dict, pipeline_type)
    response = launch_sfn(execution_id, sfn_input)

    return {
        "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "executionArn ": response['executionArn']
        })
    }


if __name__ == '__main__':
    test_event={
        'Identifier': 'hammerdb'
    }

    handler(event=test_event)
