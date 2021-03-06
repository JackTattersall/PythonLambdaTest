import jwt
import json
from services import soap_client


def handler(event, context):
    data = json.loads(event['body'])
    decoded_jwt = None
    try:
        decoded_jwt = jwt.decode(event['headers']['Authorization'], 'paigeleah1')
    except Exception as e:
        pass

    return {
        'statusCode': 200,
        'body': json.dumps({
            'person': data,
            'jwt': decoded_jwt or ""
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'www.dave.com',
            'Access-Control-Allow-Methods': 'OPTION,POST',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
    }
