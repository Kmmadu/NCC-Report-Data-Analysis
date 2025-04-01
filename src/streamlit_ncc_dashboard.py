import streamlit as st
import pandas as pd
import plotly.express as px
from functools import reduce
import os

# -------------------------------------------------------------------
# Load and Preprocess Data
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    Load and preprocess the merged client dataset.
    
    The function builds an absolute path to the merged_clients.csv file located
    in the data folder (at the repo root), verifies its existence, and reads it.
    It standardizes the 'CLIENT' and 'CUSTOMER STATUS' columns for consistent filtering.
    
    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    try:
        # Get current script directory (inside the src folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Build absolute path to the data file (data folder is in the repo root)
        file_path = os.path.join(current_dir, '..', 'data', 'merged_clients.csv')
        
        # Verify that the data file exists
        if not os.path.exists(file_path):
            st.error(f"Data file not found at: {file_path}")
            st.stop()
            
        df = pd.read_csv(file_path)
        
        # Standardize the 'CLIENT' column
        df["CLIENT"] = df["CLIENT"].replace({
            "Corporate and Retail": "Corporate",
            "Retail Clients": "Retail",
            "corporate": "Corporate"
        }).str.strip().str.title()
        
        # Standardize the 'CUSTOMER STATUS' column
        df["CUSTOMER STATUS"] = df["CUSTOMER STATUS"].replace({
            "Active": "Connected",
            "Inactive": "Disconnected",
            "Diconnected": "Disconnected"
        }).str.strip().str.title()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# -------------------------------------------------------------------
