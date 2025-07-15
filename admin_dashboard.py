import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")  # Fetch from env, use default if not set

# Initialize session state variables if not present
if "admin_access" not in st.session_state:
    st.session_state["admin_access"] = False  # Initially, admin access is False

if "page" not in st.session_state:
    st.session_state["page"] = "assistant"  # Default page is the assistant page

# Sidebar for navigation
with st.sidebar:
    st.image("Hotel_Logo.png", width=200)
    st.title("HOSPI - Your Virtual Hotel Assistant 🧠")
    st.markdown("### Welcome!")
    st.markdown("🕔 24x7 Service | 🛎️ Rooms: Deluxe, Budget | 📍 Pan-India")
    st.sidebar.markdown("---")

# === Admin Login ===
password = st.text_input("Enter Admin Password", type="password")

# Check if password is correct
if password == ADMIN_PASSWORD:
    st.session_state["admin_access"] = True  # Set admin access to True
    st.session_state["page"] = "admin_dashboard"  # Redirect to admin dashboard page
    st.success("You have access to the **Admin Dashboard**!")
else:
    if password and password != ADMIN_PASSWORD:
        st.error("Incorrect password. Please try again.")

# === Displaying Pages Based on Session State ===
if st.session_state["admin_access"]:
    # Admin Dashboard logic here
    if st.session_state["page"] == "admin_dashboard":
        st.title("Admin Dashboard")
        st.markdown("Here you can manage bookings, monitor feedback, and view analytics.")

        # Sample Data (You can replace this with actual dynamic data from your app)
        booking_data = [
            {"Booking ID": 1, "Guest": "John Doe", "Room Type": "Deluxe", "Check-in": "2025-07-16", "Check-out": "2025-07-18", "Status": "Confirmed"},
            {"Booking ID": 2, "Guest": "Alice Smith", "Room Type": "Budget", "Check-in": "2025-07-17", "Check-out": "2025-07-20", "Status": "Pending"},
            {"Booking ID": 3, "Guest": "Bob Lee", "Room Type": "Suite", "Check-in": "2025-07-18", "Check-out": "2025-07-22", "Status": "Confirmed"},
        ]

        feedback_data = [
            {"Booking ID": 1, "Feedback": "👍", "Message": "The room was fantastic!", "Date": "2025-07-16"},
            {"Booking ID": 2, "Feedback": "👎", "Message": "The food quality was poor.", "Date": "2025-07-17"},
            {"Booking ID": 3, "Feedback": "👍", "Message": "Excellent service!", "Date": "2025-07-18"},
        ]

        # Displaying bookings and feedback (as dataframes)
        st.header("📅 Active Bookings")
        st.dataframe(booking_data)

        st.header("📣 User Feedback")
        st.dataframe(feedback_data)

        # Analytics
        st.header("📊 Analytics")
        st.markdown(f"Total Bookings: {len(booking_data)}")
        st.markdown(f"Total Feedback: {len(feedback_data)}")

        # Provide an option to log out
        if st.button("Logout"):
            st.session_state["admin_access"] = False  # Reset access on logout
            st.session_state["page"] = "assistant"  # Reset to the normal assistant page

else:
    # If admin access isn't granted, show the assistant page
    if st.session_state["page"] == "assistant":
        st.markdown("Please log in to access the **Admin Dashboard**.")
        # Further assistant logic can be added here
