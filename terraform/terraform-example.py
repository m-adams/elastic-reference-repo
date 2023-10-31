
import sys
import os
import pprint

# My local imports
print(os.getcwd())
sys.path.append(os.getcwd()) # add current working directory to path
print(sys.path)

from importlib import reload
from tools import terraformes

reload(terraformes); # reload module in case of changes

# Use terraform to create a cluster if it doesn't exist or just to return the details if it does
cluster_details, es = terraformes.create_or_return_terraform_cluster(terraform_dir="terraform/elastic-cloud/",env_filepath="terraform/.env")

print(es.info()) # print cluster info

# %%
pprint.pprint(cluster_details)

# %% [markdown]
# ## When you are finished you can destroy your cluster
# 
# I created a helper function which could add to sanity check so you don't accidentally delete a cluster if you click run all by acident
# 
# 

# %%
terraformes.safe_destroy_terrafrom_clsuter(cluster_details) 

# %% [markdown]
# 


