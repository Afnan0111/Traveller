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


def haji_names(file_path):
    haji = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Only load id and name into the dictionary
            haji[row["id"].strip()] = {
                "name": row["name"].strip(),
                "payment": "",  # Default empty value for payment
                "bookedby": ""  # Default empty value for bookedby
            }
    return haji

# Function to update a user's booking status and write back to the CSV file
def update_booking(file_path, user_id, payment_status, booked_by):
    # Load the existing users' data
    haji = haji_names(file_path)
    
    # Check if the user exists
    if user_id in haji:
        # Update the user's payment and booked_by details
        haji[user_id]["payment"] = payment_status
        haji[user_id]["bookedby"] = booked_by
        
        # Now, write the updated data back to the file
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ["id", "name", "payment", "bookedby"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header
            writer.writeheader()

            # Write the updated user data
            for user_id, details in haji.items():
                writer.writerow({
                    "id": user_id,
                    "name": details["name"],
                    "payment": details["payment"],
                    "bookedby": details["bookedby"]
                })

        print(f"Booking updated for ID: {user_id}")
    else:
        print(f"User ID {user_id} not found.")


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
    user_id = st.text_input("Enter your ID")
    paid = st.radio("Has the trip been paid?", ("Yes", "No"))

    if st.button("Book Trip"):
        if user_id:
            # Load data from the haji CSV file
            haji_data = haji_names("haji.csv")
            
            # Check if the user exists in the haji file
            if user_id in haji_data:
                name = haji_data[user_id]  # Get the name corresponding to the user_id
                
                # Sanitize trip name and set the filename for booking
                sanitized_trip_name = trip_name.replace(" ", "_").lower()  # Replace spaces with underscores
                filename = f"{sanitized_trip_name}.csv"
                
                # Check if the file exists. If it doesn't, create it and write the header.
                file_exists = os.path.exists(filename)
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow([ "name", "user_id", "paid", "booked_by"])  # Write header for new file
                    # Save the booking details
                    writer.writerow([ name, user_id, paid,booked_by])
                
                st.success(f"Booking confirmed for {name} ({user_id}) on {trip_name}!")
            else:
                st.error("User ID not found in the haji file.")
        else:
            st.error("Please provide your ID.")

# Main logic
if __name__ == "__main__":
    login()  # Run the login function
    if st.session_state.logged_in:
        show_trips()  # Show trips if logged in
