import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from utils import get_data

def analyze_data():
    st.header("Data Analysis")
    
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        df = get_data()
        
        if df.empty:
            st.write("No data available.")
            return
        
        location = st.selectbox("Select Location", df['location'].unique())
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        
        filtered_df = df[(df['timestamp'] >= pd.Timestamp(start_date)) & (df['timestamp'] <= pd.Timestamp(end_date))]
        
        if st.button("Generate Plot"):
            if filtered_df.empty:
                st.write("No data available for the selected criteria.")
            else:
                st.subheader("Temperature vs Time")
                plt.figure(figsize=(10, 5))
                plt.plot(filtered_df['timestamp'], filtered_df['Temp'])
                plt.xlabel("Time")
                plt.ylabel("Temperature")
                plt.title("Temperature over Time")
                st.pyplot(plt)
    else:
        st.write("Please log in to analyze data.")
