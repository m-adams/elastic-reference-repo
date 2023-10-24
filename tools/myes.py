
# impart modules to connect to elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import os
from dotenv import load_dotenv


def init( additional_env_vars=[],dotenv_path='../.env' ):
    ### This function will load the environment variables from a local .env file
    ### This function will also check that the required environment variables are set
    ### This function will also write an example.env file if one does not exist
    ### This function will also connect to elasticsearch and check that the connection is working
    ### This function will return the elasticsearch connection object

    # Load environment variables from a local .env file
    # This is a convenience for local development

    # List all the required environment variables here
    # I like this approach because it's easy to add new variables while also updating the checks for those variables and the example files
    base_env_variables = [ 'CLOUD_ID', 'ELASTICSEARCH_API_KEY', 'ELASTICSEARCH_API_KEY_ID' ]

    # Combine the base_env_variables with any additional_env_vars passed in to the init function
    required_env_vars = base_env_variables + additional_env_vars

    # Load environment variables from .env file if it exists
    if os.path.exists( dotenv_path):
        print('Loading environment variables from .env file')
        load_dotenv(override=True,dotenv_path=dotenv_path)
    else:
        print('No .env file found at ' + dotenv_path)
        print('Current dir = ', os.getcwd())

    # Load each required variable from the required_env_vars list in to  a local variable
    for env_var in required_env_vars:
        globals()[env_var] = os.getenv(env_var)
        #ASSERT that the environment variable has been set
        assert globals()[env_var], f'{env_var} environment variable not set'


    # Write an example.env file, overwriting if it exists
    # This file gives somebody starting of an example ,env file to use
    with open( dotenv_path+".example", 'w') as f:
        for env_var in required_env_vars:
            f.write(f'{env_var}=\n')

    # Connect to Elasticsearch and check the connection is working
    es = Elasticsearch(cloud_id=CLOUD_ID, # type: ignore
        api_key=(ELASTICSEARCH_API_KEY_ID, ELASTICSEARCH_API_KEY) # type: ignore
    )

    #print out if the connection was sucessful or not
    if es.ping():
        print('Connected to Elasticsearch')
        return es
    else:
        print('Connection to Elasticsearch failed')
        return None



#def getSearchTemplates(es):
    # Get the list of search templates
    #search_templates = es.
    #print(search_templates)
    #return search_templates

#print(getSearchTemplates(es))


