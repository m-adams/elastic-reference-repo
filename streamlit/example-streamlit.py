import os
import streamlit as st
import streamlit_authenticator as stauth

import sys
sys.path.append("../") # go to parent dir this help imports work as expected
# Import myes which is some tools to get up and running faster
from tools import myes
import importlib
importlib.reload(myes) # reload module to get latest changes

# Required Environment Variables

# cloud_id - Elastic Cloud Deployment ID

extra_env_vars=[]
# We can load the variables like this
#extra_env_vars = [ 'INDEX_NAME', 'APP_NAME', 'IMAGE_URL', 'DEMO_USER', 'DEMO_PASS'  ]

es=myes.init(extra_env_vars)

if(hasattr(myes,"DEMO_USER")): 
    demo_username = myes.DEMO_USER
else: 
    demo_username = "demo"
if(hasattr(myes,"DEMO_PASS")):
    demo_password = myes.DEMO_PASS
else:
    demo_password = "demo"
if(hasattr(myes,"APP_NAME")):
    app_name = myes.APP_NAME
else:
    app_name = "My Demo App"
if(hasattr(myes,"IMAGE_URL")):
    image_url = myes.IMAGE_URL
else:
    image_url = "https://www.elastic.co/static-res/images/elastic-logo-200.png"





# Setup basic authentication to the app
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


def app_main():
    st.title(app_name)
    st.image(image_url)
    # Main chat form
    with st.form("example_form"):
        global check
        check = False
        check = st.checkbox(label='Example checkbox',value= check)
        query = st.text_input("You: ")
        submit_button = st.form_submit_button("Send")

    if submit_button:
        st.write(es.info().body)
        


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    app_main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')



