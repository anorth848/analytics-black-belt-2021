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
bronze_lake_uri = os.path.join(os.environ['BRONZE_LAKE_S3URI'], '')
silver_lake_uri = os.path.join(os.environ['SILVER_LAKE_S3URI'], '')


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


def get_hudi_configs(table_name, database_name, table_config, pipeline_type):
    primary_key = table_config['primary_key']
    precombine_field = table_config['watermark']
    glue_database = database_name

    if pipeline_type == 'seed_hudi':
        source_s3uri = f"{bronze_lake_uri}/full/{table_name.replace('_', '/')}"
    # assume continuous(cdc) if not initial seed
    else:
        source_s3uri = f"{bronze_lake_uri}/cdc/{table_name.replace('_', '/')}"

    hudi_conf = {
        'hoodie.table.name': table_name,
        'hoodie.datasource.write.recordkey.field': primary_key,
        'hoodie.datasource.write.precombine.field': precombine_field,
        'hoodie.datasource.hive_sync.database': glue_database,
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.table': table_name,
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.deltastreamer.source.dfs.root': source_s3uri
    }

    if table_config['is_partitioned'] is False:
        extractor = 'org.apache.hudi.hive.NonPartitionedExtractor'
        key_generator = 'org.apache.hudi.keygen.NonpartitionedKeyGenerator'
    else:
        extractor = table_config['partition_extractor_class']
        hudi_conf['hoodie.datasource.write.partitionpath.field'] = table_config['partition_path']
        key_generator = 'org.apache.hudi.keygen.ComplexKeyGenerator'

    hudi_conf['hoodie.datasource.hive_sync.partition_extractor_class'] = extractor
    hudi_conf['hoodie.datasource.write.keygenerator.class'] = key_generator
    #  Not required with latest Hudi libraries, should be inferred based on recordkey.field
    # 'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.ComplexKeyGenerator',
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

            elif pipeline_type in ['seed_hudi', 'continuous_hudi']:
                target_db_name = configs['DatabaseConfig']['target_db_name']
                target_table_name = '_'.join([configs['DatabaseConfig']['target_table_prefix'], table.replace('.', '_')])
                if 'spark_conf' in config and 'seed_hudi' in config['spark_conf']:
                    for k, v in config['spark_conf']['seed_hudi'].items():
                        spark_submit_args.extend(['--conf', f'{k}={v}'])

                spark_submit_args.extend([
                    '--class', 'org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer',
                    '/usr/lib/hudi/hudi-utilities-bundle.jar',
                    '--table-type', 'COPY_ON_WRITE',
                    '--source-class', 'org.apache.hudi.utilities.sources.ParquetDFSSource',
                    '--enable-hive-sync',
                    '--target-table', target_table_name,
                    '--target-base-path', os.path.join(silver_lake_uri, target_table_name)
                ])
                if pipeline_type == 'continuous_hudi':
                    spark_submit_args.extend(['--continuous'])

                hudi_configs = get_hudi_configs(target_table_name, target_db_name, config['hudi_config'], pipeline_type)
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
