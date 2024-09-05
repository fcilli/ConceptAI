
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Security Dashboard Mockup")

# Example table for logs
data = {
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'Events': [12, 15, 20],
    'Incidents': [1, 0, 2]
}

df = pd.DataFrame(data)

st.subheader("Logs Data")
st.dataframe(df)

# Donut chart example (incident breakdown)
incident_breakdown = df['Incidents'].value_counts()
fig = px.pie(values=incident_breakdown, names=incident_breakdown.index, hole=0.4, title='Incident Breakdown')
st.plotly_chart(fig)

# Line chart for event and incident trends
fig = px.line(df, x='Date', y=['Events', 'Incidents'], title="Events and Incidents Over Time")
st.plotly_chart(fig)
