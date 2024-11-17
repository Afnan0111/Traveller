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

def login(users):
    print("Please log in")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if username in users and users[username] == password:
        print(f"Login successful! Welcome, {username}.")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    login()  # Run the login function

    if st.session_state.logged_in:
        show_trips() 

