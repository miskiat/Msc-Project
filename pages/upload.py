# pages/upload.py

import streamlit as st
import pandas as pd
import os

LOCATIONS_CSV_PATH = 'data/locations.csv'
DATA_CSV_PATH = 'data/data.csv'

def load_locations():
    if os.path.exists(LOCATIONS_CSV_PATH):
        return pd.read_csv(LOCATIONS_CSV_PATH)
    else:
        return pd.DataFrame(columns=['id', 'name'])

def upload_data():
    st.title("Upload Data")
    st.write("Upload your CSV files here and select a location.")

    df_locations = load_locations()

    if df_locations.empty:
        st.write("No locations available. Please add locations first.")
        return

    location_options = df_locations.set_index('id')['name'].to_dict()
    selected_location_id = st.selectbox("Select Location", options=list(location_options.keys()), format_func=lambda x: location_options.get(x))

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            data['Location'] = selected_location_id  # Assign the selected location ID to the data
            if os.path.exists(DATA_CSV_PATH):
                existing_data = pd.read_csv(DATA_CSV_PATH)
                combined_data = pd.concat([existing_data, data], ignore_index=True)
            else:
                combined_data = data
            combined_data.to_csv(DATA_CSV_PATH, index=False)
            st.success("File successfully uploaded!")
            st.write(data.head())  # Display the first few rows of the uploaded data
        except Exception as e:
            st.error(f"Error reading the file: {e}")
