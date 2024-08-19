import streamlit as st
from models import load_users, save_users, get_user, update_user, delete_user, admin_add_user

def show():
    st.title("User Management")

    if 'action' in st.session_state:
        if st.session_state.action == 'edit':
            edit_user(st.session_state.selected_user)
        elif st.session_state.action == 'delete':
            confirm_delete(st.session_state.selected_user)
        # Clear session state after handling the action
        del st.session_state.action
        del st.session_state.selected_user
        return

    # Display users in a table with Edit and Delete buttons in the same row
    users_df = load_users()
    if users_df.empty:
        st.write("No users to display.")
        return

    for _, user in users_df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

        col1.write(f"**Username:** {user['username']}")
        col2.write(f"**Role:** {user['role']}")

        with col3:
            if st.button(f"Edit {user['username']}", key=f"edit_{user['username']}"):
                st.session_state.selected_user = user['username']
                st.session_state.action = 'edit'
                st.experimental_rerun()

        with col4:
            if st.button(f"Delete {user['username']}", key=f"delete_{user['username']}"):
                st.session_state.selected_user = user['username']
                st.session_state.action = 'delete'
                st.experimental_rerun()

    st.subheader("Add New User")
    with st.form(key='add_user_form'):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["User", "Admin"])
        submit_button = st.form_submit_button("Add User")

        if submit_button:
            error = admin_add_user(new_username, new_password, role)
            if error:
                st.error(error)
            else:
                st.success("User added successfully!")
                st.experimental_rerun()

def edit_user(username):
    st.subheader(f"Edit User: {username}")

    user = get_user(username)
    if user is None:
        st.error("User not found.")
        return

    with st.form(key='edit_form'):
        new_role = st.selectbox("New Role", ["User", "Admin"], index=["User", "Admin"].index(user['role']))
        new_password = st.text_input("New Password (leave empty to keep current password)", type="password")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if new_password:
                update_user(username, new_role, new_password)
            else:
                update_user(username, new_role=new_role)

            st.success(f"User {username} updated successfully!")
            st.session_state.action = None
            st.experimental_rerun()

def confirm_delete(username):
    st.warning(f"Are you sure you want to delete {username}?")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Yes, Delete"):
            delete_user(username)
            st.success(f"User {username} deleted successfully!")
            st.session_state.action = None
            st.experimental_rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.action = None
            st.experimental_rerun()
