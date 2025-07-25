import pandas as pd
import os
import hashlib

USERS_FILE = "users.xlsx"

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_users_file():
    """Initialize the users file with default admin user"""
    if not os.path.exists(USERS_FILE):
        # Create default admin user
        default_users = pd.DataFrame({
            'username': ['admin'],
            'password': [hash_password('admin123')],
            'is_admin': [True]
        })
        default_users.to_excel(USERS_FILE, index=False, engine='openpyxl')
        return True
    return False

def get_users():
    """Get all users from the Excel file"""
    initialize_users_file()
    try:
        return pd.read_excel(USERS_FILE, engine='openpyxl')
    except Exception as e:
        print(f"Error reading users file: {e}")
        return pd.DataFrame()

def authenticate_user(username, password):
    """Authenticate a user"""
    users_df = get_users()
    if users_df.empty:
        return False
    
    user = users_df[users_df['username'] == username]
    if user.empty:
        return False
    
    stored_password = user.iloc[0]['password']
    return stored_password == hash_password(password)

def is_admin(username):
    """Check if a user is an admin"""
    users_df = get_users()
    if users_df.empty:
        return False
    
    user = users_df[users_df['username'] == username]
    if user.empty:
        return False
    
    return user.iloc[0]['is_admin']

def create_user(username, password, is_admin=False):
    """Create a new user"""
    users_df = get_users()
    
    # Check if user already exists
    if not users_df[users_df['username'] == username].empty:
        return False
    
    # Add new user
    new_user = pd.DataFrame({
        'username': [username],
        'password': [hash_password(password)],
        'is_admin': [is_admin]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    try:
        users_df.to_excel(USERS_FILE, index=False, engine='openpyxl')
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
