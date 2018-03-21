import os
import unittest

from models.enums import ResponseType, ResponseLookup
from services.soap_client import XStreamMessageService
import mock
import re


# helper function to read test files
def read_file_to_string(file_name):
    file_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'tests/test_files/{}'.format(file_name))

    with open(file_path, 'r') as myfile:
        return re.sub(r'\s+', '', myfile.read())


class TestCreateMessage(unittest.TestCase):
    def setUp(self):
        self.service = XStreamMessageService()
        self.mock_prospect = {'name': 'Bob_Test', 'email': 'bob@test.com'}
        self.mock_risk = {
            'RiskFrame1': {
                'RiskField1': 'RiskValue1'
            }
        }
        self.mock_ptype = 'DG'
        self.mock_ref = 'BOBX01'
        self.mock_polref = 'BOBX01DG01'

    # Function always required
    # Keep in mind, all white space, tabs and new lines are stripped from test file

    # smoke test
    def test_with_no_kwargs(self):
        result = self.service.create_message('test-function')
        expected = read_file_to_string('create_message_no_kwargs.xml')
        self.assertEqual(expected, result)

    # create prospect
    def test_prospect_only(self):
        result = self.service.create_message('test-function', prospect=self.mock_prospect)
        expected = read_file_to_string('create_message_prospect_only.xml')
        self.assertEqual(expected, result)

    # create policy (risk)
    def test_refno_ptype_and_risk(self):
        result = self.service.create_message(
            'test-function', refno=self.mock_ref, ptype=self.mock_ptype, risk=self.mock_risk
        )
        expected = read_file_to_string('create_message_refno_ptype_and_risk.xml')
        self.assertEqual(expected, result)

    # transact
    def test_refno_and_polref(self):
        result = self.service.create_message('test-function', refno=self.mock_ref, polref=self.mock_polref)
        expected = read_file_to_string('create_message_refno_and_polref.xml')
        self.assertEqual(expected, result)

    # handle errors
    @mock.patch('services.soap_client.xmltodict.unparse')
    @mock.patch('services.soap_client.print')
    def test_exceptions_are_caught_handled_printed_to_std_out_and_reraised(
            self, mock_print: mock.MagicMock, mock_unparse: mock.MagicMock
    ):

        mock_unparse.side_effect = Exception('test exception')

        with(self.assertRaises(Exception)):
            self.service.create_message('test-function')

        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_has_calls(
            calls=[
                mock.call('Info: creating xstream message'),
                mock.call('Error: error in create_message - test exception')
            ]
        )


class TestProcessMessage(unittest.TestCase):
    def setUp(self):
        self.service = XStreamMessageService()

    @mock.patch('services.soap_client.zeep.Client')
    def test_process_message_called_with_correct_parameters(self, mock_client):
        client_return_value = mock.MagicMock()
        client_return_value.service.processMessage = mock.MagicMock()
        mock_client.return_value = client_return_value

        mock_message = read_file_to_string('create_message_no_kwargs.xml')
        self.service.process_message(mock_message)

        # using ANY so not to expose service access details, message is all we are interested in
        client_return_value.service.processMessage.assert_called_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock_message, mock.ANY
        )

    # handle errors
    @mock.patch('services.soap_client.zeep.Client')
    @mock.patch('services.soap_client.print')
    def test_exceptions_are_caught_handled_printed_to_std_out_and_reraised(
            self, mock_print, mock_client
    ):
        mock_client.side_effect = Exception('test exception')

        with(self.assertRaises(Exception)):
            self.service.process_message('mock message')

        self.assertEqual(mock_print.call_count, 2)

        mock_print.assert_has_calls(
            calls=[
                mock.call('Info: Processing message'),
                mock.call('Error: Posting to xstream failed - test exception')
            ]
        )


class TestProcessResponse(unittest.TestCase):
    def setUp(self):
        self.service = XStreamMessageService()

    # Test the correct responses are returned or exceptions/errors are handled correctly, given the different
    # shapes of xstreams soap client responses

    # --------------------PROSPECT------------------
    def test_process_response_prospect_valid(self):
        result = self.service.process_response(
            read_file_to_string('process_response_prospect_valid.xml'),
            ResponseType.PROSPECT
        )

        expected = '{"refno": "BOBX01"}'

        self.assertEqual(expected, result)

    @mock.patch('services.soap_client.print')
    def test_process_response_prospect_exception(self, mock_print):

        with self.assertRaises(KeyError):
            self.service.process_response(
                read_file_to_string('process_response_prospect_exception.xml'),
                ResponseType.PROSPECT
            )

        mock_print.assert_has_calls(
            calls=[
                mock.call('Info: Processing response for prospect'),
                mock.call(
                    "Error: key error on xml response, has the xstream response model"
                    " changed? - '{}'".format(ResponseLookup.REFNO.value))
            ]
        )

    # --------------------RISK------------------
    def test_process_response_risk_valid(self):
        result = self.service.process_response(
            read_file_to_string('process_response_risk_valid.xml'),
            ResponseType.RISK
        )

        expected = '{"polref": "BOBX001DG1", "refno": "BOBX001", "premium": "10000"}'

        self.assertEqual(expected, result)

    @mock.patch('services.soap_client.print')
    def test_process_response_risk_exception(self, mock_print):
        with self.assertRaises(KeyError):
            self.service.process_response(
                read_file_to_string('process_response_risk_exception.xml'),
                ResponseType.RISK
            )

        mock_print.assert_has_calls(
            calls=[
                mock.call('Info: Processing response for risk'),
                mock.call(
                    "Error: key error on xml response, has the xstream response model"
                    " changed? - '{}'".format(ResponseLookup.POLREF.value))
            ]
        )

    # todo test transaction responses once we know what they should be.

    # --------------------RISK------------------
    @mock.patch('services.soap_client.print')
    def test_process_response_error(self, mock_print):
        with self.assertRaises(Exception):
            self.service.process_response(
                read_file_to_string('process_response_error.xml'),
                ResponseType.RISK
            )

        mock_print.assert_has_calls(
            calls=[
                mock.call('Info: Processing response for risk'),
                mock.call("Error: xstream responded with errors ['errornumber1', 'errornumber2']")
            ]
        )