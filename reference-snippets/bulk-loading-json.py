# This script loops over json files in a directory and uses bulk to index tem in to elasticsearch


import os
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

INDEX_NAME = 'reference'
DATA_DIR = '../json/data'
# Create es which is an elasticsearch connection object



# Bulk indexing function
def index_documents(documents):
    actions = []
    for doc in documents:
        id=doc.pop("_id")
        action = {
            "_index": INDEX_NAME,
            "_id": id,
            "_source": doc
        }
        
        actions.append(action)
    
    success, _ = bulk(es, actions=actions,raise_on_error=False)
    return success

# List to store documents
documents = []

# Loop through JSON files in the directory
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(DATA_DIR, filename)

        # Read JSON file
        with open(file_path, "r") as file:
            data = json.load(file)
        for doc in data:
            documents.append(doc)
        success_count = index_documents(documents)
        print(f"Indexed {success_count} documents")
            
        # Clear the document list after indexing
        documents = []

# Index any remaining documents
if len(documents) > 0:
    success_count = index_documents(documents)
    print(f"Indexed {success_count} documents")