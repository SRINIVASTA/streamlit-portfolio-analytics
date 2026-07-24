import streamlit as st
import requests
import uuid
import json

def track_all_apps(app_name: str):
    """Universal tracker using the secure GA4 Measurement Protocol."""
    try:
        # 1. CREDENTIALS (Updated with your real Measurement ID!)
        MASTER_GA_ID = "G-K81T36LYB7"  
        
        # Make sure to generate and paste your API secret from your GA4 dashboard settings here
        API_SECRET = "YOUR_API_SECRET_HERE" 
        
        # 2. Establish a unique session ID
        if "analytics_user_id" not in st.session_state:
            st.session_state.analytics_user_id = str(uuid.uuid4())
        
        # 3. Secure Production Collection Endpoint
        url = f"https://google-analytics.com{MASTER_GA_ID}&api_secret={API_SECRET}"
        
        # 4. Correctly formatted JSON payload required for Server-Side events
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
        
        # 5. POST the data payload straight to the server
        requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=3)
    except Exception:
        pass
