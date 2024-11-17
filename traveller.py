import streamlit as st
import csv

# Title of the website
st.title('The Traveller Extra Trips')

import csv

def load_users_from_csv(file_path):
    users = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"]] = row["password"]
    return users

database_type = "csv"

def login(username, password):
    user_data = load_users_from_csv("users.csv")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Login form
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in user_data and user_data[username] == password:
                st.session_state.logged_in = True
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password")
    else:
        st.success("You are logged in!")
        if st.button("Log out"):
            st.session_state.logged_in = False



# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

if selection == "Home":
    st.title("Welcome to the Home Page!")
    st.write("This is the main content of the website.")
elif selection == "About":
    st.title("About Us")
    st.write("This is some information about the website.")
else:
    st.title("Contact")
    st.write("Feel free to contact us at contact@example.com.")
