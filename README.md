# Elasticsearch reference project

## Intro
the idea for this project is to collect various tools and techniques for setting up a python project to work with Elasticsearch.
This will hopefully act as a jumping off point for a new project and speed up actually doing the point of the project and not trying to remember how to load environment variables again.

## VSCode setup reminders

1. Fork this repository
2. Clone the Fork in VSCode
    1. Open the command palette with the key combination of Ctrl + Shift + P 
    2. At the command palette prompt, enter gitcl , select the Git: Clone command, then select Clone from GitHub and press Enter
    3. When prompted for the Repository URL, select clone from GitHub, then press Enter
3. Creaate a new python virtual environment
    1. Open the command palette with the key combination of Ctrl + Shift + P 
    2. Search for the **Python: Create Environment** command, and select . Select Venv
    3. Pick the python version you want to use
4. Get your Elastic creds
    1. Go to your cluster in Elastic Cloud and get the CloudID
    2. Go to Kibana and generate a new API Key
    3. Make sure you select json as the format and then pick out the id and key
5. Create your .env file for testing
    1. Copy .env.example to .env
    2. Add your parameters


## Structure

### /tools
This is where reusable functions live in modules.
As projects require functionallity repeadedly, it should be matured in to modules held here.

The current modules are:
* myes - Tools for initialising and working with elasticsearch such as extra helper functions
* eslogger - A hacky way to get logs sent directly to Elasticsearch rather than the offical approach with Elastic agent. This can be useful for simple demos


## Updating the requirements file

If new dependencies get added, update the requirements file using
```python
pip freeze > requirements,txt
```


## Running streamlit in VSCode
The repository chould contain a luanch.json which configures launching streamlit
To run Streamlit, head to the file and in the Run/Debug in the left menu you should be able to select Python:Streamlit


## VSCode Troubleshooting
### Can't find the package I installed with pip
You can get issues where the terminal stops using the correct interpreter and therefore pip install etc stops working. The easiest solution is to replace the venv by going to the command pallet to create a new one and the select relete and recreate.