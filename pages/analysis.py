# pages/analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import os

DATA_CSV_PATH = 'data/data.csv'  # Adjust path if necessary
LOCATIONS_CSV_PATH = 'data/locations.csv'  # Adjust path if necessary

def load_data():
    # Add custom CSS
    st.markdown("""
        <style>
        .st-emotion-cache-1s0bj5q {
            max-height: 0;
            list-style: none;
            overflow: overlay;
            margin: 0px;
            padding-top: 0;
            padding-bottom: 0;
            visibility: hidden;
        }
        </style>
        """, unsafe_allow_html=True)
    if os.path.exists(DATA_CSV_PATH):
        return pd.read_csv(DATA_CSV_PATH)
    else:
        return pd.DataFrame()

def load_locations():
    if os.path.exists(LOCATIONS_CSV_PATH):
        return pd.read_csv(LOCATIONS_CSV_PATH)
    else:
        return pd.DataFrame(columns=['id', 'name'])

def analyze_data():
    st.title("Analyze Data")

    # Load data
    df = load_data()
    locations_df = load_locations()

    if df.empty:
        st.warning("No data available for analysis.")
        return

    if locations_df.empty:
        st.warning("No locations available. Please add locations first.")
        return

    # Convert 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

    # Select date range
    min_date, max_date = df['Time'].min(), df['Time'].max()
    start_date = st.date_input("Start Date", min_date)
    end_date = st.date_input("End Date", max_date)

    if start_date > end_date:
        st.warning("End date must be after the start date.")
        return

    # Filter data based on selected date range
    filtered_df = df[(df['Time'] >= pd.to_datetime(start_date)) & (df['Time'] <= pd.to_datetime(end_date))]

    if filtered_df.empty:
        st.warning("No data available for the selected date range.")
        return

    # Create a dictionary for location ID and name mapping
    location_map = dict(zip(locations_df['name'], locations_df['id']))

    # Select locations to compare
    location_names = list(location_map.keys())
    selected_location_names = st.multiselect("Select Locations to Compare", location_names, key="location_selector")

    if not selected_location_names:
        st.warning("Please select at least one location.")
        return

    # Get the IDs of the selected locations
    selected_location_ids = [location_map[name] for name in selected_location_names]

    # Filter data based on selected location IDs
    filtered_df = filtered_df[filtered_df['Location'].isin(selected_location_ids)]

    if filtered_df.empty:
        st.warning("No data available for the selected locations and date range.")
        return

    # Set 'Time' column as index for plotting
    filtered_df.set_index('Time', inplace=True)

    # Define consistent colors for features
    feature_colors = {
        'IR': 'blue',
        'Lux': 'orange',
        'Magnitude of Acceleration': 'green',
        'Magnetic Field Strength': 'red',
        'H.Angle': 'purple',
        'VBAT': 'brown',
        'Temp': 'pink'
    }

    # Create a line chart for each selected location
    for location_id in selected_location_ids:
        location_name = locations_df[locations_df['id'] == location_id]['name'].values[0]
        location_data = filtered_df[filtered_df['Location'] == location_id]
        
        if location_data.empty:
            st.warning(f"No data available for location: {location_name} in the selected date range.")
            continue
        
        # Feature selection
        features = list(feature_colors.keys())
        selected_features = st.multiselect("Select Features to Display", features, default=features, key=f"features_selector_{location_id}")

        # Compute additional features
        if 'Magnitude of Acceleration' in selected_features:
            if {'Accel_X', 'Accel_Y', 'Accel_Z'}.issubset(location_data.columns):
                location_data['Magnitude of Acceleration'] = np.sqrt(location_data['Accel_X']**2 + location_data['Accel_Y']**2 + location_data['Accel_Z']**2)
        
        if 'Magnetic Field Strength' in selected_features:
            if {'Mag_X', 'Mag_Y', 'Mag_Z'}.issubset(location_data.columns):
                location_data['Magnetic Field Strength'] = np.sqrt(location_data['Mag_X']**2 + location_data['Mag_Y']**2 + location_data['Mag_Z']**2)
        
        # Filter columns based on selected features and available data
        plot_columns = []
        for feature in selected_features:
            if feature in location_data.columns or feature == 'Temp':
                plot_columns.append(feature)
            elif feature == 'Temp':
                st.warning(f"Temperature data (Temp) is not available for location: {location_name}")

        if plot_columns:
            st.subheader(f"Data for Location: {location_name}")
            st.line_chart(location_data[plot_columns].copy(), use_container_width=True)
        else:
            st.warning(f"No valid columns to plot for location: {location_name}")

    st.success("Analysis complete!")
