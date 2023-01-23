import requests, io, json
import pandas as pd
from .utils import invoke_rest_endpoint
from connectors.core.connector import get_logger, ConnectorError
from .constants import LOGGER_NAME
import re, json
from io import StringIO

logger = get_logger(LOGGER_NAME)

def get_feed(config=None, *args, **kwargs):
    textdf = invoke_rest_endpoint(config, 'downloads/csv_online/', 'GET').content.decode('utf8')
    df = textdf[textdf.find('id,dateadded,url,url_status,threat,tags,urlhaus_link,reporter'):]
    api_response = pd.DataFrame(pd.read_csv(io.StringIO(df), lineterminator='\n', header=0, index_col=None)).to_json(orient='records')
    if api_response != '':
        iodata = StringIO(api_response)
        return json.load(iodata)
    else:
        return None