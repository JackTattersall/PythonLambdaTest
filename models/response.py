import json


class Response:
    def __init__(self, body: str, status_code=200):
        self.body = body
        self.status_code = status_code
        self.headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'www.dave.com',
            'Access-Control-Allow-Methods': 'OPTION,POST',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }

    def to_json(self):
        response_json = {
            'statusCode': self.status_code,
            'headers': self.headers,
            'body': json.dumps(self.body)
        }

        return response_json
