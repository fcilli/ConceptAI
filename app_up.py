import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# Backend URL
BACKEND_URL = "https://conceptai-back.streamlit.app"

# Function to fetch settings from the backend
def fetch_settings():
    url = f"{BACKEND_URL}/?endpoint=settings"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            settings_data = {}
            for line in data["settings"].split("\n"):
                if line:
                    key, value = line.split("=")
                    settings_data[key] = int(value)
            return settings_data
        else:
            st.warning(data["message"])
    else:
        st.warning("Failed to fetch settings from backend.")
    return {"threshold": 50, "refresh_interval": 10, "recurring_data_trigger": 70}

# Function to fetch event data from the backend
def fetch_event_data(module):
    url = f"{BACKEND_URL}/?endpoint=events&module={module}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            df = pd.read_csv(pd.compat.StringIO(response.text))
            return df
        except:
            st.warning(f"No event data available for {module}.")
            return pd.DataFrame({'Date': [], 'Event': []})
    else:
        st.warning(f"Failed to fetch event data for {module}.")
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

# Fetch settings from the backend
settings = fetch_settings()

# Autorefresh every X seconds based on settings
st_autorefresh(interval=settings["refresh_interval"] * 1000, key="data_refresh")

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

