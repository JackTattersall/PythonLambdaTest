import json


def handler(event, context):
    data = {
        "response": event['body']
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
