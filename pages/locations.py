# pages/locations.py

import streamlit as st
import pandas as pd
import os

LOCATIONS_CSV_PATH = 'data/locations.csv'

def load_locations():
    if os.path.exists(LOCATIONS_CSV_PATH):
        return pd.read_csv(LOCATIONS_CSV_PATH)
    else:
        return pd.DataFrame(columns=['id', 'name'])

def save_locations(df):
    df.to_csv(LOCATIONS_CSV_PATH, index=False)

def show():
    st.title("Manage Locations")

    # Load locations from CSV
    df = load_locations()

    # Display existing locations with search and pagination
    st.subheader("Existing Locations")

    # Search functionality
    search_query = st.text_input("Search Location", "")
    if search_query:
        df = df[df['name'].str.contains(search_query, case=False, na=False)]

    # Pagination functionality
    page_size = 10
    total_items = len(df)
    if total_items > 0:
        total_pages = (total_items // page_size) + (1 if total_items % page_size > 0 else 0)
        if total_pages > 1:
            page = st.slider("Page", 1, total_pages, 1)
        else:
            page = 1

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        df_page = df[start_index:end_index]
    else:
        total_pages = 1
        page = 1
        df_page = df  # No pagination needed

    # Display the table with maximum width
    st.dataframe(df_page, width=1000)  # Adjust the width as needed

    # Add new location
    with st.form(key='add_location_form'):
        st.subheader("Add New Location")
        location_name = st.text_input("Location Name", key='add_location_name')
        add_button = st.form_submit_button("Add Location")

        if add_button:
            if location_name:
                # Check for duplicate (case-insensitive)
                if location_name.lower() in df['name'].str.lower().values:
                    st.error("Location already exists.")
                else:
                    new_id = df['id'].max() + 1 if not df.empty else 1
                    new_row = pd.DataFrame({'id': [new_id], 'name': [location_name]})
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_locations(df)
                    st.success("Location added successfully!")
                    st.experimental_rerun()  # Refresh the page to show updated data
            else:
                st.error("Location name cannot be empty.")

    # Edit existing location
    if not df.empty:
        st.subheader("Edit Location")
        location_id = st.selectbox("Select Location to Edit", df['id'], key='edit_location_id')
        if location_id != st.session_state.get('edit_location_id', None):
            st.session_state.edit_location_id = location_id
            st.session_state.edit_location_name = df[df['id'] == location_id]['name'].values[0]

        with st.form(key='edit_location_form'):
            new_name = st.text_input("New Location Name", value=st.session_state.get('edit_location_name', ''), key='edit_location_name')
            edit_button = st.form_submit_button("Update Location")

            if edit_button:
                if new_name:
                    if new_name.lower() in df['name'].str.lower().values and new_name.lower() != df[df['id'] == location_id]['name'].values[0].lower():
                        st.error("Location name already exists.")
                    else:
                        df.loc[df['id'] == st.session_state.edit_location_id, 'name'] = new_name
                        save_locations(df)
                        st.success("Location updated successfully!")
                        st.experimental_rerun()  # Refresh the page to show updated data
                else:
                    st.error("Location name cannot be empty.")
