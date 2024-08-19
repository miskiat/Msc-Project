# pages/home.py

import streamlit as st
import pandas as pd
import os

USER_CSV_PATH = 'data/users.csv'
DATA_CSV_PATH = 'data/data.csv'

def get_data_stats():
    if os.path.exists(DATA_CSV_PATH):
        df = pd.read_csv(DATA_CSV_PATH)
        num_data_points = len(df)
    else:
        num_data_points = 0
    return num_data_points

def get_location_count():
    if os.path.exists(DATA_CSV_PATH):
        df = pd.read_csv(DATA_CSV_PATH)
        num_locations = df['Location'].nunique()
    else:
        num_locations = 0
    return num_locations

def get_registered_users():
    if os.path.exists(USER_CSV_PATH):
        df = pd.read_csv(USER_CSV_PATH)
        num_users = len(df)
    else:
        num_users = 0
    return num_users

def show():
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
    st.title("Home Page")

    if 'username' in st.session_state:
        st.title(f"Hello, {st.session_state.username}! 👋🏾")

    st.write("Dashboard Statistics:")

    # Create three columns for the statistics
    col1, col2, col3 = st.columns(3)

    # Data for statistics
    stats = {
        "Number of Data Points": get_data_stats(),
        "Number of Locations": get_location_count(),
        "Number of Registered Users": get_registered_users()
    }

    # Display statistics in columns
    with col1:
        st.markdown("""
        <div style="border-radius: 15px; padding: 20px; background-color: #f0f0f0; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 20px; color: #333;">Number of Data Points</div>
            <div style="font-size: 36px; font-weight: bold; color: #ff0088;">{}</div>
        </div>
        """.format(stats["Number of Data Points"]), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border-radius: 15px; padding: 20px; background-color: #f0f0f0; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 20px; color: #333;">Number of Locations</div>
            <div style="font-size: 36px; font-weight: bold; color: #ff0088;">{}</div>
        </div>
        """.format(stats["Number of Locations"]), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="border-radius: 15px; padding: 20px; background-color: #f0f0f0; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 20px; color: #333;">Number of Registered Users</div>
            <div style="font-size: 36px; font-weight: bold; color: #ff0088;">{}</div>
        </div>
        """.format(stats["Number of Registered Users"]), unsafe_allow_html=True)

if __name__ == "__main__":
    show()
