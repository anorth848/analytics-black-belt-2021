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


def write_configs(execution_id, data):
    object_prefix = f'runtime/stepfunctions/{sfn_arn.split(":")[-1]}/{execution_id}/'
    s3 = boto3.resource('s3')
    s3.Object(runtime_bucket, os.path.join(object_prefix, "full_load_configs.json")).put(Body=data.encode('utf-8'))
    s3_uri = os.path.join('s3://', runtime_bucket, object_prefix)

    return s3_uri


def munge_configs(items):
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
        elif config['config'] == 'emr::config::full_load':
            configs['EmrConfigs'] = config
            configs['EmrConfigs']['step_parallelism'] = int(config['step_parallelism'])
            configs['EmrConfigs']['worker']['count'] = int(config['worker']['count'])
        else:
            raise RuntimeError('Unsupported config type')

    return configs


def get_configs(identifier):
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

    configs = munge_configs(items)
    return configs


def generate_sfn_input(identifier, config_s3_uri, configs):
    tables = []
    for table in configs['TableConfigs'].keys():
        if 'enabled' in configs['TableConfigs'][table] and configs['TableConfigs'][table]['enabled'] is True:
            spark_submit_args = ['spark-submit']
            if 'spark_conf' in configs['TableConfigs'][table] and 'full_load' in configs['TableConfigs'][table]['spark_conf']:
                for k, v in configs['TableConfigs'][table]['spark_conf']['full_load'].items():
                    spark_submit_args.extend(['--conf', f'{k}={v}'])

            spark_submit_args.extend(['/mnt/var/lib/instance-controller/public/scripts/full_load.py', '--table_name', table])
            entry = {
                'table_name': table,
                'jar_step_args': spark_submit_args
            }
            tables.append(entry)
            logger.info(f'Table added to stepfunction input: {json.dumps(entry, indent=4)}')
        else:
            logger.info(f'Table {table} is disabled, skipping. To enable, set attribute "enabled": true')
            continue
    #table_list = [x for x in configs['TableConfigs'].keys()]
    sfn_input = {
        'lambda': {
            'identifier': identifier,
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
    execution_id = f'{identifier}-full_load-{timestamp}'
    config_dict = get_configs(identifier)
    config_s3_uri = write_configs(execution_id, json.dumps(config_dict, indent=4))
    logger.info(f'Runtime config written to: {config_s3_uri}.')
    sfn_input = generate_sfn_input(identifier, config_s3_uri, config_dict)
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
