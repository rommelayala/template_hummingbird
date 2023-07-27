import sys
import logging

from elasticsearch7 import Elasticsearch

sys.path.append("..")
from lib.config_variables import ConfigVariables


def log_json_to_foundation_elastic(data_configured):
    variables = ConfigVariables()

    es = Elasticsearch([variables.elasticsearch_url])
    index_name = variables.index_name
    # Send data to elastic
    # todo: comment/uncomment to work
    response = es.index(index=index_name, body=data_configured)
    logging.debug(response)

def __init__(self):
    self.data = []
