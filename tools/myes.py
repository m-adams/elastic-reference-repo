
# impart modules to connect to elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import os
from dotenv import load_dotenv


def init( additional_env_vars={},dotenv_path='../.env' ):
    """ This function loads environment variables and connects to Elasticsearch

    Description:
        It is asssumed there are base variables required which are 'CLOUD_ID', 'ELASTICSEARCH_API_KEY', 'ELASTICSEARCH_API_KEY_ID',
        If you require additional variables specify them in the additional_env_vars dictionary along with any default values
        If a .env file is found, it will overwite an existing environment variable with the value in the .env file
        If the variable is not specififed in the .env or the file doesn't exist it will check if it's set and if not, use the default value
        If you want to error out if a variable isn't present, set the default value to None.
        It will also write out an example file with all the variables, but no values to help people get started
    Args:
        additional_env_vars (dict): A dictionary of additional environment variables to load and their default values
        dotenv_path (str): The path to the .env file

    Returns:
        Elasticsearch: An Elasticsearch connection object
        dict: A dictionary of configuration variables
    .
    """

    # We will store everything in a config dictionary
    config={}

    base_env_variables = {'CLOUD_ID': None, 'ELASTICSEARCH_API_KEY':None, 'ELASTICSEARCH_API_KEY_ID':None} 


    # Combine the base_env_variables with any additional_env_vars passed in to the init function
    required_env_vars = {**base_env_variables, **additional_env_vars}   

    # Load environment variables from .env file if it exists
    if os.path.exists( dotenv_path):
        print('Loading environment variables from .env file')
        load_dotenv(override=True,dotenv_path=dotenv_path)
    else:
        print('No .env file found at ' + dotenv_path)
        print('Current dir = ', os.getcwd())

    # Load each required variable from the required_env_vars list in to  a local variable
    for env_var in required_env_vars.keys():
        config[env_var] = os.getenv(env_var)
        if config[env_var] is None:
            config[env_var] = required_env_vars[env_var]
            print(f'No value found for {env_var} in .env file or environment, using default value of {config[env_var]}')
        #ASSERT that the variable is not None
        assert config[env_var], f'{env_var} environment variable not set'


    # Write an example.env file, overwriting if it exists
    # This file gives somebody starting of an example ,env file to use
    with open( dotenv_path+".example", 'w') as f:
        for env_var in required_env_vars:
            f.write(f'{env_var}=\n')

    # Connect to Elasticsearch and check the connection is working
    es = Elasticsearch(cloud_id=config['CLOUD_ID'], 
        api_key=(config['ELASTICSEARCH_API_KEY_ID'], config['ELASTICSEARCH_API_KEY'])
    )

    #print out if the connection was sucessful or not
    if es.ping():
        print('Connected to Elasticsearch')
    else:
        print('Connection to Elasticsearch failed')
        return None, config
    
    
    return es, config

# Bulk indexing function
def index_documents(elasticsearch_connection: Elasticsearch ,\
                    documents: list,\
                    index_name: str,\
                    batch_size: int = 1000):
    """ This function indexes a list of documents in to Elasticsearch

    Description:
        This function uses the builk API to index documents in batches of 1000
        It will print out the progress of the indexing
    Args:
        elasticsearch_connection (Elasticsearch): An Elasticsearch connection object
        documents (list): A list of documents (dict) to index. If they have an '_id' filed it will be used as the document id
        index_name (str): The name of the index to index the documents in to
        batch_size (int): The number of documents to index in each batch

    Returns:
        int: The number of documents indexed
    .
    """

    actions = []
    batch = []
    total_indexed = 0
    for i in range(0, len(documents), batch_size):
        start=i
        end=min(i+batch_size,len(documents))
        print(f'Batching docs: {start} to {end} of {len(documents)}')
        batch = documents[start:end]
        actions = []
        for doc in batch:
            action = {
                "_index": index_name,
                "_source": doc
            }
            if doc.has_key("_id"):
                id=doc.pop("_id")
                action["_id"]=id
            actions.append(action)
    
        success, _ = helpers.bulk(elasticsearch_connection, actions=actions,raise_on_error=False)
        print(f'Indexed {success} documents')
        total_indexed += success
    return total_indexed

#def getSearchTemplates(es):
    # Get the list of search templates
    #search_templates = es.
    #print(search_templates)
    #return search_templates

#print(getSearchTemplates(es))


