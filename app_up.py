import streamlit as st
import requests

# Backend URL
BACKEND_URL = "https://conceptai-back.streamlit.app"

# Function to fetch settings from the backend
def fetch_settings():
    url = f"{BACKEND_URL}/?endpoint=settings"
    response = requests.get(url)
    
    # Handle non-JSON response gracefully
    try:
        data = response.json()  # Try to parse the response as JSON
    except ValueError:
        st.error("Failed to fetch settings from backend. Response is not valid JSON.")
        return {"threshold": 50, "refresh_interval": 10, "recurring_data_trigger": 70}

    if response.status_code == 200:
        # If the file is missing but default settings are provided
        if data["status"] == "error" and "default_settings" in data:
            settings_data = {}
            for line in data["default_settings"].split("\n"):
                if line:
                    key, value = line.split("=")
                    settings_data[key] = int(value)
            st.warning(data["message"])  # Display the error message
            return settings_data
        
        elif data["status"] == "success":
            settings_data = {}
            for line in data["settings"].split("\n"):
                if line:
                    key, value = line.split("=")
                    settings_data[key] = int(value)
            return settings_data
    else:
        st.warning(data.get("message", "Unknown error occurred while fetching settings."))
        return {"threshold": 50, "refresh_interval": 10, "recurring_data_trigger": 70}
