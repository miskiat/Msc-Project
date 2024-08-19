# main.py

import streamlit as st
from models import add_user, validate_user, get_user
from pages import home, upload, analysis, locations, user_management

def main():
    st.set_page_config(page_title="Data Dashboard", layout="wide")

    # Add custom CSS
    st.markdown("""
        <style>
        .st-emotion-cache-1s0bj5q{
            max-height: 0;
            list-style: none;
            overflow: hidden;
            margin: 0px;
            padding-top: 0;
            padding-bottom: 0;
            visibility: hidden;
            display: none;
        }
        .st-emotion-cache-dvghzm {
            max-height: 0vh;
            list-style: none;
            overflow: hidden;
            margin: 0px;
            padding-top: 6rem;
            padding-bottom: 1rem;
            visibility: hidden;
            display: none;
        }
                .stApp .sidebar-content {
            display: none; /* Hides the sidebar content */
        }
        .stApp .css-1q6w1v3 {
            display: none; /* Hides unwanted sidebars */
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Display the logo at the top of the page and add logout functionality
    if st.session_state.logged_in:
        st.sidebar.image("static/logo.png", use_column_width=True)  # Display logo in the sidebar
        st.sidebar.title("Menu")

        # Sidebar menu
        menu = ["Home", "Upload Data", "Analyze Data", "Manage Locations", "User Management"]
        choice = st.sidebar.selectbox("Select Page", menu)

        if choice == "Home":
            home.show()
        elif choice == "Upload Data":
            upload.upload_data()
        elif choice == "Analyze Data":
            analysis.analyze_data()
        elif choice == "Manage Locations":
            locations.show()
        elif choice == "User Management":
            user_management.show()

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_rerun()  # Rerun to refresh the page
    else:
        show_login_or_registration()

def show_login_or_registration():
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
    
    st.title("Login or Register")

    # Tabs for Login and Registration
    tab = st.selectbox("Select Tab", ["Login", "Register"])

    if tab == "Login":
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

    elif tab == "Register":
        with st.form(key='register_form'):
            st.subheader("Register")
            new_username = st.text_input("New Username", key='register_username')
            new_password = st.text_input("New Password", type="password", key='register_password')
            role = st.selectbox("Role", ["Admin", "User"])
            register_button = st.form_submit_button("Register")

            if register_button:
                if new_username and new_password:
                    if get_user(new_username) is None:  # Check if username already exists
                        add_user(new_username, new_password, role)
                        st.success("User registered successfully!")
                    else:
                        st.error("Username already exists.")
                else:
                    st.error("Please provide both username and password.")

if __name__ == "__main__":
    main()
