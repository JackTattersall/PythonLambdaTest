from enum import Enum


class ResponseType(Enum):
    PROSPECT = 'prospect'
    RISK = 'risk'
    TRANSACTION = 'transaction'


class ResponseLookup(Enum):
    POLREF = 'xmlreply/apmdata/apmpolicy/p.py/polref'
    REFNO = 'xmlreply/apmdata/prospect/p.cm/refno'
    PREMIUM = 'xmlreply/apmdata/apmpolicy/cs01/Total.prem'
    CLIENT_REF = 'xmlreply/apmdata/apmpolicy/p.py/brooms.ref'
    RESPONSE_STATUS = 'xmlreply/messages/result'
    ERRORS = 'xmlreply/messages/error'


class FunctionTypes(Enum):
    CREATE_PROSPECT = 'create-cliv-prospect'
    CREATE_RISK = 'create-cliv-policy'
    TRANSACT = 'cliv-transfer'
