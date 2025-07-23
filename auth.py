#This is a streamlit page for authentication
import streamlit as st
from msal import ConfidentialClientApplication
import uuid
import requests


#Azure app registrations
def ms_authenticate():
    MS_CLIENT_ID = "e75da912-cfd8-40f5-b4d1-09a4a8ab82b2"
    MS_TENANT_ID = "9e1e17f9-8be4-4ec7-9c7a-4329142ba80f"
    MS_CLIENT_SECRET = "6GK8Q~GoIGdNf1Flg8kUXu2nG2h.~x6HOfLjOaMQ"
    MS_CLIENT_SECRET_ID = "7eb169c8-9f6d-44dd-8baf-624a111391e7"
    SCOPE = ["User.Read"]
    REDIRECT_URI = "http://localhost:8501"

    #Create MSAL app
    app = ConfidentialClientApplication(
        client_id=MS_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{MS_TENANT_ID}",
        client_credential=MS_CLIENT_SECRET
    )

    #Generate the authorization URL
    auth_url = app.get_authorization_request_url(SCOPE, state=str(uuid.uuid4()), redirect_uri="http://localhost:8501")

    st.write("### Login with Microsoft")
    st.markdown(f"[Login]({auth_url})", unsafe_allow_html=False)

    print(st.query_params)

    #Handle the redirect and get the authorization code
    if "code" in st.query_params:
        code = st.query_params["code"][0]
        result = app.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
        
        if "access_token" in result:
            st.session_state.logged_in = True
            st.session_state.access_token = result["access_token"]
            headers = {"Authorization": f"Bearer {result['access_token']}"}
            user_info = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
            st.success(f"Login successful! Welcome, {user_info['displayName']}.")
            st.session_state.user_info = user_info
            st.rerun()
        else:
            st.error("Login failed. Please try again.")
    else:
        st.warning("Please login to continue.")


#This is a simple authentication page
def authenticate(username, password):
    #For simplicity, we are using hardcoded credentials
    if username == "admin" and password == "password":
        return True
    return False

def is_authenticated():
    return st.session_state.get("logged_in", False)

def logout():
    st.session_state.logged_in = False
    st.success("You have been logged out.")
    st.rerun()

#Streamlit app for authentication
st.title("Authentication Page")

if st.button("Login"):
    ms_authenticate()
