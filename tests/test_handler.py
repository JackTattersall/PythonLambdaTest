import unittest
import index
from hello import handler;


class TestHandlerCase(unittest.TestCase):

    def test_hello_world_response(self):
        print("testing response.")
        result = index.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Hello World', result['body'])

    def test_hello_response(self):
        event = {
            'pathParameters': {
                'name': 'testname'
            }
        }

        context = {}

        expected = {
            'body': '{"output": "Hello testname"}',
            'headers': {
                'Content-Type': 'application/json'
            },
            'statusCode': 200
        }

        self.assertEqual(handler(event, context), expected)


if __name__ == '__main__':
    unittest.main()
