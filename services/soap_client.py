import zeep
import xmltodict
from os import environ


class XStreamMessageService:
    """
    Entry point for parsing json(dict) data into a valid XStream schema
    """
    def __init__(self):
        self.template = {
            'xmlexecute': {
                'job': {
                    'queue': '1'
                },
                'parameters': {
                    'yzt': {
                        'Char20.1': None
                    }
                },
                'apmdata': {
                    'prospect': {
                        'p.cm': None
                    }
                },
                'apmpolicy': {
                    'p.py': {
                        'Ptype': None
                    }
                }
            }
        }

    def _add_apm(self, json: dict):
        self.template['xmlexecute']['apmdata']['prospect']['p.cm'] = json

    def _add_policy_type(self, policy_type: str):
        self.template['xmlexecute']['apmpolicy']['p.py']['Ptype'] = policy_type

    def _add_risk_data(self, risk_data: dict):
        for risk_frame, values in risk_data.items():
            self.template['xmlexecute']['apmpolicy'][risk_frame] = values

    def _add_polref(self, polref: str):
        self.template['xmlexecute']['apmpolicy']['p.py']['Polref'] = polref

    def _add_ref(self, ref: str):
        self._add_apm({'Refno': ref})

    def _add_function_type(self, function_type: str):
        self.template['xmlexecute']['parameters']['yzt']['char20.1'] = function_type

    def _parse_to_xml(self):
        parsed_dict = xmltodict.unparse(self.template, full_document=False)
        return parsed_dict

    @staticmethod
    def post(message: str) -> str:
        client = zeep.Client(wsdl='https://openinterchange.openecommerce.co.uk/OpenInterchange/OpenInterchange?wsdl')
        response = client.service.processMessage(
            environ[''], environ[''], environ[''], environ[''], environ[''], message, 0)
        return response

    def process_response(self):
        pass

    def create_prospect_message(self, prospect_json: dict):
        self._add_apm(prospect_json)
        self._add_function_type('create-cliv-prospect')
        prospect_message = self._parse_to_xml()
        return prospect_message

    def create_risk_message(self, policy_json: dict):
        self._add_ref(policy_json['Ref'])
        self._add_policy_type(policy_json['Ptype'])
        self._add_risk_data(policy_json['Risk'])
        self._add_function_type('create-cliv-policy')
        risk_message = self._parse_to_xml()
        return risk_message

    def create_transaction_message(self, transaction_json: dict):
        self._add_ref(transaction_json['Ref'])
        self._add_polref(transaction_json['Polref'])
        self._add_function_type('cliv_transfer')
        transaction_message = self._parse_to_xml()
        return transaction_message
