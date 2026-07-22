# app.py (Renders charts & filters analytics data grids)
import streamlit as st
import pandas as pd

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
    target_sheet_url = st.secrets["analytics_sheet_csv_url"]
    
    # Download the live log stream straight from Google Sheets into a DataFrame
    df = pd.read_csv(target_sheet_url)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # 1. High-Level KPI Summary Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Page Views Across Portfolio", f"{len(df):,}")
    col2.metric("Unique Viewers (Fingerprints) Identified", f"{df['User_Fingerprint'].nunique():,}")
    col3.metric("Active Tracked Apps Online", f"{df['App_Name'].nunique()}/60+")
    
    st.markdown("---")
    
    # 2. Graphical Traffic Split Charts Row
    left_col, right_col = st.columns()
    
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
        
    st.markdown("---")
    
    # 3. Comprehensive Raw Activity Stream (Latest Hits First)
    st.subheader("🕒 Live Global Activity Stream")
    df_sorted = df.sort_values(by="Timestamp", ascending=False)
    df_sorted["Timestamp"] = df_sorted["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(df_sorted, use_container_width=True, hide_index=True)

except Exception:
    st.error("🔒 Security Access Denied: Missing valid data stream configuration credentials.")
    st.info("Analytics metrics are restricted exclusively to the workspace manager administrator via Streamlit Secrets.")
