import remote_logger  # 🚀 Runs the tracking payload automatically on load
import streamlit as st
import pandas as pd
import datetime
import hashlib
import json
import urllib.request

# 🌐 NATIVE BACKGROUND WEB LOGGER (No pip install required)
def run_native_tracker(app_identity):
    current_host = st.context.headers.get("host", "").lower()
    if "streamlit" not in current_host and "localhost" not in current_host:
        return 

    if "analytics_logged" not in st.session_state:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_agent = st.context.headers.get("user-agent", "Unknown")
            user_ip = st.context.ip_address or "Local"
            
            user_fingerprint = hashlib.sha256(f"{user_agent}-{user_ip}".encode()).hexdigest()[:16]
            ctx = st.runtime.scriptrunner.script_run_context.get_script_run_ctx()
            session_id = ctx.session_id if ctx else "No_Session"

            payload = {
                "Timestamp": now,
                "App_Name": app_identity,
                "Session_ID": session_id,
                "User_Fingerprint": user_fingerprint
            }

            req = urllib.request.Request(
                st.secrets["google_analytics_url"], 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                pass
            st.session_state.analytics_logged = True
        except Exception:
            pass

# 🚀 Execute the tracker instantly on Line 41 using its own name
run_native_tracker("streamlit-portfolio-analytics")


# 📊 Renders charts & filters analytics data grids
st.set_page_config(
    page_title="SRINIVASTA Apps Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Apps Traffic Control Center")
st.caption("Real-time telemetry and user fingerprints across your 60+ deployed applications.")
st.markdown("---")

try:
    if "analytics_sheet_csv_url" not in st.secrets:
        st.error("🔒 Security Access Denied: Missing valid data stream configuration credentials.")
        st.stop()

    target_sheet_url = st.secrets["analytics_sheet_csv_url"]
    df = pd.read_csv(target_sheet_url)
    
    required_columns = ["Timestamp", "App_Name", "Session_ID", "User_Fingerprint"]
    if not all(col in df.columns for col in required_columns):
        st.error("📊 Spreadsheet Layout Mismatch: Please verify your Google Sheet column headers match exactly.")
        st.stop()

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Page Views Across Portfolio", f"{len(df):,}")
    col2.metric("Unique Viewers (Fingerprints) Identified", f"{df['User_Fingerprint'].nunique():,}")
    col3.metric("Active Tracked Apps Online", f"{df['App_Name'].nunique()}/60+")
    
    st.markdown("---")
    
    left_col, right_col = st.columns(2)
    if not df.empty:
        with left_col:
            st.subheader("📈 Traffic Load Distribution by Repository")
            app_counts = df["App_Name"].value_counts()
            st.bar_chart(app_counts)
            
        with right_col:
            st.subheader("🏆 Most Visited Applications")
            st.dataframe(
                app_counts.rename_axis("App Name").reset_index(name="Total Hits"),
                width="stretch",
                hide_index=True
            )
    else:
        st.info("The Google Sheet connected successfully, but it has no traffic rows yet!")
        
    st.markdown("---")
    
    st.subheader("🕒 Live Global Activity Stream")
    if not df.empty:
        df_sorted = df.sort_values(by="Timestamp", ascending=False)
        df_sorted["Timestamp"] = df_sorted["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        st.dataframe(df_sorted, width="stretch", hide_index=True)
    else:
        st.dataframe(pd.DataFrame(columns=required_columns), width="stretch", hide_index=True)

except Exception:
    st.error("🔒 Security Access Denied: Missing valid data stream configuration credentials.")
