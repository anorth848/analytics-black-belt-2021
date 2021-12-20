import boto3
import json
from datetime import datetime


def launch_sfn(stepfunction, identifier):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    client = boto3.client('stepfunctions')
    sfn_input = {
        'input': {
            'lambda': {
                'identifier': identifier
            }
        }
    }
    response = client.start_execution(
        stateMachineArn=stepfunction,
        name=f'{identifier}-{timestamp}',
        input=json.dumps(sfn_input)
    )
    return response


def handler(event, context=None):
    stepfunction = event['StepFunction']
    identifier = event['Identifier']
    response = launch_sfn(stepfunction, identifier)
    print(response)


if __name__ == '__main__':
    test_event={
        'StepFunction': 'arn:aws:states:us-east-1:831275422924:stateMachine:FullLoadStepFunction-sFRyZzGfBnid',
        'Identifier': 'hammerdb'
    }
    handler(event=test_event)
