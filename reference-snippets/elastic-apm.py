# How to add simple APM traces and direct logs

import sys
sys.path.append("./") # go to parent dir this help imports work as expected
# Import myes which is some tools to get up and running faster
from tools import myes
import importlib
import os
import elasticapm
importlib.reload(myes) # reload module to get latest changes

# Docs
# https://www.elastic.co/guide/en/apm/agent/python/current/instrumenting-custom-code.html

os.environ['ELASTIC_APM_SERVICE_NAME'] = "my-demo-app"
os.environ['ELASTIC_APM_ENVIRONMENT'] = "development"
env_path = './.env'
extra_env_vars = [ 'ELASTIC_APM_SERVICE_NAME', 'ELASTIC_APM_SECRET_TOKEN' ]

# Load environment variables from .env file if it exists and initialise the elasticsearch connection
es=myes.init(additional_env_vars=extra_env_vars,dotenv_path=env_path)

apmclient = elasticapm.Client()
elasticapm.instrument()

@elasticapm.capture_span("my_span")
def my_span():
    print("my_span")
    elasticapm.label(es_query="test")
    

my_span()
