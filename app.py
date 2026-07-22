import streamlit as st
import pandas as pd
import traceback  # Used to print out exact line failures

# Set up browser layout frame window options
st.set_page_config(
    page_title="SRINIVASTA Apps Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Apps Traffic Control Center")
st.caption("Real-time telemetry and user fingerprints across your 60+ deployed applications.")
st.markdown("---")

# SECURE INGESTION: Fetches your shared sheet CSV download URL hidden in Streamlit secrets
try:
    if "analytics_sheet_csv_url" not in st.secrets:
        raise KeyError("The secret key 'analytics_sheet_csv_url' is missing entirely from your Streamlit Secrets panel.")

    target_sheet_url = st.secrets["analytics_sheet_csv_url"]
    
    # Download the live log stream straight from Google Sheets into a DataFrame
    df = pd.read_csv(target_sheet_url)
    
    # Check if the sheet is completely empty or missing columns
    required_columns = ["Timestamp", "App_Name", "Session_ID", "User_Fingerprint"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Google Sheet is missing these exact columns or has a typo: {missing_cols}. Current columns found: {list(df.columns)}")

    # Convert timestamps cleanly
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # 1. High-Level KPI Summary Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Page Views Across Portfolio", f"{len(df):,}")
    col2.metric("Unique Viewers (Fingerprints) Identified", f"{df['User_Fingerprint'].nunique():,}")
    col3.metric("Active Tracked Apps Online", f"{df['App_Name'].nunique()}/60+")
    
    st.markdown("---")
    
    # 2. Graphical Traffic Split Charts Row (FIXED: Added '2' columns)
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
        st.info("The Google Sheet connected successfully, but it has no traffic rows yet! Visit one of your 60+ apps to log the first visit.")
        
    st.markdown("---")
    
    # 3. Comprehensive Raw Activity Stream (Latest Hits First)
    st.subheader("🕒 Live Global Activity Stream")
    if not df.empty:
        df_sorted = df.sort_values(by="Timestamp", ascending=False)
        df_sorted["Timestamp"] = df_sorted["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        st.dataframe(df_sorted, use_container_width=True, hide_index=True)
    else:
        st.dataframe(pd.DataFrame(columns=required_columns), use_container_width=True, hide_index=True)

except Exception as e:
    # 🔴 DIAGNOSTIC OVERRIDE: Shows you the exact technical issue on screen
    st.error("🔒 Security Access Denied: Missing valid data stream configuration credentials.")
    st.info("Analytics metrics are restricted exclusively to the workspace manager administrator via Streamlit Secrets.")
    
    st.markdown("---")
    st.subheader("🛠️ Technical Debugging Console (Admin View)")
    st.warning(f"**Error Details:** {str(e)}")
    with st.expander("View Full Code Error Traceback"):
        st.code(traceback.format_exc())
