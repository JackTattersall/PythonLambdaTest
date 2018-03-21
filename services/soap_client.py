import json
from models.enums import ResponseType, ResponseLookup

import zeep
import xmltodict
from os import environ
import dpath.util as dict_xpath


class XStreamMessageService(object):
    """
    Entry point for parsing json(dict) data into a valid XStream schema
    """
    @staticmethod
    def create_message(xstream_function: str, refno='', ptype='', polref='', prospect=None, risk=None) -> str:
        print('Info: creating xstream message')

        try:

            template = {
                'xmlexecute': {
                    'job': {
                        'queue': '1'
                    },
                    'parameters': {
                        'yzt': {
                            'Char20.1': xstream_function
                        }
                    },
                    'apmdata': {
                        'prospect': {
                            'p.cm': prospect or {'refno': refno}
                        }
                    },
                    'apmpolicy': {
                        'p.py': {
                            'polref': polref,
                            'ptype': ptype
                        }
                    }
                }
            }

            if risk:
                for risk_frame, risk_fields in risk.items():
                    dict_xpath.new(template, 'xmlexecute/apmpolicy/{}'.format(risk_frame), risk_fields)

            parsed_template = xmltodict.unparse(template, full_document=False)
        except Exception as e:
            print('Error: error in create_message - {}'.format(e))
            raise Exception(e)

        return parsed_template

    @staticmethod
    def process_message(message: str) -> str:
        print('Info: Processing message')

        # todo add wsdl url and auth tokens to env var
        try:
            client = zeep.Client(
                wsdl='https://openinterchange.openecommerce.co.uk/OpenInterchange/OpenInterchange?wsdl'
            )

            response = client.service.processMessage(
                environ['messageType'],
                environ['branch'],
                environ['marsReference'],
                environ['bNumber'],
                environ['licenseKey'],
                message,
                int(environ['timeout'])
            )
        except Exception as e:
            print('Error: Posting to xstream failed - {}'.format(e))
            raise Exception(e)

        return response

    @staticmethod
    def process_response(response: str, response_type: ResponseType) -> str:
        print('Info: Processing response for {}'.format(response_type.value))

        parsed_response = xmltodict.parse(response)

        response_status = dict_xpath.get(parsed_response, ResponseLookup.RESPONSE_STATUS.value).lower()

        client_response_body = {}

        if response_status == 'ok':

            if response_type == ResponseType.PROSPECT:
                try:
                    client_response_body['refno'] = dict_xpath.get(parsed_response, ResponseLookup.REFNO.value)
                except KeyError as e:
                    print('Error: key error on xml response, has the xstream response model changed? - {}'.format(e))
                    raise KeyError(e)

            if response_type == ResponseType.RISK:
                try:
                    client_response_body['polref'] = dict_xpath.get(parsed_response, ResponseLookup.POLREF.value)
                    client_response_body['refno'] = dict_xpath.get(parsed_response, ResponseLookup.REFNO.value)
                    client_response_body['premium'] = dict_xpath.get(parsed_response, ResponseLookup.PREMIUM.value)
                except KeyError as e:
                    print('Error: key error on xml response, has the xstream response model changed? - {}'.format(e))
                    raise KeyError(e)

            if response_type == ResponseType.TRANSACTION:
                try:
                    client_response_body['client_ref'] = dict_xpath.get(
                        parsed_response, ResponseLookup.CLIENT_REF.value
                    )
                except KeyError as e:
                    print('Error: key error on xml response, has the xstream response model changed? - {}'.format(e))
                    raise KeyError(e)

        elif response_status == 'error':

            try:
                errors = dict_xpath.get(parsed_response, ResponseLookup.ERRORS.value)
                print('Error: xstream responded with errors {}'.format(errors))
            except KeyError as e:
                print('Error: key error on xml response, has the xstream response model changed? - {}'.format(e))

            raise Exception()

        else:
            print('Error: xstream response contains unknown response status {}'.format(response_status))
            raise Exception()

        return json.dumps(client_response_body)


class PremiumFinanceGateway(object):
    pass
