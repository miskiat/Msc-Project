import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

USER_CSV_PATH = 'data/users.csv'
SITE_CSV_PATH = 'data/sites.csv'

# User management functions
def load_users():
    try:
        return pd.read_csv(USER_CSV_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['user_id', 'username', 'password', 'role'])

def get_user(username):
    df = load_users()
    user = df[df['username'] == username]
    if not user.empty:
        return user.iloc[0]  # Return the first matching user
    return None

def validate_user(username, password):
    user = get_user(username)
    if user is not None:
        hashed_password = user['password']
        return check_password_hash(hashed_password, password)
    return False

def save_users(df):
    df.to_csv(USER_CSV_PATH, index=False)

def add_user(username, password, role):
    df = load_users()
    if not df[df['username'] == username].empty:
        return "Username already exists"

    user_id = df['user_id'].max() + 1 if not df.empty else 1
    hashed_password = generate_password_hash(password)
    new_user = pd.DataFrame({
        'user_id': [user_id],
        'username': [username],
        'password': [hashed_password],
        'role': [role]
    })
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    return None

def admin_add_user(username, password, role):
    # Only admin can use this function
    return add_user(username, password, role)

def get_all_users():
    return load_users()

def update_user(username, new_role=None, new_password=None):
    df = load_users()
    user_idx = df[df['username'] == username].index

    if user_idx.empty:
        return False
    
    if new_role is not None:
        df.at[user_idx, 'role'] = new_role

    if new_password:
        hashed_password = generate_password_hash(new_password)
        df.at[user_idx, 'password'] = hashed_password

    save_users(df)
    return True

def delete_user(username):
    df = load_users()
    df = df[df['username'] != username]
    save_users(df)
    return True

# Site management functions
def load_sites():
    try:
        return pd.read_csv(SITE_CSV_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['site_id', 'site_name', 'location'])

def save_sites(df):
    df.to_csv(SITE_CSV_PATH, index=False)

def add_site(site_name, location):
    df = load_sites()
    site_id = df['site_id'].max() + 1 if not df.empty else 1
    new_site = pd.DataFrame({
        'site_id': [site_id],
        'site_name': [site_name],
        'location': [location]
    })
    df = pd.concat([df, new_site], ignore_index=True)
    save_sites(df)

def get_site(site_name):
    df = load_sites()
    return df[df['site_name'] == site_name].iloc[0] if not df[df['site_name'] == site_name].empty else None
