# import unittest
# import risk_handler
# import prospect_handler
#
#
# class TestHandlerCase(unittest.TestCase):
#     def test_hello_world_response(self):
#         print("testing response.")
#         result = risk_handler.handler({"body": '{"test_body_key": "test body value"}'}, None)
#         print(result)
#         self.assertEqual(result['statusCode'], 200)
#         self.assertEqual(result['headers']['Content-Type'], 'application/json')
#         self.assertEqual('{"person": {"test_body_key": "test body value"}, "jwt": ""}', result['body'])
#
#     def test_hello_response(self):
#         print("testing response.")
#         result = prospect_handler.handler({"body": '{"test_body_key": "test body value"}'}, None)
#         print(result)
#         self.assertEqual(result['statusCode'], 200)
#         self.assertEqual(result['headers']['Content-Type'], 'application/json')
#         self.assertEqual('{"person": {"test_body_key": "test body value"}, "jwt": ""}', result['body'])
#
#
# if __name__ == '__main__':
#     unittest.main()
