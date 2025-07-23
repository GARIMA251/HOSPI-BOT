import pandas as pd  
import streamlit as st
import os
import qrcode
from io import BytesIO
import base64
import time
from chatbot import get_response
import re
from chatbot import is_hindi
from datetime import datetime
import csv

LOG_FILE_PATH = 'real_time_logs.csv'

# Check if running on Streamlit Cloud
IS_CLOUD = os.getenv("STREAMLIT_SERVER_RUN", "").lower() == "true"

# Safe import + init for speech recognition
sr = None
pyttsx3 = None
engine = None

if not IS_CLOUD:
    try:
        import speech_recognition as sr
        import pyttsx3
        engine = pyttsx3.init()
    except Exception as e:
        st.warning(f"Speech libraries not available locally: {e}")

# Set page config
st.set_page_config(page_title="HOSPI – Hotel Bot", layout="centered")

# Title with some extra space below it
st.markdown("<h1 style='text-align:center; color: black;'>HOSPI - Your Virtual Hotel Assistant</h1>", unsafe_allow_html=True)
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Increased gap here

# Function to remove emojis for TTS only
def remove_emojis_for_tts(text):
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff"
        "\u200d\u2640-\u2642\u25aa\u25ab\u25fe\u2b50"
        "\ufe0f\u203c\u2049\u2122\u2139\ufe0f\U0001f004-\U0001f0cf"
        "\U0001f170-\U0001f251\U0001f300-\U0001f5ff\U0001f600-\U0001f64f"
        "\U0001f680-\U0001f6ff\U0001f700-\U0001f77f\U0001f780-\U0001f7ff"
        "\U0001f800-\U0001f8ff\U0001f900-\U0001f9ff\U0001fa00-\U0001fa6f"
        "\U0001fa70-\U0001faff\U0001fb00-\U0001fbff\U0001fc00-\U0001fcff"
        "\U0001fd00-\U0001fdff\U0001fe00-\U0001feff\U0001ff00-\U0001ffff]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r"", text)


