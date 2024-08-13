# main.py

import streamlit as st
from models import add_user, validate_user
from pages import home, upload, analysis, locations

def main():
    st.set_page_config(page_title="Data Dashboard", layout="wide")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Display the logo at the top of the sidebar
    st.sidebar.image("static/logo.png", use_column_width=True)  # Replace with your logo path

    if st.session_state.logged_in:
        # Sidebar menu
        menu = ["Home", "Upload Data", "Analyze Data", "Manage Locations"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            home.show()
        elif choice == "Upload Data":
            upload.upload_data()
        elif choice == "Analyze Data":
            analysis.analyze_data()
        elif choice == "Manage Locations":
            locations.show()
    else:
        show_login_or_registration()

def show_login_or_registration():
    st.title("Login or Register")
    
    # Show login form
    with st.form(key='login_form'):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()  # Rerun to refresh the sidebar
            else:
                st.error("Invalid username or password.")
    
    # Show registration form
    with st.form(key='register_form'):
        st.subheader("Register")
        new_username = st.text_input("New Username", key='register_username')
        new_password = st.text_input("New Password", type="password", key='register_password')
        role = st.selectbox("Role", ["Admin", "User"])
        register_button = st.form_submit_button("Register")

        if register_button:
            if new_username and new_password:
                add_user(new_username, new_password, role)
                st.success("User registered successfully!")
            else:
                st.error("Please provide both username and password.")

if __name__ == "__main__":
    main()
