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
        
        # Strip spaces from input to handle any extra spaces
        username = username.strip()
        password = password.strip()

        if username in user_data:
            # Check if the credentials match
            if user_data[username] == password:
                st.session_state.logged_in = True
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid password.")
        else:
            st.error("Username not found in database.")
    else:
        st.success("You are logged in!")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.experimental_rerun()

def show_trips():
    trips = [
        {"name": "Badr", "price": "250"},
        {"name": "Jeddah", "price": "150"},
        {"name": "Taif", "price": "200"},
        {"name": "Haibar", "price": "350"},
        {"name": "Zam Zam Factory", "price": "100"},
        {"name": "Kiswa Factory", "price": "100"},
        {"name": "Jinni Wadeeah", "price": "100"},
        {"name": "Extra Umrah", "price": "150"},
        {"name": "Hijama", "price": "150"},
    ]

    # Display the list of trips
    st.subheader("Available Trips")
    for trip in trips:
        if st.button(f"{trip['name']}"):
            st.write(f"Price: {trip['price']}")

# Main logic
if __name__ == "__main__":
    login()  # Run the login function
    if st.session_state.logged_in:
        show_trips()  # Show trips if logged in
