import streamlit as st
import os

# Create an upload directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Function to handle file uploads with a progress bar
def upload_file(module_name):
    st.subheader(f"Upload Event File for {module_name}")
    uploaded_file = st.file_uploader(f"Choose a CSV file for {module_name}", type="csv")
    
    if uploaded_file is not None:
        # Create a progress bar
        progress_bar = st.progress(0)
        bytes_data = uploaded_file.getvalue()
        total_size = len(bytes_data)

        # Simulate writing file with progress bar
        file_path = os.path.join("uploads", f"{module_name}_events.csv")
        with open(file_path, "wb") as f:
            chunk_size = 1024
            for i in range(0, total_size, chunk_size):
                f.write(bytes_data[i:i + chunk_size])
                progress = min((i + chunk_size) / total_size, 1.0)
                progress_bar.progress(progress)
        st.success(f"{module_name} event file uploaded successfully!")

# Save parameters in a structured way for the frontend to use
def save_parameters(threshold, refresh_interval, recurring_data_trigger):
    with open("uploads/settings.txt", "w") as f:
        f.write(f"threshold={threshold}\n")
        f.write(f"refresh_interval={refresh_interval}\n")
        f.write(f"recurring_data_trigger={recurring_data_trigger}\n")
    st.success("Settings saved successfully!")

# Parameter setting
st.title("Backend: File Uploads and Parameter Settings")

# Upload files for each module
for module in ["CTI", "SIM", "M&O", "IAM", "GRC"]:
    upload_file(module)

# Parameter section
st.subheader("Set Parameters")
threshold = st.slider("Incident Threshold", min_value=1, max_value=100, value=50)
refresh_interval = st.slider("Autorefresh Interval (seconds)", min_value=5, max_value=60, value=10)
recurring_data_trigger = st.slider("Trigger incidents on recurring data (%)", min_value=1, max_value=100, value=70)

# Save settings button
if st.button("Save Settings"):
    save_parameters(threshold, refresh_interval, recurring_data_trigger)

# Link back to the main dashboard
st.markdown("[Go to Main Dashboard](https://share.streamlit.io/yourusername/yourrepo/main/app.py)")
