from models.enums import ResponseType, FunctionTypes
from services.soap_client import XStreamMessageService
from models.response import Response


class ProspectService(object):
    def __init__(self):
        self.xstream_service = XStreamMessageService

    def create_prospect(self, prospect):
        try:
            message = self.xstream_service.create_message(FunctionTypes.CREATE_PROSPECT.value, prospect=prospect)
            service_response = self.xstream_service.process_message(message)
            api_response_body = self.xstream_service.process_response(service_response, ResponseType.PROSPECT)
            api_response = Response(api_response_body, status_code=200)
        except Exception as e:
            print('Error: create_prospect failed - {}'.format(e))
            api_response = Response('Internal server error', status_code=500)

        return api_response
