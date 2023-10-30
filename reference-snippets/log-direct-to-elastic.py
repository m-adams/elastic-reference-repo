# Definitly not our prefered option but it's very useful for quick demos

import sys
sys.path.append("./") # go to parent dir this help imports work as expected
# Import myes which is some tools to get up and running faster
from tools import myes
from tools import loggeres
import importlib
import os

importlib.reload(myes) # reload module to get latest changes, useful for dev
importlib.reload(loggeres)


import ecs_logging
import logging

env_path = './.env'
extra_env_vars = {'LOGS_INDEX_NAME': 'logs-demo-dev','EVENT_DATASET_LOGS': 'demo'}

# Load environment variables from .env file if it exists and initialise the elasticsearch connection
es,config=myes.init(additional_env_vars=extra_env_vars,dotenv_path=env_path)

handler = loggeres.ElasticHandler(logging.INFO,es,config['LOGS_INDEX_NAME'])
handler.setFormatter(ecs_logging.StdlibFormatter())
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addFilter(loggeres.SystemLogFilter(config['EVENT_DATASET_LOGS']))

audit_message = 'This is just a test'
audit_context = {'event.dataset': config['EVENT_DATASET_LOGS']}
logger.info(audit_message,extra=audit_context)
