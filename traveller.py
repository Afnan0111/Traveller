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

# Function to load haji names and details from CSV
def haji_names(file_path):
    haji = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Only load id and name into the dictionary
            haji[row["id"].strip()] = row["name"].strip()

    except FileNotFoundError:
        st.error(f"{file_path} not found. Please make sure the file exists.")
    return haji

# Function to update booking status in a trip file
def update_booking(trip_name, user_id, user_name, payment_status):
    sanitized_trip_name = trip_name.replace(" ", "_").lower()  # Sanitize the trip name for the file
    filename = f"{sanitized_trip_name}.csv"
    
    # Check if file exists, if not create it and write headers
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["name", "user_id", "paid", "booked_by"])  # Write header for new file
        # Save the booking details
        writer.writerow([user_name, user_id, payment_status, user_name])  # Writing booking details

    st.success(f"Booking confirmed for {user_name} ({user_id}) on {trip_name}!")

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
        {"name": "Extra Umrah 1", "price": "150"},
        {"name": "Extra Umrah 2", "price": "150"},
        {"name": "Hijama", "price": "150"},
    ]

    # Display the list of trips
    st.subheader("Available Trips")
    for trip in trips:
        if st.button(f"{trip['name']}"):
            st.write(f"Price: {trip['price']}")
            book_trip(trip['name'])

def book_trip(trip_name):
    st.subheader(f"Booking for {trip_name}")
    
    # Input field for user ID
    user_id = st.text_input("Enter your Haji ID")
    paid = st.radio("Has the trip been paid?", ("Yes", "No"))

    if st.button("Book Trip"):
        if user_id:
            # Load data from the haji CSV file
            haji_data = haji_names("haji.csv")
            
            # Check if the user exists in the haji file
            if user_id in haji_data:
                user_name = haji_data[user_id]["name"]  # Get the name corresponding to the user_id
                payment_status = paid
                
                # Update the booking in the respective trip file
                update_booking(trip_name, user_id, user_name, payment_status)
            else:
                st.error(f"User ID {user_id} not found in the haji file.")
        else:
            st.error("Please provide your Haji ID.")

# Main logic
if __name__ == "__main__":
    login()  # Run the login function
    if st.session_state.logged_in:
        show_trips()  # Show trips if logged in
