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
    
    # Input fields for booking
    name = st.text_input("Enter your full name")
    user_id = st.text_input("Enter your ID")
    paid = st.radio("Has the trip been paid?", ("Yes", "No"))

    if st.button("Book Trip"):
        if name and user_id:
            sanitized_trip_name = trip_name.replace(" ", "_").lower()  # Replace spaces with underscores
            filename = f"{sanitized_trip_name}.csv"
            
            # Check if the file exists. If it doesn't, create it and write the header.
            file_exists = os.path.exists(filename)
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["trip_name", "name", "user_id", "paid"])  # Write header for new file
                # Save the booking details
                writer.writerow([trip_name, name, user_id, paid])
            st.success(f"Booking confirmed for {name} on {trip_name}!")
        else:
            st.error("Please provide all the required details.")

# Main logic
if __name__ == "__main__":
    login()  # Run the login function
    if st.session_state.logged_in:
        show_trips()  # Show trips if logged in
