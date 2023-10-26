
# General imports
import sys
import importlib # Used to reload modules
import streamlit as st
import streamlit_authenticator as stauth

# Elastic imports
import elasticapm
import ecs_logging
import logging

# My local imports
sys.path.append("../") # go to parent dir this help imports work as expected
# Import myes which is some tools to get up and running faster
from tools import myes
from tools import eslogger
importlib.reload(myes) # reload module to get latest changes
importlib.reload(eslogger)

global app_name
@st.cache_resource
def __init__():
    """ This function is used to initialise the app and set some variables

    Description:
        Streamlit can end up runnning things multiple time so we can use a special function experimental_singleton
        https://docs.streamlit.io/library/api-reference/performance/st.experimental_singleton
    
    Returns:
        string: A string of data to display
    """

    # Required settings and default in a dictionary
    param_defaults = {
        'INDEX_NAME': 'reference',
        'DATA_DIR': '../json/data',
        'APP_NAME': 'My Demo App',
        'IMAGE_URL': 'https://www.elastic.co/static-res/images/elastic-logo-200.png',
        'DEMO_USER': 'demo',
        'DEMO_PASS': 'demo',
        'ELASTIC_APM_SERVICE_NAME':"my-demo-app",
        'ELASTIC_APM_ENVIRONMENT' : "development",
        'ELASTIC_APM_SECRET_TOKEN': None,
        'LOGS_INDEX_NAME': 'logs-demo-dev',
        'EVENT_DATASET_LOGS': 'demo'
    }
    # Load environment variables from .env file if it exists and initialise the elasticsearch connection
    es,config=myes.init(param_defaults,dotenv_path='./.env')

    # Init the APM client
    apmclient = elasticapm.Client()
    elasticapm.instrument()

    # Setup logging to the same Elastic cluster
    handler = eslogger.ElasticHandler(logging.INFO,es,config['LOGS_INDEX_NAME'])
    handler.setFormatter(ecs_logging.StdlibFormatter())
    global logger 
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addFilter(eslogger.SystemLogFilter(config['EVENT_DATASET_LOGS']))

    # Set some variables that are a bit nicer to read from our config dictionary
    global app_name, image_url, index_name
    app_name = config['APP_NAME']
    image_url = config['IMAGE_URL']
    index_name = config['INDEX_NAME']
    return es,config,logger


@elasticapm.capture_span("get_data")
def get_data(query: str):
    """ Holding function of what to do when the button is clicked. Add useful code here
    
    Args:
        query (string): The query string entered by the user
    Returns:
        string: A string of data to display
    """
    
    elasticapm.label(es_query=query)
    audit_message = 'This is just a test logging message from my streamlit app'
    audit_context = {'user.full_name': name,
                     'event.dataset': config['EVENT_DATASET_LOGS']}
    logger.info(audit_message,extra=audit_context)

    return es.info().body

def app_main():
    st.title(config['APP_NAME'])
    st.image(config['IMAGE_URL'], width=200)
    # Main chat form
    with st.form("example_form"):
        global check
        check = False
        check = st.checkbox(label='Example checkbox',value= check)
        query = st.text_input("You: ")
        submit_button = st.form_submit_button("Send")

    if submit_button:
        st.write(get_data(query))
        

es,config,logger=__init__()

 # Set some variables that are a bit nicer to read from our config dictionary
demo_username = config['DEMO_USER']
demo_password = config['DEMO_PASS']
# Setup basic authentication to the streamlit app
hashed_pass=stauth.Hasher([demo_password]).generate()[0]
creds={}
creds['usernames']={}
creds['usernames'][demo_username] = {'password': hashed_pass, 'name': demo_username}
authenticator = stauth.Authenticate(
    creds,
    "examplecookiename-demo",
    "thisisacookie",
    30,
    '')
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    app_main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')



