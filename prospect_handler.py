import json


def handler(event, context):
    data = {
        "response": event
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
