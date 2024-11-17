import streamlit as st

# Title of the website
st.title('The Traveller Extra Trips')

# Text input for user to enter their name
name = st.text_input('Enter your name')

# Display a message based on the input
if name:
    st.write(f'Hello, {name}!')
else:
    st.write('Hello, World!')

# Display a slider
age = st.slider('How old are you?', 0, 100, 25)
st.write(f'You are {age} years old.')

# Display a chart (e.g., random data)
import numpy as np
chart_data = np.random.randn(20, 3)
st.line_chart(chart_data)


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
