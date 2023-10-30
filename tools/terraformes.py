from python_terraform import *
from elasticsearch import Elasticsearch


# My local imports
from importlib import reload 
import os
from tools import configes
from tools import myes
reload(myes)

def create_or_return_terraform_cluster(terraform_dir: str,parameters={'EC_API_KET':None},env_filepath="./.env"):
    """
    Create or return a Cluster in Elastic Cloud using Terraform

    Description:
        This function will create a cluster in Elastic Cloud using Terraform if it doesn't already exist.
        If it does exist it will return the cluster details and a connection objct as well as setting the cluster details as env variables
    
    Args:
        terraform_dir (str): The path to the Terraform directory
        parameters (dict): A dictionary of additional environment variables to load and their default values
        env_filepath (str): The path to the .env file  

    Returns:
        dict: A dictionary of cluster details
        Elasticsearch: An Elasticsearch connection object
    .
    """

    # Need to make sure the API key is loaded
    if 'EC_API_KEY' not in parameters:
        parameters['EC_API_KEY']=None    # Load local enviroment variables from .env file if it exists
    variables = configes.load_config_from_env(env_filepath,parameters)

    # Initialize Terraform and manage state
    tf=Terraform(working_dir=terraform_dir,variables=variables)
    # Show the current state
    tf.init()
    return_code, stdout, stderr =tf.apply(skip_plan=True, capture_output=False,variables=variables)

    absolute_terraform_dir = os.path.abspath(terraform_dir) 
    cluster_details = {'terraform_dir': absolute_terraform_dir}
    resources=tf.tfstate.resources
    for resource in resources:
        if resource['type'] == 'ec_deployment':
            instances=resource['instances']
            instance=instances[0]
            attributes=instance['attributes']
            cluster_details['cluster_name']=attributes['name']
            cluster_details['cluster_alias']=attributes['alias']
            cluster_details['cloud_region']=attributes['region']
            cluster_details['elastic_apm_secret_token']=attributes['apm_secret_token']
            cluster_details['deployment_template_id']=attributes['deployment_template_id']
            cluster_details['elasticsearch_password']=attributes['elasticsearch_password']
            cluster_details['elasticsearch_username']=attributes['elasticsearch_username']
            cluster_details['cluster_id']=attributes['id']
            cluster_details['kibana_url']=attributes['kibana']['https_endpoint']
            cluster_details['elasticsearch_url']=attributes['elasticsearch']['https_endpoint']
            cluster_details['elastic_apm_server_url']=attributes['integrations_server']['endpoints']['apm']
            cluster_details['cloud_id']=attributes['elasticsearch']['cloud_id']
    configes.set_env_vars_from_dict(cluster_details)

    es, config = myes.init()

    return cluster_details, es


def safe_destroy_terraform_cluster(terraform_dir:str,env_filepath="./.env"):
    """
    Destroy a cluster in Elastic Cloud using Terraform

    Description:
        This function will destroy a cluster in Elastic Cloud using Terraform
        It will check if the cluster exists first and if it does it will destroy it
        If it doesn't exist it will do nothing

    Args:
        terraform_dir (str): The path to the Terraform directory

    Returns:
        bool: Whether the cluster was destroyed or not
    .
    """
    input("Are you sure you want to destroy the cluster? Press Enter to continue...")
    parameters={'EC_API_KEY':None}    # Load local enviroment variables from .env file if it exists
    variables = configes.load_config_from_env(env_filepath,parameters)

    # Initialize Terraform and manage state
    tf=Terraform(working_dir=terraform_dir)
    # Show the current state
    tf.init()
    return_code=0
    #return_code, stdout, stderr =tf.destroy(skip_plan=True, capture_output=False,variables=variables)

    if return_code == 0:
        return True
    else:
        return False

def safe_destroy_terrafrom_clsuter(cluster_details: dict):
    """
    Destroy a cluster in Elastic Cloud using Terraform

    Description:
        This function will destroy a cluster in Elastic Cloud using Terraform
        It will check if the cluster exists first and if it does it will destroy it
        If it doesn't exist it will do nothing

    Args:
        cluster_details (dict): A dictionary of cluster details

    Returns:
        bool: Whether the cluster was destroyed or not
    .
    """

    name=input(f"Enter the name of the cluster '{cluster_details['cluster_name']}' to destroy: ")

    if name.strip() == cluster_details['cluster_name']:
        return safe_destroy_terraform_cluster(cluster_details['terraform_dir'])


