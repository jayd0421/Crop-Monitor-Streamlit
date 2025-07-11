import ee
import streamlit as st
import json

def ee_to_st():
    # Load service account from Streamlit secrets
    service_account_info = st.secrets["earthengine"]

    # Convert TOML dict to JSON string
    json_creds = json.dumps(service_account_info)

    # Authenticate and initialize Earth Engine
    credentials = ee.ServiceAccountCredentials(service_account_info["client_email"], key_data=json_creds)
    return ee.Initialize(credentials)
