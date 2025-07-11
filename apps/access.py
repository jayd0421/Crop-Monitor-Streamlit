import geemap
import ee
import streamlit as st
import json

def ee_to_st():
    """Authenticate Earth Engine using service account on Streamlit Cloud or default on local dev."""
    try:
        geemap.ee_initialize()
    except Exception:
        # Convert TOML object to a plain Python dict
        service_account_info = dict(st.secrets["earthengine"])
        
        # Convert dict to JSON string
        json_creds = json.dumps(service_account_info)
        
        # Authenticate with service account
        credentials = ee.ServiceAccountCredentials(service_account_info["client_email"], key_data=json_creds)
        ee.Initialize(credentials)
        st.success("Earth Engine initialized using service account.")