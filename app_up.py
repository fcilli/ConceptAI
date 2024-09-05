import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Use the same /tmp directory as the backend to access files
UPLOAD_DIR = "/tmp"

# Function to read settings from the backend app
def read_settings():
    settings_file = os.path.join(UPLOAD_DIR, "settings.txt")
    settings = {
        "threshold": 50,  # Default value
        "refresh_interval": 10,  # Default value
        "recurring_data_trigger": 70  # Default value
    }

    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                settings[key] = int(value)

    return settings

# Function to load event list from uploaded CSV files
def load_event_list(module_name):
    file_path = os.path.join(UPLOAD_DIR, f"{module_name}_events.csv")
    
    # If no file exists, show placeholder data
    if not os.path.exists(file_path):
        return pd.DataFrame({
            'Date': ['No Data Available'],
            'Event': ['No events uploaded yet']
        })

    # Load data from the uploaded CSV file
    return pd.read_csv(file_path)

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

# Dashboard for each module (CTI, SIM, M&O, IAM, GRC)
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
    event_df = load_event_list(module_name)
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

# Read settings from backend (saved in /tmp)
settings = read_settings()

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
