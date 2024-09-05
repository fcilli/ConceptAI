
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Simulate dynamic data generation for dashboards
def generate_simulated_data():
    dates = pd.date_range(start='2024-01-01', periods=10)
    events = np.random.randint(10, 50, size=10)
    incidents = np.random.randint(0, 5, size=10)
    return pd.DataFrame({'Date': dates, 'Events': events, 'Incidents': incidents})

# Each dashboard logic (SIM, CTI, IAM, M&O, GRC)
def sim_dashboard():
    st.title("SIM Dashboard")
    data = generate_simulated_data()
    st.subheader("SIM Logs Data")
    st.dataframe(data)
    
    fig = px.line(data, x='Date', y='Events', title='SIM Event Trends')
    st.plotly_chart(fig)
    
    incident_breakdown = data['Incidents'].value_counts()
    fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='SIM Incident Breakdown')
    st.plotly_chart(fig)

def cti_dashboard():
    st.title("CTI Dashboard")
    data = generate_simulated_data()
    st.subheader("CTI Logs Data")
    st.dataframe(data)
    
    fig = px.line(data, x='Date', y='Events', title='CTI Event Trends')
    st.plotly_chart(fig)
    
    incident_breakdown = data['Incidents'].value_counts()
    fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='CTI Incident Breakdown')
    st.plotly_chart(fig)

def iam_dashboard():
    st.title("IAM Dashboard")
    data = generate_simulated_data()
    st.subheader("IAM Logs Data")
    st.dataframe(data)
    
    fig = px.line(data, x='Date', y='Events', title='IAM Event Trends')
    st.plotly_chart(fig)
    
    incident_breakdown = data['Incidents'].value_counts()
    fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='IAM Incident Breakdown')
    st.plotly_chart(fig)

def mo_dashboard():
    st.title("M&O Dashboard")
    data = generate_simulated_data()
    st.subheader("M&O Logs Data")
    st.dataframe(data)
    
    fig = px.line(data, x='Date', y='Events', title='M&O Event Trends')
    st.plotly_chart(fig)
    
    incident_breakdown = data['Incidents'].value_counts()
    fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='M&O Incident Breakdown')
    st.plotly_chart(fig)

def grc_dashboard():
    st.title("GRC Dashboard")
    data = generate_simulated_data()
    st.subheader("GRC Logs Data")
    st.dataframe(data)
    
    fig = px.line(data, x='Date', y='Events', title='GRC Event Trends')
    st.plotly_chart(fig)
    
    incident_breakdown = data['Incidents'].value_counts()
    fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='GRC Incident Breakdown')
    st.plotly_chart(fig)

# Orchestrator Dashboard
def orchestrator_dashboard():
    st.title("Orchestrator Dashboard")
    
    # Simulate collecting data from each area
    sim_data = generate_simulated_data()
    cti_data = generate_simulated_data()
    iam_data = generate_simulated_data()
    mo_data = generate_simulated_data()
    grc_data = generate_simulated_data()
    
    # Aggregate the incidents from all dashboards
    total_incidents = sim_data['Incidents'].sum() + cti_data['Incidents'].sum() + \
                      iam_data['Incidents'].sum() + mo_data['Incidents'].sum() + \
                      grc_data['Incidents'].sum()
    
    st.subheader(f"Total Incidents from All Dashboards: {total_incidents}")
    
    # Display individual incidents breakdown for each area
    st.write("### Incident Breakdown:")
    st.write("**SIM Incidents**: ", sim_data['Incidents'].sum())
    st.write("**CTI Incidents**: ", cti_data['Incidents'].sum())
    st.write("**IAM Incidents**: ", iam_data['Incidents'].sum())
    st.write("**M&O Incidents**: ", mo_data['Incidents'].sum())
    st.write("**GRC Incidents**: ", grc_data['Incidents'].sum())

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Orchestrator", "SIM", "CTI", "IAM", "M&O", "GRC"])

# Page routing
if page == "SIM":
    sim_dashboard()
elif page == "CTI":
    cti_dashboard()
elif page == "IAM":
    iam_dashboard()
elif page == "M&O":
    mo_dashboard()
elif page == "GRC":
    grc_dashboard()
else:
    orchestrator_dashboard()

