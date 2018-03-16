import json


def handler(event, context):
    data = event['body']
    return {
        'statusCode': 200,
        'body': data,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'www.dave.com'
        }
    }
