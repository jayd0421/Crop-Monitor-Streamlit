import ee
import streamlit as st
import json

def ee_to_st():
    """Authenticate Earth Engine using service account on Streamlit Cloud or default on local dev."""
    try:
        ee.Initialize()
    except Exception:
        service_account_info = st.secrets["earthengine"]
        json_creds = json.dumps(service_account_info)
        credentials = ee.ServiceAccountCredentials(service_account_info["client_email"], key_data=json_creds)
        ee.Initialize(credentials)
