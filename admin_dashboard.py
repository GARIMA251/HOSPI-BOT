import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import time

# Load the .env file
load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  # Fetch from env

REAL_TIME_LOGS = "real_time_logs.csv"

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

# Admin login check
if "admin_access" not in st.session_state or not st.session_state["admin_access"]:
    password = st.text_input("Enter Admin Password", type="password", key="admin_password")

    # Show error message only if the user has entered something
    if password:
        if password == ADMIN_PASSWORD:
            st.session_state["admin_access"] = True
            st.session_state["page"] = "admin_dashboard"  # Redirect to admin dashboard page
            st.success("You have access to the **Admin Dashboard**!")
        else:
            st.error("Incorrect password.")
else:
    if st.session_state["admin_access"]:
        st.title("Admin Dashboard")

        # Read the CSV file to get booking data only after login
        if os.path.exists(REAL_TIME_LOGS):
            df = pd.read_csv(REAL_TIME_LOGS)
            st.write("### Real-Time Logs")
            st.dataframe(df)  # Display the logs in a table format

            # Convert DataFrame to a list of dictionaries for easier processing
            logs = df.to_dict(orient='records')  # Convert to list of dictionaries

            # Calculate totals for analytics
            def calculate_totals(logs):
                room_bookings = sum(1 for log in logs if log.get("request_type") == "Room Booking")
                food_orders = sum(1 for log in logs if log.get("request_type") == "Food Order")
                spa_appointments = sum(1 for log in logs if log.get("request_type") == "Spa Appointment")
                return room_bookings, food_orders, spa_appointments

            # Displaying analytics
            room_bookings, food_orders, spa_appointments = calculate_totals(logs)

            st.markdown(f"**Total Room Bookings**: {room_bookings}")
            st.markdown(f"**Total Food Orders**: {food_orders}")
            st.markdown(f"**Total Spa Appointments**: {spa_appointments}")
            

        else:
            st.markdown("No bookings yet.")  # Message when there are no logs

        # Logout Button
        if st.button("Logout"):
            st.session_state["admin_access"] = False
            st.session_state["page"] = "assistant"  # Redirect back to the assistant page
            st.success("You have logged out successfully. Redirecting back to the assistant page...")
            time.sleep(2)  # Delay to show the logout message before redirecting
            st.experimental_rerun()  # Refresh the page to show the assistant page