from connectors.core.connector import get_logger, ConnectorError
from .utils import query_endpoint
from .constants import LOGGER_NAME
import re, json
from io import StringIO

logger = get_logger(LOGGER_NAME)

def query_ip(config, params, *args, **kwargs):
    apiurl = config.get('query_server_fqhn')
    ip = params.get('domain')
    if not apiurl:
        raise ConnectorError('Missing required input')
    endpoint = apiurl + 'v1/host/'
    request_body = {'host' : ip }
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