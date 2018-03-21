import jwt
import json

from models.response import Response
from services.prospect_service import ProspectService
from os import environ


def handler(event, context):
    prospect = json.loads(event['body'])
    print(event)

    # todo move jwt functionality into a service class to keep things dry
    try:
        # todo make jwt secret an env var
        jwt.decode(event['headers']['Authorization'], 'paigeleah1')
    except Exception as e:
        print('Error: jwt did not decode correctly - {}'.format(e))
        return Response('Unauthorized', status_code=401)

    prospect_service = ProspectService()
    api_response = prospect_service.create_prospect(prospect)

    return api_response.to_json()
