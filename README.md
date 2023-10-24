# Elasticsearch reference project

## Intro
the idea for this project is to collect various tools and techniques for setting up a python project to work with Elasticsearch.
This will hopefully act as a jumping off point for a new project and speed up actually doing the point of the project and not trying to remember how to load environment variables again.

## VSCode setup reminders

- Fork this repository
- Clone the Fork in VSCode
1. Open the command palette with the key combination of Ctrl + Shift + P 
2. At the command palette prompt, enter gitcl , select the Git: Clone command, then select Clone from GitHub and press Enter
3. When prompted for the Repository URL, select clone from GitHub, then press Enter

- Creaate a new python virtual environment
1. Open the command palette with the key combination of Ctrl + Shift + P 
2. Search for the **Python: Create Environment** command, and select it
3. Select Venv
4. Pick the python version you want to use

- Get your Elastic creds
1. Go to your cluster in Elastic Cloud and get the CloudID
2. Go to Kibana and generate a new API Key
4. Make sure you select json as the format and then pick out the id and key

- Create your .env file for testing
1. Copy example.env to .env
2. Add your parameters


## Updating the requirements file

If new dependencies get added, update the requirements file using
```python
pip freeze > requirements,txt
```


## Running streamlit in VSCode
The repository chould contain a luanch.json which configures launching streamlit
To run Streamlit, head to the file and in the Run/Debug in the left menu you should be able to select Python:Streamlit