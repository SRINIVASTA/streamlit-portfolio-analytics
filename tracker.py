import streamlit as st
import requests
import uuid
import json

def track_all_apps(app_name: str):
    """Universal tracker pulling secrets securely from Streamlit Cloud memory."""
    try:
        # 1. READ SECRETS DYNAMICALLY FROM STREAMLIT ENVIRONMENT
        # This completely hides your API key from public GitHub eyes
        MASTER_GA_ID = st.secrets["GA_MEASUREMENT_ID"]
        API_SECRET = st.secrets["GA_API_SECRET"]
        
        if "analytics_user_id" not in st.session_state:
            st.session_state.analytics_user_id = str(uuid.uuid4())
        
        url = f"https://google-analytics.com{MASTER_GA_ID}&api_secret={API_SECRET}"
        
        payload = {
            "client_id": st.session_state.analytics_user_id,
            "events": [{
                "name": "page_view",
                "params": {
                    "page_title": app_name,
                    "page_location": f"https://streamlit.io{app_name.lower().replace(' ', '-')}",
                    "engagement_time_msec": "1000",
                    "session_id": st.session_state.analytics_user_id
                }
            }]
        }
        
        requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=3)
    except Exception:
        pass
