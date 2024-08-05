import streamlit as st
import pandas as pd
from utils import process_csv
from models import get_user

def upload_data():
    st.header("Upload Data")
    
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = get_user(st.session_state.username)['user_id']

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        location = st.text_input("Enter Location")

        if st.button("Upload"):
            if uploaded_file and location:
                df = pd.read_csv(uploaded_file)
                if process_csv(df, location, user_id):
                    st.success("Data uploaded successfully!")
                else:
                    st.error("Failed to upload data.")
            else:
                st.error("Please provide both file and location.")
    else:
        st.write("Please log in to upload data.")