def log_user_request(request_type, details, hotel_name):
    """Logs user requests like room booking, food orders, etc."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "request_type": request_type,
        "hotel_name": hotel_name,  
        "details": details
    }


    if os.path.exists(LOG_FILE_PATH):
        df = pd.read_csv(LOG_FILE_PATH)
        # Convert the log_entry dictionary to a DataFrame
        log_entry_df = pd.DataFrame([log_entry])
        # Use pd.concat to add the new entry to the existing DataFrame
        df = pd.concat([df, log_entry_df], ignore_index=True)
    else:
        df = pd.DataFrame([log_entry])

    # Save the DataFrame back to CSV
    df.to_csv(LOG_FILE_PATH, index=False)


    # Store log entries in session state for display in Streamlit
    if "real_time_logs" not in st.session_state:
        st.session_state["real_time_logs"] = []
    st.session_state["real_time_logs"].append(log_entry)

# Initialize session state for selected_hotel if not already set
if "selected_hotel" not in st.session_state:
    st.session_state["selected_hotel"] = None

# Hotel selection widget
selected_hotel = st.selectbox(
    "Select Your Hotel",
    ["Taj Palace", "Radisson Blu", "Leela Palace"],  # List of available hotels
    key="selected_hotel"
)

if selected_hotel and st.session_state.selected_hotel != selected_hotel:
    st.session_state.selected_hotel = selected_hotel

# Display the selected hotel or prompt for selection
if st.session_state.selected_hotel:
    st.write(f"Hotel selected: {st.session_state.selected_hotel}")
else:
    st.write("Please select a hotel to proceed.")

if "bookings" not in st.session_state:
    st.session_state["bookings"] = []
if "spa_bookings" not in st.session_state:
    st.session_state["spa_bookings"] = []
if "dining_bookings" not in st.session_state:
    st.session_state["dining_bookings"] = []
if "feedback" not in st.session_state:
    st.session_state["feedback"] = []
if "admin_access" not in st.session_state:
    st.session_state["admin_access"] = False

# Handle Room Booking
if 'room' in st.session_state.get("user_input", "").lower() and not st.session_state.get('room_booked', False):
    service_type = "Room Booking"
    with st.form(key=f"{service_type}_form"): 
        st.subheader(f"Book {service_type}")

        room_type = st.selectbox("Select Room Type", ["Presidential Suite", "Deluxe Room", "Standard Room"])
        check_in_date = st.date_input("Check-in Date", min_value=datetime.today())
        check_out_date = st.date_input("Check-out Date", min_value=datetime.today())

        submit_button = st.form_submit_button(label="Book Now")
        if submit_button:
            if not room_type or not check_in_date or not check_out_date:
                st.error("Please fill in all details for room booking.")
            else:
                log_user_request(service_type, f"Room Type: {room_type}, Check-in: {check_in_date}, Check-out: {check_out_date}, Hotel: {st.session_state.selected_hotel}", st.session_state.selected_hotel)
                st.session_state.chat_history.append(("bot", f"Your {room_type} has been reserved."))
                st.session_state.room_booked = True

# Handle Food Order
if 'food' in st.session_state.get("user_input", "").lower() and not st.session_state.get('food_booked', False):
    service_type = "Food Order"
    with st.form(key=f"{service_type}_form"): 
        st.subheader(f"Book {service_type}")

        food_type = st.selectbox("Select Food Type", ["Breakfast", "Lunch", "Dinner"])
        special_requests = st.text_input("Special Requests (e.g., vegetarian, allergies)")

        submit_button = st.form_submit_button(label="Place Order")
        if submit_button:
            if not food_type:
                st.error("Please select the food type.")
            else:
                log_user_request(service_type, f"Food Type: {food_type}, Special Requests: {special_requests}, Hotel: {st.session_state.selected_hotel}", st.session_state.selected_hotel)
                st.session_state.chat_history.append(("bot", f"Your {food_type} order has been placed."))
                st.session_state.food_booked = True

# Handle Spa Appointment
if 'spa' in st.session_state.get("user_input", "").lower() and not st.session_state.get('spa_booked', False):
    service_type = "Spa Appointment"
    with st.form(key=f"{service_type}_form"): 
        st.subheader(f"Book {service_type}")

        spa_service = st.selectbox("Select Spa Service", ["Massage", "Facial", "Pedicure", "Manicure"])
        service_time = st.time_input("Preferred Time for Spa Service")

        submit_button = st.form_submit_button(label="Book Spa Appointment")
        if submit_button:
            if not spa_service or not service_time:
                st.error("Please fill in all details for spa appointment.")
            else:
                log_user_request(service_type, f"Spa Service: {spa_service}, Time: {service_time}, Hotel: {st.session_state.selected_hotel}", st.session_state.selected_hotel)
                st.session_state.chat_history.append(("bot", f"Your {spa_service} appointment has been booked at {service_time}."))
                st.session_state.spa_booked = True

# 🎤 Speech-to-Text function
def get_speech_input():
    if sr is None:
        st.warning("🎙️ Speech input not supported on Streamlit Cloud.")
        return ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=15)  
    try:
        result = r.recognize_google(audio)
        st.session_state.typed_input = result  
        return result
    except sr.UnknownValueError:
        return "🤖 Sorry, I didn't catch that."
    except sr.RequestError:
        return "⚠️ Speech recognition service error."



# QR Code Generator
def generate_qr_code(url: str):
    qr = qrcode.QRCode(version=1, box_size=8, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/png;base64,{base64_img}" alt="QR Code" style="width:200px;"/>'

# Custom styles for the app
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://i.pinimg.com/1200x/11/c2/15/11c215bff93a0b97a6750582fea81e62.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 16px;
    }
    .user-message {
        background-color: #ffffff;
        color: black;
    }
    .bot-message {
        background-color: #f9f9f9;
        color: black;
    }
    .feedback-row {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 6px;
        margin-bottom: 10px;
    }
    .feedback-confirmation {
        font-size: 15px;
        font-weight: bold;
        background-color: rgba(240, 240, 240, 0.9);
        padding: 6px 12px;
        border-radius: 8px;
        color: black;
    }
    .input-mic-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        max-width: 700px;
        margin: 20px auto 15px;
    }
    .input-mic-container input {
        flex: 1;
        padding: 14px 18px;
        font-size: 16px;
        border-radius: 16px;
        border: none;
        height: 52px;
        background-color: white;
    }
    .input-mic-container button {
        height: 52px;
        width: 52px;
        background-color:white;
        color: white;
        font-size: 22px;
        border: none;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .example-queries {
        margin-bottom: 30px;  /* adds space below Tips */
    }
    .qr-code-container {
        margin-top: 20px;  /* adds space above QR code */
    }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("Hotel_Logo.png", width=200)
    st.title("HOSPI - Your Hotel Assistant 🧠")
    st.markdown("Welcome to your smart hotel assistant!")
    st.markdown("🕔 24x7 Service | 🛎️ Rooms: Deluxe, Budget | 📍 Pan-India")
    st.markdown("---")
    # Provide an option for admin to enter the dashboard
    if st.sidebar.button("Go to Admin Dashboard"):
        os.system("streamlit run admin_dashboard.py")


    # QR Code for easy mobile access
    deployed_url = "https://your-streamlit-app-url.streamlit.app" 
    st.markdown("### 📱 Scan to open HOSPI on your device:")
    st.markdown(generate_qr_code(deployed_url), unsafe_allow_html=True)

    if st.button("💡 Show Tips", key="tips_btn"):
        st.session_state.show_faq = not st.session_state.show_faq

    if st.session_state.get("show_faq", False):
        st.markdown("""
        <div class="example-queries">
            <p><strong>Try asking:</strong></p>
            <ul>
                <li>👉 Book a deluxe room 🛎️</li>
                <li>👉 What's for dinner tonight? 🍽️</li>
                <li>👉 Check-out time? 🕔</li>
                <li>👉 Reserve a spa appointment 💆‍♀️</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Non-admin interface content
