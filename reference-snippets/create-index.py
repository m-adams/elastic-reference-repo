# This script creates the index in Elasticsearch
# It can delete the index if it already exists

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import os

DELETE_EXISTING = True
INDEX_NAME = 'reference'

mapping_path = '../json/index_mappings.json'
settings_path = '../json/index_settings.json'


# Setup the main index to recieve the data
if es.indices.exists(index=INDEX_NAME) and DELETE_EXISTING:
    es.indices.delete(index=INDEX_NAME)
if not es.indices.exists(index=INDEX_NAME):
    with open(mapping_path, "r") as file:
                mapping = json.load(file)
    with open(settings_path, "r") as file:
                settings = json.load(file)
    es.indices.create(index=INDEX_NAME,mappings=mapping,settings=settings)