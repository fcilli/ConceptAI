import streamlit as st
import os
import json

# Use /tmp directory for storage
UPLOAD_DIR = "/tmp"

# Ensure the /tmp directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# API Endpoint logic
params = st.experimental_get_query_params()
if 'endpoint' in params:
    # Serve the settings
    if params['endpoint'][0] == 'settings':
        settings_file = os.path.join(UPLOAD_DIR, "settings.txt")
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                settings_data = f.read()
            st.write(json.dumps({"status": "success", "settings": settings_data}))
        else:
            # Return a default settings response if file not found
            st.write(json.dumps({
                "status": "error", 
                "message": "No settings file found",
                "default_settings": "threshold=50\nrefresh_interval=10\nrecurring_data_trigger=70"
            }))

    # Serve the event data
    elif params['endpoint'][0] == 'events':
        module = params.get('module', [''])[0]
        event_file = os.path.join(UPLOAD_DIR, f"{module}_events.csv")
        if os.path.exists(event_file):
            with open(event_file, "r") as f:
                st.write(f.read())
        else:
            st.write(json.dumps({"status": "error", "message": f"No event file for {module} found"}))

else:
    # Normal backend functionality for file uploads and parameter setting

    st.title("Backend: File Uploads and Parameter Settings")

    # Function to handle file uploads
    def upload_file(module_name):
        st.subheader(f"Upload Event File for {module_name}")
        uploaded_file = st.file_uploader(f"Choose a CSV file for {module_name}", type="csv")
        
        if uploaded_file is not None:
            # Save file in /tmp directory
            file_path = os.path.join(UPLOAD_DIR, f"{module_name}_events.csv")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"{module_name} event file uploaded successfully!")
            st.write(f"File temporarily saved at: {file_path}")

    # Upload files for different modules
    for module in ["CTI", "SIM", "M&O", "IAM", "GRC"]:
        upload_file(module)

    # Save parameters
    st.subheader("Set Parameters")
    threshold = st.slider("Incident Threshold", min_value=1, max_value=100, value=50)
    refresh_interval = st.slider("Autorefresh Interval (seconds)", min_value=5, max_value=60, value=10)
    recurring_data_trigger = st.slider("Trigger incidents on recurring data (%)", min_value=1, max_value=100, value=70)

    def save_parameters(threshold, refresh_interval, recurring_data_trigger):
        settings_file = os.path.join(UPLOAD_DIR, "settings.txt")
        with open(settings_file, "w") as f:
            f.write(f"threshold={threshold}\n")
            f.write(f"refresh_interval={refresh_interval}\n")
            f.write(f"recurring_data_trigger={recurring_data_trigger}\n")
        st.success("Settings saved successfully!")

    # Save the settings to /tmp when button is clicked
    if st.button("Save Settings"):
        save_parameters(threshold, refresh_interval, recurring_data_trigger)

    st.markdown("[Go to Main Dashboard](https://conceptai-up.streamlit.app)")
