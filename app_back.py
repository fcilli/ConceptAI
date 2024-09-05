import streamlit as st
import os

# Use the /tmp directory for storing uploaded files and settings
UPLOAD_DIR = "/tmp"

# Ensure the /tmp directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Function to handle file uploads
def upload_file(module_name):
    st.subheader(f"Upload Event File for {module_name}")
    uploaded_file = st.file_uploader(f"Choose a CSV file for {module_name}", type="csv")
    
    if uploaded_file is not None:
        # Save the uploaded file in /tmp directory
        file_path = os.path.join(UPLOAD_DIR, f"{module_name}_events.csv")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{module_name} event file uploaded successfully!")
        st.write(f"File saved temporarily at: {file_path}")

# Save parameters in a structured way
def save_parameters(threshold, refresh_interval, recurring_data_trigger):
    settings_file = os.path.join(UPLOAD_DIR, "settings.txt")
    with open(settings_file, "w") as f:
        f.write(f"threshold={threshold}\n")
        f.write(f"refresh_interval={refresh_interval}\n")
        f.write(f"recurring_data_trigger={recurring_data_trigger}\n")
    st.success("Settings saved successfully!")

# Main Backend App
st.title("Backend: File Uploads and Parameter Settings")

# File Upload for each module (CTI, SIM, M&O, IAM, GRC)
for module in ["CTI", "SIM", "M&O", "IAM", "GRC"]:
    upload_file(module)

# Parameter settings
st.subheader("Set Parameters")
threshold = st.slider("Incident Threshold", min_value=1, max_value=100, value=50)
refresh_interval = st.slider("Autorefresh Interval (seconds)", min_value=5, max_value=60, value=10)
recurring_data_trigger = st.slider("Trigger incidents on recurring data (%)", min_value=1, max_value=100, value=70)

# Save parameters when the button is clicked
if st.button("Save Settings"):
    save_parameters(threshold, refresh_interval, recurring_data_trigger)

# Link to frontend
st.markdown("[Go to Main Dashboard](https://conceptai-up.streamlit.app)")
