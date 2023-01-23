from connectors.core.connector import get_logger, ConnectorError
from .utils import query_endpoint
from .constants import LOGGER_NAME
import re, json
from io import StringIO

logger = get_logger(LOGGER_NAME)

def query_hash(config, params, *args, **kwargs):
    apiurl = config.get('query_server_fqhn')
    hash = params.get('hash')

    if re.match('^[a-fA-F0-9]{32}$', hash, ) != None:
        request_body = {'md5_hash' : hash }
    elif re.match('^[a-fA-F0-9]{64}$', hash ) != None:
        request_body = {'sha256_hash' : hash }
    else:
        test = re.match(hash, '[a-fA-F\d]{32}')
        raise ConnectorError('Invalid hash type, not MD5 or SHA254')

    if not apiurl:
        raise ConnectorError('Missing required input')

    endpoint = apiurl + 'v1/payload/'

    headers = {
        'accept': 'multipart/form-data',
        'Accept-Encoding' : 'gzip, deflate, br'
    }
    api_response = query_endpoint(endpoint, data=request_body, headers=headers).content.decode('utf8')
    if api_response != '':
        io = StringIO(api_response)
        return json.load(io)
    else:
        return None