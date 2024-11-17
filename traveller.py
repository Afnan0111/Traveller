import streamlit as st
import csv
import os

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

def haji_names(file_path):
    haji = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Only load id and name into the dictionary
            haji[row["id"].strip()] = row["name"].strip()
    return haji

# Function to handle login logic
def login():
    user_data = load_users_from_csv("users.csv")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Please log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        username = username.strip()
        password = password.strip()

        if username in user_data:
            if user_data[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username  # Save the logged-in username in session state
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid password.")
        else:
            st.error("Username not found in database.")
    else:
        st.success(f"Welcome back, {st.session_state.username}!")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.username = None
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
        {"name": "Extra Umrah 1", "price": "150"},
        {"name": "Extra Umrah 2", "price": "150"},
        {"name": "Hijama", "price": "150"},
    ]

    st.subheader("Available Trips")
    for trip in trips:
        if st.button(f"{trip['name']}"):
            st.write(f"Price: {trip['price']}")
            book_trip(trip['name'])

def book_trip(trip_name):
    st.subheader(f"Booking for {trip_name}")
    
    user_id = st.text_input("Enter your ID")
    paid = st.radio("Has the trip been paid?", ("Yes", "No"))

    if st.button("Book Trip"):
        if user_id:
            # Load data from the haji CSV file
            haji_data = haji_names("haji.csv")

            if user_id in haji_data:
                name = haji_data[user_id]  # Get the name corresponding to the user_id
                booked_by = st.session_state.get('username', 'Unknown')  # Use logged-in username

                sanitized_trip_name = trip_name.replace(" ", "_").lower()  # Replace spaces with underscores
                filename = f"{sanitized_trip_name}.csv"

                # Check if the file exists
                file_exists = os.path.exists(filename)
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["name", "user_id", "paid", "booked_by"])  # Write header for new file
                    # Save the booking details
                    writer.writerow([name, user_id, paid, booked_by])

                st.success(f"Booking confirmed for {name} ({user_id}) on {trip_name}!")
            else:
                st.error("User ID not found in the haji file.")
        else:
            st.error("Please provide your ID.")


if __name__ == "__main__":
    login()  # Run the login function
    if st.session_state.logged_in:
        show_trips()  # Show trips if logged in
