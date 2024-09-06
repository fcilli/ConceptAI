import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication
    return GoogleDrive(gauth)

# Authenticate Google Drive
drive = authenticate_drive()

# Upload settings to Google Drive
def upload_to_drive(file_name, file_content):
    gfile = drive.CreateFile({'title': file_name})
    gfile.SetContentString(file_content)
    gfile.Upload()  # Upload the file.
    st.success(f"{file_name} uploaded successfully to Google Drive!")

# Function to handle file uploads to Google Drive
def upload_file(module_name):
    st.subheader(f"Upload Event File for {module_name}")
    uploaded_file = st.file_uploader(f"Choose a CSV file for {module_name}", type="csv")
    
    if uploaded_file is not None:
        # Save the file to Google Drive
        file_content = uploaded_file.getvalue().decode("utf-8")
        upload_to_drive(f"{module_name}_events.csv", file_content)

# Upload files for different modules (CTI, SIM, M&O, IAM, GRC)
for module in ["CTI", "SIM", "M&O", "IAM", "GRC"]:
    upload_file(module)

# Save settings
st.subheader("Set Parameters")
threshold = st.slider("Incident Threshold", min_value=1, max_value=100, value=50)
refresh_interval = st.slider("Autorefresh Interval (seconds)", min_value=5, max_value=60, value=10)
recurring_data_trigger = st.slider("Trigger incidents on recurring data (%)", min_value=1, max_value=100, value=70)

def save_parameters(threshold, refresh_interval, recurring_data_trigger):
    settings_content = f"threshold={threshold}\nrefresh_interval={refresh_interval}\nrecurring_data_trigger={recurring_data_trigger}"
    upload_to_drive("settings.txt", settings_content)

if st.button("Save Settings"):
    save_parameters(threshold, refresh_interval, recurring_data_trigger)

st.markdown("[Go to Main Dashboard](https://conceptai-up.streamlit.app)")


    st.markdown("[Go to Main Dashboard](https://conceptai-up.streamlit.app)")
