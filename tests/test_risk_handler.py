import unittest
import risk_handler
import prospect_handler


class TestHandlerCase(unittest.TestCase):
    def test_hello_world_response(self):
        print("testing response.")
        result = risk_handler.handler({"body": "test body"}, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('test body', result['body']['person'])

    def test_hello_response(self):
        print("testing response.")
        result = prospect_handler.handler({"body": "test body"}, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('test body', result['body']['person'])


if __name__ == '__main__':
    unittest.main()
