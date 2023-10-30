from dotenv import load_dotenv
import os

def load_config_from_env(env_filepath="./.env",overwrite=False,config_vars={}):
    """
    Load local enviroment variables from .env file if it exists and return the values to use in a config dictionary

    Description:
        This function will load environment variables from a .env file if it exists and return the values to use in a config dictionary.
        It will create an .env.example file with the required variables to keep an up to date example of what is required.
        If the environment variable is already set it will not be overwritten unless overwrite=True is passed in.
        The order of precedence is: environment variable, .env file, default value unless overwrite=True is passed in.
        If the script can't determine the value of a variable it will error out so set a defult value or use None if you want to mandate the value must exist in the environment variables or file.

    Args:
        env_filepath (str): The path to the .env file
        overwrite (bool): Whether to overwrite existing environment variables with values from the .env file
        config_vars (dict): A dictionary of additional environment variables to load and their default values

    Returns:
        dict: A dictionary of configuration variables
    .
    """
    # We will store everything in a config dictionary
    config={}

    # Load environment variables from .env file if it exists
    if os.path.exists( env_filepath):
        print('Loading environment variables from .env file')
        result=load_dotenv(override=overwrite,dotenv_path=env_filepath)
    else:
        print('No .env file found at ' + env_filepath)
        print('Current dir = ', os.getcwd())

    # Load each required variable from the required_env_vars list in to  a local variable
    for env_var in config_vars.keys():
        config[env_var] = os.getenv(env_var)
        if config[env_var] is None:
            os.environ[env_var] = config_vars[env_var] # Make sure it is now an env variable for modules that look directly for env vars
            config[env_var] = config_vars[env_var]
            print(f'No value found for {env_var} in .env file or environment, using default value of {config[env_var]}')
        #ASSERT that the variable is not None
        assert config[env_var], f'{env_var} environment variable not set'


    # Write an example.env file, overwriting if it exists
    # This file gives somebody starting of an example ,env file to use
    with open( env_filepath+".example", 'w') as f:
        for env_var in config_vars:
            f.write(f'{env_var}=\n')

    return config

def  set_env_vars_from_dict(vars: dict):
    """
    Set environment variables from a dictionary

    Description:
        This function will set environment variables from a dictionary
        It will not overwrite existing environment variables. This is useful for forcing new values

    Args:
        vars (dict): A dictionary of environment variables to set

    Returns:
        None
    .
    """
    for key, value in vars.items():
        key=key.upper() # Make sure it's uppercase
        os.environ[key] = value