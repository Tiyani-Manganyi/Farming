import streamlit as st
import os
import hashlib
import csv

# Define users file
USERS_FILE = 'users.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, name, surname, email):
    hashed_password = hash_password(password)
    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_password, name, surname, email])

def login_user(username, password):
    hashed_password = hash_password(password)
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == hashed_password:
                return True
    return False

def create_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'name', 'surname', 'email'])

# Create the users file
create_users_file()

# Page configuration
st.set_page_config(page_title="Farming System", page_icon="🌾")

# CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        body {
            font-family: 'Poppins', sans-serif;
            background-image: url('https://via.placeholder.com/1500x1000.png?text=Farming+Background'); /* Replace with an actual farming image URL */
            background-size: cover;
            background-attachment: fixed;
        }

        .form-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .form-container h2 {
            text-align: center;
            margin-bottom: 20px;
            color: green;
        }

        .form-container input[type="text"],
        .form-container input[type="password"],
        .form-container input[type="email"],
        .form-container button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .form-container button {
            background: green;
            color: white;
            border: none;
            cursor: pointer;
        }

        .form-container button:hover {
            background: darkgreen;
        }
    </style>
""", unsafe_allow_html=True)

# Display forms
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Registration form
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.header("Sign Up")
        reg_username = st.text_input("Username")
        reg_password = st.text_input("Password", type="password")
        reg_name = st.text_input("Name")
        reg_surname = st.text_input("Surname")
        reg_email = st.text_input("Email")
        if st.button("Register"):
            register_user(reg_username, reg_password, reg_name, reg_surname, reg_email)
            st.success("Registered successfully!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Login form
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.header("Login")
        log_username = st.text_input("Login Username")
        log_password = st.text_input("Login Password", type="password")
        if st.button("Login"):
            if login_user(log_username, log_password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.write("Welcome! You are logged in.")
