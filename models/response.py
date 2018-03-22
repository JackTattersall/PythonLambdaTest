import json


class Response:
    def __init__(self, body: str, status_code=200):
        self.body = body
        self.status_code = status_code
        self.headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
        }

    def to_json(self):
        response_json = {
            'statusCode': self.status_code,
            'headers': self.headers,
            'body': self.body
        }

        return response_json
