import streamlit as st
import os

# Create an upload directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Function to handle file uploads for each module
def upload_file(module_name):
    st.subheader(f"Upload Event File for {module_name}")
    uploaded_file = st.file_uploader(f"Choose a CSV file for {module_name}", type="csv")

    if uploaded_file is not None:
        # Save the file to the uploads folder
        file_path = os.path.join("uploads", f"{module_name}_events.csv")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{module_name} event file uploaded successfully!")

# Parameter setting
st.title("Backend: File Uploads and Parameter Settings")

# Upload files for each module
for module in ["CTI", "SIM", "M&O", "IAM", "GRC"]:
    upload_file(module)

# Placeholder for setting parameters (e.g., threshold)
st.subheader("Set Parameters")
threshold = st.slider("Incident Threshold", min_value=1, max_value=100, value=50)
refresh_interval = st.slider("Autorefresh Interval (seconds)", min_value=5, max_value=60, value=10)

# Save settings (for simplicity, storing settings as session state)
if st.button("Save Settings"):
    st.session_state['threshold'] = threshold
    st.session_state['refresh_interval'] = refresh_interval
    st.success("Settings saved successfully!")

# Link back to the main dashboard
st.markdown("[Go to Main Dashboard](https://share.streamlit.io/yourusername/yourrepo/main/app.py)")
