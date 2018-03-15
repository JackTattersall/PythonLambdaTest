import unittest
import risk_handler
import prospect_handler


class TestHandlerCase(unittest.TestCase):

    def test_hello_world_response(self):
        print("testing response.")
        result = risk_handler.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        #self.assertIn('Hello World', result['body'])

    def test_hello_response(self):
        print("testing response.")
        result = prospect_handler.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        # self.assertIn('Hello World', result['body'])

        # event = {
        #     'pathParameters': {
        #         'name': 'testname'
        #     }
        # }
        #
        # context = {}
        #
        # expected = {
        #     'body': '{"output": "Hello testname"}',
        #     'headers': {
        #         'Content-Type': 'application/json'
        #     },
        #     'statusCode': 200
        # }
        #
        # self.assertEqual(prospect_handler.handler(event, context), expected)


if __name__ == '__main__':
    unittest.main()
