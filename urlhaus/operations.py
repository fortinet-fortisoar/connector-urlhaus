"""
Copyright start
Copyright (C) 2008 - 2021 Fortinet Inc.
All rights reserved.
FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
Copyright end
"""
import base64
import json
import requests
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('urlhaus')


class urlhaus(object):
    def __init__(self, config):
        self.server_url = config.get('server_url')
        if not self.server_url.startswith('https://'):
            self.server_url = 'https://' + self.server_url
        if not self.server_url.endswith('/'):
            self.server_url += '/'
   
    def make_request(self, endpoint=None, method='GET', data=None, params=None, files=None, headers=None, timeout=None):
        try:
            url = self.server_url + endpoint
            response = requests.request(method, url, params=params, files=files, data=data, headers=headers,timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(response.text)
                raise ConnectorError({'status_code': response.status_code, 'message': response.reason})
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Url not reachable')
        except Exception as err:
            logger.exception(str(err))
            raise ConnectorError(str(err))


def login(config, params):
  haus = urlhaus(config)
  endpoint = '/v1/urls/recent/'
  response = haus.make_request(endpoint=endpoint, method='GET')
  return response

def get_url_details(config, params):
  haus = urlhaus(config)
  endpoint = '/v1/url/'
  url = params.get('URL')
  json_data = {
        'url' : url,
      }
  response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
  #requests.post(url ='https://urlhaus-api.abuse.ch/v1/url/' , data=json_data)
  return response

def get_host_details(config, params):
  haus = urlhaus(config)
  endpoint = '/v1/host/'
  host = params.get('host')
  json_data = {
        'host' : host,
      }
  response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
  #requests.post(url ='https://urlhaus-api.abuse.ch/v1/url/' , data=json_data)
  return response

def get_hash_details(config, params):
  haus = urlhaus(config)
  endpoint = '/v1/payload/'
  file_hash = params.get('hash')
  if re.search(r"^[A-Za-z0-9]{32}$", file_hash):
    hash_algo = 'md5_hash'
    json_data = {
      'md5_hash' : file_hash,
    }
    response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
    return response
  elif re.search(r"^[A-Za-z0-9]{64}$", file_hash):
    hash_algo = 'sha256_hash'
    #if len(file_hash) == 32:
    json_data = {
      'sha256_hash' : file_hash,
    }
    response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
    return response
  else:
    return "Invalid file hash type provided please make sure its MD5 or SHA256"


def _check_health(config):
    try:
        params = {}
        res = login(config, params)
        if res:
            logger.info('connector available')
            return True
    except Exception as e:
        logger.exception('{}'.format(e))
        raise ConnectorError('{}'.format(e))

def get_recent_URLs(config, params):
  haus = urlhaus(config)
  limit = params.get('limit')
  endpoint = '/v1/urls/recent/limit/' + str(limit)
  response = haus.make_request(endpoint=endpoint, method='GET')
  return response

def get_UrlDetails_id(config, params):
  haus = urlhaus(config)
  urlid = params.get('urlid')
  endpoint = '/v1/urlid/' 
  json_data = {
      'urlid' : urlid,
    }
  response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
  return response

def get_tag(config, params):
  haus = urlhaus(config)
  tag = params.get('tag')
  endpoint = '/v1/tag/' 
  json_data = {
      'tag' : tag,
    }
  response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
  return response

def get_signature(config, params):
  haus = urlhaus(config)
  signature = params.get('signature')
  endpoint = '/v1/signature/' 
  json_data = {
      'signature' : signature,
    }
  response = haus.make_request(endpoint=endpoint, method='post', data=json_data)
  return response


def get_recent_Payload(config, params):
  haus = urlhaus(config)
  limit = params.get('limit')
  endpoint = '/v1/payloads/recent/limit/' + str(limit)
  response = haus.make_request(endpoint=endpoint, method='GET')
  return response

operations = {
  	'login': login,
  	'get_url_details': get_url_details,
  	'get_hash_details': get_hash_details,
  	'get_host_details' : get_host_details,
  	'get_recent_URLs' : get_recent_URLs,
  	'get_recent_Payload' : get_recent_Payload,
  	'get_UrlDetails_id' : get_UrlDetails_id,
  	'get_tag' : get_tag,
  	'get_signature' : get_signature
	}
