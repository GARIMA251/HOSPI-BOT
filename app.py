import streamlit as st
import os
import qrcode
from io import BytesIO
import base64
import time
from chatbot import get_response



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

# Initialize session state variables if not present
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

# Sample data for testing
if not st.session_state["bookings"]:
    st.session_state["bookings"] = [{"Booking ID": 1, "Guest": "KARAN", "Room Type": "Deluxe", "Check-in": "2025-07-16", "Check-out": "2025-07-18", "Status": "Pending"}]
if not st.session_state["spa_bookings"]:
    st.session_state["spa_bookings"] = [{"Spa Booking ID": 1, "Guest": "ADITI", "Therapy Type": "Swedish Massage", "Date": "2025-07-17", "Time": "10:00 AM", "Status": "Pending"}]
if not st.session_state["dining_bookings"]:
    st.session_state["dining_bookings"] = [{"Dining Booking ID": 1, "Guest": "SUNNY", "Meal Type": "Dinner", "Date": "2025-07-18", "Time": "7:00 PM", "Status": "Pending"}]
if not st.session_state["feedback"]:
    st.session_state["feedback"] = [{"Booking ID": 1, "Feedback": "👍", "Date": "2025-07-16"}]

# 🎤 Speech-to-Text function
def get_speech_input():
    if sr is None:
        st.warning("🎙️ Speech input not supported on Streamlit Cloud.")
        return ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=5)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Speech recognition service error."

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

# Title
st.markdown("<h1 style='text-align:center; color: black;'>HOSPI - Your Virtual Hotel Assistant</h1>", unsafe_allow_html=True)

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

# 🧠 Chat History
for idx, (sender, message) in enumerate(st.session_state.chat_history):
    msg_class = "user-message" if sender == "user" else "bot-message"
    name = "You" if sender == "user" else "HOSPI"
    st.markdown(f"<div class='chat-bubble {msg_class}'><b>{name}:</b> {message}</div>", unsafe_allow_html=True)

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
                    st.session_state[confirm_key] = "🔊 Reading aloud ....."
                    engine.say(message)
                    engine.runAndWait()
                else:
                    st.info("🔊 Text-to-speech is disabled on Streamlit Cloud.")

        with col4:
            if confirm_key in st.session_state:
                st.markdown(f"<div class='feedback-confirmation'>{st.session_state[confirm_key]}</div>", unsafe_allow_html=True)
                time.sleep(4)
                del st.session_state[confirm_key]
        st.markdown('</div>', unsafe_allow_html=True)

if "text_input_key" not in st.session_state:
    st.session_state.text_input_key = f"input_{int(time.time())}"

# 🎤💬 Input Interface
st.markdown("""<div class="input-mic-container">""", unsafe_allow_html=True)
col1, col2 = st.columns([0.85, 0.15])
with col1:
    typed = st.text_input(
        "Type your message here",
        value="",
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
    st.session_state.user_input = typed.strip()
    st.session_state.input_mode = "text"
    st.session_state.trigger_response = True
    st.session_state.text_input_key = f"input_{time.time_ns()}"

# 🎙️ Handle Mic Input
if (
    st.session_state.get("input_mode") == "mic"
    and not st.session_state.get("mic_triggered", False)
):
    st.session_state.mic_triggered = True
    spoken_input = get_speech_input()
    if spoken_input.strip():
        st.session_state.user_input = spoken_input
        st.session_state.trigger_response = True
    st.session_state.input_mode = None

# 🤖 Process Bot Response
if st.session_state.get("trigger_response") and st.session_state.get("user_input", "").strip():
    user_message = st.session_state["user_input"]
    st.session_state.chat_history.append(("user", user_message))
    reply = get_response(user_message)
    st.session_state.chat_history.append(("bot", reply))
    st.session_state["user_input"] = ""
    st.session_state["trigger_response"] = False
    st.session_state["mic_triggered"] = False
