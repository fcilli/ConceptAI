import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import plotly.express as px

# Authenticate Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication
    return GoogleDrive(gauth)

# Authenticate Google Drive
drive = authenticate_drive()

# Function to download files from Google Drive
def download_from_drive(file_name):
    file_list = drive.ListFile({'q': f"title='{file_name}'"}).GetList()
    if file_list:
        file = file_list[0]  # Get the first file that matches the query
        file_content = file.GetContentString()  # Download the file content as a string
        return file_content
    else:
        st.warning(f"{file_name} not found on Google Drive")
        return None

# Fetch settings from Google Drive
def fetch_settings():
    settings_content = download_from_drive("settings.txt")
    if settings_content:
        settings_data = {}
        for line in settings_content.split("\n"):
            if line:
                key, value = line.split("=")
                settings_data[key] = int(value)
        return settings_data
    else:
        return {"threshold": 50, "refresh_interval": 10, "recurring_data_trigger": 70}

# Fetch event data from Google Drive for a module
def fetch_event_data(module):
    file_content = download_from_drive(f"{module}_events.csv")
    if file_content:
        return pd.read_csv(pd.compat.StringIO(file_content))
    else:
        return pd.DataFrame({'Date': [], 'Event': []})

# Function to create Donut chart
def create_donut_chart(sources_data):
    fig = px.pie(sources_data, values='Count', names='Source', hole=0.4, title="Source Breakdown")
    st.plotly_chart(fig)

# Function to create Event vs Incident graph
def create_event_vs_incident_graph(event_df):
    st.subheader("Event vs Incident Graph")
    event_df['Incident'] = [True if i % 2 == 0 else False for i in range(len(event_df))]  # Placeholder logic
    fig = px.line(event_df, x='Date', y='Event', title="Events vs Incidents")
    st.plotly_chart(fig)

# Function to generate Incident list
def generate_incident_list(event_df):
    st.subheader("Incident List")
    incident_df = event_df[event_df['Incident'] == True]
    st.dataframe(incident_df)

# Layout for module dashboard (CTI, SIM, M&O, IAM, GRC)
def module_dashboard(module_name, settings):
    st.title(f"{module_name} Dashboard")

    # Example data for Donut chart
    sources_data = pd.DataFrame({
        'Source': ['API', 'Database', 'File System'],
        'Count': [100, 150, 50]
    })

    # Create a 2x2 layout grid
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Upper Left: Donut chart
    with col1:
        create_donut_chart(sources_data)

    # Lower Left: Event list
    event_df = fetch_event_data(module_name)
    with col3:
        st.subheader(f"Event List for {module_name}")
        st.dataframe(event_df)

    # Upper Right: Event vs Incident graph
    with col2:
        create_event_vs_incident_graph(event_df)

    # Lower Right: Incident list
    with col4:
        generate_incident_list(event_df)

# Main frontend app
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Dashboard", ["CTI", "SIM", "M&O", "IAM", "GRC"])

# Fetch settings from Google Drive
settings = fetch_settings()

# Autorefresh every X seconds based on settings
st.experimental_rerun() if st.experimental_get_query_params() and settings.get("refresh_interval", 10) else None

# Show the selected dashboard
if page == "CTI":
    module_dashboard("CTI", settings)
elif page == "SIM":
    module_dashboard("SIM", settings)
elif page == "M&O":
    module_dashboard("M&O", settings)
elif page == "IAM":
    module_dashboard("IAM", settings)
elif page == "GRC":
    module_dashboard("GRC", settings)
