import boto3
import json
import logging
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key

sfn_arn = os.environ.get('STEPFUNCTION_ARN',
               'arn:aws:states:us-east-1:831275422924:stateMachine:FullLoadStepFunction-sFRyZzGfBnid')
config_table = os.environ.get('CONFIG_TABLE',
               'da-black-belt-2021-DynamoDbStack-Q4N7US2STWHU-RdbmsConfigTable-E4SG2QC95RL8')
runtime_bucket = os.environ.get('RUNTIME_BUCKET', 'adamn-831275422924')

log_level = os.environ.get('LOG_LEVEL', logging.INFO)

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level)


def write_configs(execution_id, data):
    object_prefix = f'runtime/stepfunctions/{sfn_arn.split(":")[-1]}/{execution_id}/'
    s3 = boto3.resource('s3')
    s3.Object(runtime_bucket, os.path.join(object_prefix, "full_load_configs.json")).put(Body=data.encode('utf-8'))
    s3_uri = os.path.join('s3://', runtime_bucket, object_prefix)

    return s3_uri


def munge_configs(input_list):
    configs = {
        'DatabaseConfig': {},
        'TableConfigs': {}
    }
    for config in input_list:
        if config['config'] == 'database::config':
            configs['DatabaseConfig'] = config
        elif config['config'].startswith('table::'):
            configs['TableConfigs'][config['config'].split('::')[-1]] = config
        else:
            raise RuntimeError('Unsupported config type')
    table_list = [x for x in configs['TableConfigs'].keys()]

    return configs, table_list


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


def launch_sfn(identifier, execution_id, config_s3_uri, table_list):
    client = boto3.client('stepfunctions')
    sfn_input = {
        'lambda': {
            'identifier': identifier,
            'runtime_configs': config_s3_uri,  # && sudo chmod -R 755 $_
            'table_list': table_list
        }
    }
    response = client.start_execution(
        stateMachineArn=sfn_arn,
        name=execution_id,
        input=json.dumps(sfn_input)
    )
    return response


def handler(event, context=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    identifier = event['Identifier']
    execution_id = f'{identifier}-{timestamp}'
    config_dict, table_list = get_configs(identifier)
    config_s3_uri = write_configs(execution_id, json.dumps(config_dict, indent=4))
    logging.info(f'Runtime config written to: {config_s3_uri}.')
    response = launch_sfn(identifier, execution_id, config_s3_uri, table_list)

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
