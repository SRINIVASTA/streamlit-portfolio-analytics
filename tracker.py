import streamlit as st
import requests
import uuid

def track_all_apps(app_name: str):
    """
    Universal tracker for all 50+ apps.
    Uses the exact same Measurement ID across your entire network.
    """
    try:
        # Centralized Measurement ID - change this ONCE to apply to all 50+ apps
        MASTER_GA_ID = "G-K81T36LYB7"  # Replace with your actual G- ID
        
        if "analytics_user_id" not in st.session_state:
            st.session_state.analytics_user_id = str(uuid.uuid4())
        
        url = "https://google-analytics.com"
        params = {
            "v": "2",
            "tid": MASTER_GA_ID,
            "cid": st.session_state.analytics_user_id,
            "en": "page_view",
            "ep.page_title": app_name,  # Captures which specific app was opened
            "ep.page_location": f"https://streamlit.io{app_name.lower().replace(' ', '-')}"
        }
        
        requests.post(url, params=params, timeout=2)
    except Exception:
        pass
