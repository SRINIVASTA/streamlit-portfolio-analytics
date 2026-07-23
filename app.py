import streamlit as st
import pandas as pd
import datetime
import hashlib
import json
import urllib.request
import urllib.error

# 🌐 NATIVE BACKGROUND TELEMETRY LOGGER
def run_portfolio_tracker(app_identity):
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

            # Direct fallback link pasted straight into the network request dispatcher
            req = urllib.request.Request(
                st.secrets["google_analytics_url"], 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            # FIXED: Removed the problematic 'if e.code not in' block entirely
            try:
                with urllib.request.urlopen(req, timeout=4) as response:
                    response.read()
            except urllib.error.HTTPError:
                pass  # Safely catch and ignore Google's 302 redirection codes
                    
            st.session_state.analytics_logged = True
        except Exception:
            pass

# 🚀 Execute background tracking on page layout boot
run_portfolio_tracker("streamlit-portfolio-analytics")


# 📊 DASHBOARD INTERACTION ENGINE RENDER
st.set_page_config(
    page_title="SRINIVASTA Apps Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Apps Traffic Control Center")
st.caption("Real-time telemetry and user fingerprints across your 60+ deployed applications.")
st.markdown("---")

# 🔐 HARDCODED LINK DIRECTIVES (Bypasses Streamlit Cloud Secrets bugs)
target_sheet_url = st.secrets["analytics_sheet_csv_url"]

# 📥 STEP 2: Fetch and Ingest CSV Data Safely
try:
    df = pd.read_csv(target_sheet_url)
except Exception as e:
    st.error("🌐 Network Connection Error: Unable to fetch data from the live stream link.")
    st.warning("Please verify your Google Sheets sharing settings match 'Published to the web' and it is set to CSV output.")
    st.stop()

# 📐 STEP 3: Validate Sheet Header Layout Matrix
required_columns = ["Timestamp", "App_Name", "Session_ID", "User_Fingerprint"]

# Handle cases where the spreadsheet is entirely uninitialized or has blank columns
if df.empty or len(df.columns) <= 1:
    df = pd.DataFrame(columns=required_columns)

if not all(col in df.columns for col in required_columns):
    st.error("📊 Spreadsheet Layout Mismatch: Please verify your Google Sheet column headers match exactly.")
    st.caption(f"Required Headers: `{', '.join(required_columns)}`")
    st.stop()

# Clean data parsing if information exists
if not df.empty:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df = df.dropna(subset=["Timestamp"])

# 💹 STEP 4: High-Level KPI Summary Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Page Views Across Portfolio", f"{len(df):,}")
col2.metric("Unique Viewers (Fingerprints) Identified", f"{df['User_Fingerprint'].nunique() if not df.empty else 0:,}")
col3.metric("Active Tracked Apps Online", f"{df['App_Name'].nunique() if not df.empty else 0}/60+")

st.markdown("---")

# 📉 STEP 5: Graphical Data Visualizations
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
            use_container_width=True,
            hide_index=True
        )
else:
    with left_col:
        st.info("The Google Sheet connected successfully, but it has no traffic rows yet! Visit one of your 60+ apps to log the first visit.")
    with right_col:
        st.caption("Awaiting data streams from external application web containers...")
    
st.markdown("---")

# 🕒 STEP 6: Live Global Activity Stream
st.subheader("🕒 Live Global Activity Stream")
if not df.empty:
    df_sorted = df.sort_values(by="Timestamp", ascending=False)
    df_sorted["Timestamp"] = df_sorted["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(df_sorted, use_container_width=True, hide_index=True)
else:
    st.dataframe(pd.DataFrame(columns=required_columns), use_container_width=True, hide_index=True)
