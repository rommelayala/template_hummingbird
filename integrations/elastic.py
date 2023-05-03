import sys

from elasticsearch import Elasticsearch

sys.path.append("..")
from lib.config_variables import ConfigVariables


def log_json_to_foundatoin_elastic(data_configured):
    variables = ConfigVariables()

    es = Elasticsearch([variables.elasticsearch_url])
    index_name = variables.index_name

    # Send data to elastic
    response = es.index(index=index_name, body=data_configured)
    # Print response in console
    print(response)


def __init__(self):
    self.data = []


#log_json_to_foundatoin_elastic()
