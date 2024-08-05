import streamlit as st
from models import add_user, validate_user
from pages import home, upload, analysis

def main():
    st.set_page_config(page_title="Data Dashboard", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Sidebar menu
    menu = ["Home", "Upload Data", "Analyze Data"]
    choice = st.sidebar.selectbox("Menu", menu)

    if st.session_state.logged_in:
        if choice == "Home":
            home.show()  # Calls the show function in home.py
        elif choice == "Upload Data":
            upload.upload_data()  # Calls the upload_data function in upload.py
        elif choice == "Analyze Data":
            analysis.analyze_data()  # Calls the analyze_data function in analysis.py
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
                st.experimental_rerun()
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
