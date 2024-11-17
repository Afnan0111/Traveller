import streamlit as st
import csv

# Title of the website
st.title('The Traveller Extra Trips')

# Function to load users from CSV
def load_users_from_csv(file_path):
    users = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"].strip()] = row["password"].strip()  # Strip spaces
    return users


# Function to handle login logic
def login():
    user_data = load_users_from_csv("users.csv")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Login form
    if not st.session_state.logged_in:
        st.subheader("Please log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Debugging print statements
            st.write(f"Entered Username: '{username}'")
            st.write(f"Entered Password: '{password}'")
            
            # Strip spaces from input to handle any extra spaces
            username = username.strip()
            password = password.strip()

            if username in user_data:
                st.write(f"Stored password for {username}: '{user_data[username]}'")
            else:
                st.write("Username not found in database.")
            
            # Check if the credentials match
            if username in user_data and user_data[username] == password:
                st.session_state.logged_in = True
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password")
    else:
        st.success("You are logged in!")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.experimental_rerun()

# Main logic
if __name__ == "__main__":
    login()  # Run the login function

