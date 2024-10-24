import streamlit as st
import os
import hashlib
import csv
import time
from groq import Groq

# Define API key directly
GROQ_API_KEY = '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'

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

USERS_FILE = 'users.csv'

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, name, surname, email):
    """Register a new user by appending their details to the CSV file."""
    hashed_password = hash_password(password)
    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_password, name, surname, email])

def login_user(username, password):
    """Authenticate a user by checking username and password."""
    hashed_password = hash_password(password)
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == hashed_password:
                return True
    return False

def user_exists(username):
    """Check if a username already exists in the CSV file."""
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

def get_user_info(username):
    """Retrieve user information from the CSV file based on the username."""
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return {
                    'name': row[2],
                    'surname': row[3],
                    'email': row[4]
                }
    return None

def update_user_info(username, new_name, new_surname, new_email, new_password):
    """Update user information in the CSV file."""
    updated = False
    rows = []
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                hashed_password = hash_password(new_password) if new_password else row[1]
                rows.append([username, hashed_password, new_name, new_surname, new_email])
                updated = True
            else:
                rows.append(row)

    if updated:
        with open(USERS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

def create_users_file():
    """Create the users CSV file with headers if it does not exist."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'name', 'surname', 'email'])

# Set page configuration
st.set_page_config(page_title="Farming Website", page_icon="🌾")

# Create users file if it doesn't exist
create_users_file()

# Navbar HTML with a green background
nav_html = """
<style>
    body {
        background-color: #e8f5e9;
    }
    .navbar {
        background-color: green;
        padding: 1rem;
        display: flex;
        justify-content: space-around;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-size: 20px;
        font-weight: bold;
    }
</style>

<div class="navbar">
    <a href="#home">Home</a>
    <a href="#about">About</a>
    <a href="#farming">Farming</a>
    <a href="#livestock">Livestock</a>
    <a href="#vegetables">Vegetables</a>
    <a href="#contact">Contact Us</a>
</div>
"""

# Display the navbar
st.markdown(nav_html, unsafe_allow_html=True)

# Main content sections
st.title("Welcome to Our Farming, Livestock, and Vegetables Website")

st.markdown("""
## Home
Explore the best in farming, livestock, and vegetables!

## About
We are dedicated to providing fresh produce and quality livestock to our customers.

## Farming
Learn more about our farming practices and how we ensure sustainable and organic produce.

## Livestock
Our livestock are well taken care of, ensuring the highest quality meat and dairy products.

## Vegetables
We grow a variety of vegetables, using organic methods to keep them fresh and healthy.

## Contact Us
Feel free to reach out to us for any inquiries.
""")