# PDF Path Handling
# -------------------------------------------------------------------
def get_pdf_path():
    """
    Build and return the absolute path to the PDF insights report.
    
    Returns:
        str: The absolute file path to the insight.pdf file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', 'data', 'insight.pdf')

# -------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------
df = load_data()

# -------------------------------------------------------------------
# Sidebar Configuration - Filters
# -------------------------------------------------------------------
st.sidebar.header("Data Controls")

# Geographic Filters
with st.sidebar.expander("🌍 Geographic Filters", expanded=True):
    regions = st.multiselect(
        "Select Regions:",
        options=df["REGION"].unique(),
        default=list(df["REGION"].unique()),
        help="Filter data by geographic regions."
    )
    state_options = df[df["REGION"].isin(regions)]["STATE"].unique() if regions else df["STATE"].unique()
    states = st.multiselect(
        "Select States:",
        options=state_options,
        default=list(state_options),
        help="Filter data by states within the selected regions."
    )

# Customer Filters
with st.sidebar.expander("🏢 Customer Filters", expanded=True):
    client_types = st.multiselect(
        "Select Customer Types:",
        options=["Corporate", "Retail"],
        default=["Corporate", "Retail"],
        help="Filter by customer business type."
    )
    statuses = st.multiselect(
        "Select Connection Status:",
        options=["Connected", "Disconnected"],
        default=["Connected", "Disconnected"],
        help="Filter by customer connection status."
    )

# -------------------------------------------------------------------
# Filtering Logic
# -------------------------------------------------------------------
conditions = []
if regions: 
    conditions.append(df["REGION"].isin(regions))
if states: 
    conditions.append(df["STATE"].isin(states))
if client_types: 
    conditions.append(df["CLIENT"].isin(client_types))
if statuses: 
    conditions.append(df["CUSTOMER STATUS"].isin(statuses))

df_filtered = df[reduce(lambda x, y: x & y, conditions)] if conditions else df

if df_filtered.empty:
    st.warning("No data matches current filters. Adjust your selections.")
    st.stop()

# -------------------------------------------------------------------
# Dashboard Layout
# -------------------------------------------------------------------
st.title("NCC 2024 Customer Intelligence Dashboard")
st.caption("Q4 Performance Metrics & Customer Insights")

# Key Metrics Grid
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Bandwidth", 
              f"{df_filtered['BANDWIDTH SUBSCRIPTION (Mbps)'].sum():,.0f} Mbps",
              help="Total bandwidth allocated to selected customers.")
with col2:
    st.metric("Active Connections", 
              f"{df_filtered[df_filtered['CUSTOMER STATUS'] == 'Connected'].shape[0]:,}",
              help="Number of currently connected customers.")
with col3:
    st.metric("Enterprise Clients", 
              f"{df_filtered[df_filtered['CLIENT'] == 'Corporate'].shape[0]:,}",
              help="Number of corporate customers.")

# -------------------------------------------------------------------
# Visualizations
# -------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Geographic Analysis", "Customer Segmentation", "Raw Data"])

# Geographic Analysis Tab
with tab1:
    # Bar chart: Customer Distribution by Region
    fig1 = px.bar(
        df_filtered.groupby("REGION", as_index=False).size(),
        x="REGION", y="size",
        labels={"size": "Customers", "REGION": "Region"},
        title="Customer Distribution by Region"
    )
    fig1.update_layout(height=400, title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Bar chart: Top 10 States by Customer Count
    fig2 = px.bar(
        df_filtered.groupby("STATE", as_index=False).size().nlargest(10, "size"),
        x="size", y="STATE", orientation='h',
        labels={"size": "Customers", "STATE": "State"},
        title="Top 10 States by Customer Count"
    )
    fig2.update_traces(marker_color='#1f77b4')
    fig2.update_layout(title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# Customer Segmentation Tab
with tab2:
    # Pie chart: Customer Status Distribution
    fig3 = px.pie(
        df_filtered,
        names="CUSTOMER STATUS",
        color="CUSTOMER STATUS",
        color_discrete_map={"Connected": "#2ca02c", "Disconnected": "#d62728"},
        hole=0.4,
        title="Customer Status Distribution"
    )
    fig3.update_layout(title_x=0.5)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Treemap: Bandwidth Allocation by Region & Client
    fig4 = px.treemap(
        df_filtered,
        path=["REGION", "CLIENT"],
        values="BANDWIDTH SUBSCRIPTION (Mbps)",
        title="Bandwidth Allocation by Region & Client"
    )
    st.plotly_chart(fig4, use_container_width=True)

# Raw Data Tab
with tab3:
    st.subheader("Filtered Customer Data")
    bandwidth_max = int(df_filtered["BANDWIDTH SUBSCRIPTION (Mbps)"].max())
    st.data_editor(
        df_filtered.convert_dtypes().astype(object),
        column_config={
            "BANDWIDTH SUBSCRIPTION (Mbps)": st.column_config.ProgressColumn(
                format="%d Mbps",
                min_value=0,
                max_value=bandwidth_max
            )
        },
        height=600,
        use_container_width=True
    )

# -------------------------------------------------------------------
# Data Export Section (Sidebar)
# -------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Data Export")

# CSV Downloads
st.sidebar.download_button(
    label="📥 Export Filtered Data",
    data=df_filtered.to_csv(index=False),
    file_name="ncc_filtered_data.csv",
    mime="text/csv",
    help="Download currently filtered dataset as CSV"
)

st.sidebar.download_button(
    label="📥 Full Dataset Export",
    data=df.to_csv(index=False),
    file_name="ncc_full_dataset.csv",
    mime="text/csv",
    help="Download complete dataset as CSV"
)

# PDF Report Download - Fixed Path
def get_pdf_path():
    """Returns the correct path to the PDF file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the script's actual directory
    pdf_path = os.path.join(base_dir, "data", "insight.pdf")  # Adjust path based on actual repo structure
    return pdf_path

try:
    pdf_path = get_pdf_path()

    # Debugging information
    st.sidebar.markdown(f"**Expected PDF path:**  \n`{pdf_path}`")

    if os.path.exists(pdf_path):  # Checks if file exists
        with open(pdf_path, "rb") as pdf_file:
            st.sidebar.download_button(
                label="📄 Download Insights Report",
                data=pdf_file.read(),
                file_name="ncc_insights_report.pdf",
                mime="application/pdf",
                help="Download comprehensive insights report (PDF)"
            )
    else:
        st.sidebar.error(f"⚠️ PDF report not found at: {pdf_path}")
        st.sidebar.markdown("**Ensure the file exists in:**")
        st.sidebar.code("data/insight.pdf")

except Exception as e:
    st.sidebar.error(f"❌ Error loading PDF: {str(e)}")