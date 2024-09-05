import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Function to read settings from the backend app
def read_settings():
    settings = {
        "threshold": 50,
        "refresh_interval": 10,
        "recurring_data_trigger": 70
    }
    settings_file = "uploads/settings.txt"
    
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                settings[key] = int(value)
    return settings

# Function to create a Donut chart
def create_donut_chart(sources_data):
    fig = px.pie(sources_data, values='Count', names='Source', hole=0.4, title="Source Breakdown")
    st.plotly_chart(fig)

# Function to load the event list from CSV
def load_event_list(module_name):
    file_path = f"uploads/{module_name}_events.csv"
    if not os.path.exists(file_path):
        return pd.DataFrame({
            'Date': ['No Data Available'],
            'Event': ['No events uploaded yet']
        })
    return pd.read_csv(file_path)

# Function to create event vs incident graph
def create_event_vs_incident_graph(event_df):
    st.subheader("Event vs Incident Graph")
    event_df['Incident'] = [True if i % 2 == 0 else False for i in range(len(event_df))]  # Placeholder logic
    fig = px.line(event_df, x='Date', y='Event', title="Events vs Incidents")
    st.plotly_chart(fig)

# Function to generate the incident list
def generate_incident_list(event_df):
    st.subheader("Incident List")
    incident_df = event_df[event_df['Incident'] == True]  # Placeholder logic
    st.dataframe(incident_df)

# Layout for Level 2 Dashboards (CTI, SIM, M&O, IAM, GRC)
def level_2_dashboard(module_name, settings):
    st.title(f"{module_name} Dashboard")

    # Example data for donut chart
    sources_data = pd.DataFrame({
        'Source': ['API', 'Database', 'File System'],
        'Count': [100, 150, 50]
    })

    # Create a 2x2 grid for the layout
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Upper Left: Donut Chart
    with col1:
        create_donut_chart(sources_data)

    # Lower Left: Event List
    event_df = load_event_list(module_name)
    with col3:
        st.subheader(f"Event List ({module_name})")
        st.dataframe(event_df)

    # Upper Right: Event vs Incident Graph
    with col2:
        create_event_vs_incident_graph(event_df)

    # Lower Right: Incident List
    with col4:
        generate_incident_list(event_df)

# Layout for Orchestrator Dashboard
def orchestrator_dashboard(settings):
    st.title("Orchestrator Dashboard")

    # Example data for donut chart
    sources_data = pd.DataFrame({
        'Source': ['CTI', 'SIM', 'M&O', 'IAM', 'GRC'],
        'Count': [100, 200, 150, 120, 180]
    })

    # Create a 2x2 grid for the layout
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Upper Left: Donut Chart
    with col1:
        create_donut_chart(sources_data)

    # Lower Left: Aggregated Event List (Placeholder for now)
    event_df = pd.DataFrame({
        'Date': ['2024-09-05', '2024-09-06', '2024-09-07'],
        'Event': ['Incident Report', 'System Alert', 'File Tampering'],
        'Incident': [True, False, True]
    })
    with col3:
        st.subheader("Aggregated Event List (Placeholder)")
        st.dataframe(event_df)

    # Upper Right: Aggregated Event vs Incident Graph
    with col2:
        create_event_vs_incident_graph(event_df)

    # Lower Right: Aggregated Incident List
    with col4:
        generate_incident_list(event_df)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Dashboard", ["CTI", "SIM", "M&O", "IAM", "GRC", "Orchestrator"])

# Load settings from the backend app
settings = read_settings()

# Display the selected dashboard
if page == "CTI":
    level_2_dashboard("CTI", settings)
elif page == "SIM":
    level_2_dashboard("SIM", settings)
elif page == "M&O":
    level_2_dashboard("M&O", settings)
elif page == "IAM":
    level_2_dashboard("IAM", settings)
elif page == "GRC":
    level_2_dashboard("GRC", settings)
else:
    orchestrator_dashboard(settings)