for key, val in {
    "chat_history": [],
    "feedback_log": [],
    "typed_input": "",
    "user_input": "",
    "input_mode": None,
    "mic_triggered": False,
    "show_faq": False,
    "trigger_response": False,
    "last_intent": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat History and Service Handling
for idx, (sender, message) in enumerate(st.session_state.chat_history):
    msg_class = "user-message" if sender == "user" else "bot-message"
    name = "You" if sender == "user" else "HOSPI"
    st.markdown(f"<div class='chat-bubble {msg_class}'><b>{name}:</b> {message}</div>", unsafe_allow_html=True)

    # Dynamic service handling based on user input
    if sender == "bot" and 'book' in message.lower():
        if 'spa' in message.lower() and not st.session_state.get('spa_booked', False):  # Check if spa has been booked
            service_type = "Spa Appointment"
            with st.form(key=f"{service_type}_{idx}_form"): 
                st.subheader(f"Book {service_type}")

                spa_service = st.selectbox("Select Spa Service", ["Massage", "Facial", "Pedicure", "Manicure"])
                service_time = st.time_input("Preferred Time for Spa Service")

                submit_button = st.form_submit_button(label="Book Spa Appointment")
                if submit_button:
                    if not spa_service or not service_time:
                        st.error("Please fill in all details for spa appointment.")
                    else:
                        # No log saving here for spa booking, it should be done in the admin dashboard
                        st.session_state.chat_history.append(("bot", f"Your {spa_service} appointment has been booked at {service_time}."))
                        st.session_state.spa_booked = True  # Set spa booking flag to True

    # --- Feedback Section ---
    if sender == "bot":
        up_key, down_key, read_key, confirm_key = f"👍_{idx}", f"👎_{idx}", f"🔊_{idx}", f"confirm_{idx}"
        st.markdown('<div class="feedback-row">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 2.7])

        with col1:
            if st.button("👍", key=up_key):
                st.session_state.feedback_log.append({"message": message, "feedback": "good"})
                st.session_state[confirm_key] = "Thanks for the 👍!"
    
        with col2:
            if st.button("👎", key=down_key):
                st.session_state.feedback_log.append({"message": message, "feedback": "bad"})
                st.session_state[confirm_key] = "We’ll work on improving!"
    
        with col3:
            if st.button("🔊", key=read_key):
                if engine is not None:
                # Strip emojis from the message before reading aloud
                    message_for_tts = remove_emojis_for_tts(message)
                    st.session_state[confirm_key] = "🔊 Reading aloud ....."
                    engine.say(message_for_tts)
                    engine.runAndWait()

        with col4:
            if confirm_key in st.session_state:
                st.markdown(f"<div class='feedback-confirmation'>{st.session_state[confirm_key]}</div>", unsafe_allow_html=True)
                time.sleep(4)
                del st.session_state[confirm_key]
        st.markdown('</div>', unsafe_allow_html=True)

# --- Input Handling ---
if "text_input_key" not in st.session_state:
    st.session_state["text_input_key"] = f"input_{time.time_ns()}"

# 🎤💬 Input Interface
st.markdown("""<div class="input-mic-container">""", unsafe_allow_html=True)
col1, col2 = st.columns([0.85, 0.15])
with col1:
    typed = st.text_input(
        "Type your message here",
        value=st.session_state.get("typed_input", ""),
        label_visibility="collapsed",
        key=st.session_state.text_input_key
    )
with col2:
    # === Disable mic button on Streamlit Cloud ===
    if IS_CLOUD:
        st.button("🎙️ (Mic disabled on Cloud)", disabled=True, help="Mic input not supported on Streamlit Cloud.")
        mic_clicked = False
    else:
        mic_clicked = st.button("🎙️", key="mic_btn", help="Speak your request")
st.markdown("""</div>""", unsafe_allow_html=True)

send_clicked = st.button("Send", key="send_btn", help="Click to send message")

# 📤 Handle Input (typed or mic)
if mic_clicked:
    st.session_state.input_mode = "mic"
    st.session_state.mic_triggered = False

if send_clicked and typed.strip():
    # Save the typed input to session state, whether from mic or keyboard
    st.session_state.user_input = typed.strip()
    st.session_state.input_mode = "text"
    st.session_state.trigger_response = True
    st.session_state.text_input_key = f"input_{time.time_ns()}"
    st.session_state.typed_input = typed.strip()  # Store the typed input to update the input box

# 🎙️ Handle Mic Input
if (
    st.session_state.get("input_mode") == "mic"
    and not st.session_state.get("mic_triggered", False)
):
    st.session_state.mic_triggered = True
    spoken_input = get_speech_input()  # Function to handle speech-to-text
    if spoken_input.strip():
        # Update the input with the spoken input
        st.session_state.typed_input = spoken_input  
        st.session_state.user_input = spoken_input  
        st.session_state.trigger_response = True
    st.session_state.input_mode = None

# 🤖 Process Bot Response
if st.session_state.get("trigger_response") and st.session_state.get("user_input", "").strip():
    user_input = st.session_state["user_input"].strip()

    with st.spinner("HOSPI is responding... Please wait."):
        hotel_name = st.session_state.get("selected_hotel")
        reply = get_response(user_input, hotel_name)
        time.sleep(0.5)
        
        if hotel_name:
            st.session_state.chat_history.append(("user", user_input))
            reply = get_response(user_input, hotel_name)
            st.session_state.chat_history.append(("bot", reply))
        else:
            st.session_state.chat_history.append(("bot", "🤖 Please select a hotel before proceeding."))

    # Clear input only after handling response
    st.session_state.typed_input = ""
    st.session_state.text_input_key = f"input_{time.time_ns()}"

    # Reset flags for next input
    st.session_state["user_input"] = ""
    st.session_state["trigger_response"] = False
    st.session_state["mic_triggered"] = False

