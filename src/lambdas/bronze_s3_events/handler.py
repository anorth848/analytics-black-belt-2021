import boto3
import json
import logging
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key

log_level = os.environ.get('LOG_LEVEL', 'INFO')

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level)


def process_s3_event(event):
    return event


def put_dynamo_items(items):
    return True


def handler(event, context=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    response = {}
    print(json.dumps(event, indent=4))

    return {
        "statusCode": 200, #response['ResponseMetadata']['HTTPStatusCode'],
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(event)
    }


if __name__ == '__main__':
    test_event={
        'Identifier': 'hammerdb'
    }

    handler(event=test_event)
