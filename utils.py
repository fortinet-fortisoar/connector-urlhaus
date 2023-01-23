import requests, io
import json
from connectors.core.connector import get_logger, ConnectorError
from .constants import LOGGER_NAME

logger = get_logger(LOGGER_NAME)


def invoke_rest_endpoint(config, endpoint, method='GET', data=None, headers=None):
    if headers is None:
        headers = {'accept': 'application/json'}

    # utility function for a sample rest based integration using basic authentication
    # change as required for the specific integration being built

    server_fqhn = config.get('server_fqhn')
    # port = config.get('port', '443')
    # username = config.get('username')
    # password = config.get('password')
    # protocol = config.get('protocol', 'https')
    verify_ssl = True
    if not server_fqhn:
        raise ConnectorError('Missing required parameters')
    url = server_fqhn + endpoint
    try:
        response = requests.request(method, url, auth=('username', 'password'), verify=verify_ssl,
                                    data=None, headers=headers)
    except Exception as e:
        logger.exception('Error invoking endpoint: {0}'.format(endpoint))
        raise ConnectorError('Error: {0}'.format(str(e)))
    if response.ok:
        return response
    else:
        logger.error(response.content)
        raise ConnectorError(response.content)


def query_endpoint(endpoint, data, method='POST', headers=None ):
    if headers is None:
        headers = {'accept': 'application/json'}
    verify_ssl = True
    url = endpoint
    try:
        response = requests.request(method, url, data=data, verify=verify_ssl,
                                    headers=headers, stream=True)
    except Exception as e:
        logger.exception('Error invoking endpoint: {0}'.format(endpoint))
        raise ConnectorError('Error: {0}'.format(str(e)))
    if response.ok:
        return response
    else:
        logger.error(response.content)
        raise ConnectorError(response.content)
