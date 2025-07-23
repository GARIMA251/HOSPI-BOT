from difflib import get_close_matches
from dotenv import load_dotenv
load_dotenv()
import os
import time
import re
import streamlit as st
import google.generativeai as genai
from hotel_data import get_hotel_data, hotel_data  # ✅ this line brings the data dict
import random

# Initialize the Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to check if the user input contains Hindi
def is_hindi(user_input):
    """Check if the input text contains Hindi characters (Unicode range for Devanagari)."""
    hindi_regex = re.compile('[\u0900-\u097F]+')
    return bool(hindi_regex.search(user_input))

# Fallback logic when Gemini is unavailable
def rule_based_response(user_input):
    """Fallback logic when Gemini is unavailable or cannot process the query."""
    user_input = user_input.lower().strip()
    followups = ["yes", "okay", "please do", "book", "show me", "sure", "yep", "go ahead", "confirm", "do it", "sounds good"]

    # Check if a hotel is already selected
    if st.session_state.get("last_intent") == "hotel":
        hotel_name = st.session_state.get("last_subintent")
        hotel_data = get_hotel_data(hotel_name)  # This will now use fuzzy matching

        if not hotel_data:
            return "🤖 Sorry, I couldn't find the details for that hotel."

        # If the query asks about the hotel (e.g., tell me about the hotel)
        if "about" in user_input or "tell me" in user_input:
            return get_hotel_info(hotel_data)
        
        # Handle rooms, facilities, or menu queries
        if "rooms" in user_input:
            return handle_room_query(hotel_data)
        elif "facilities" in user_input:
            return handle_facilities_query(hotel_data)
        elif "menu" in user_input:
            return handle_menu_query(hotel_data)

    return "🤖 I'm sorry, I couldn't understand that clearly. Could you please rephrase?"

# Main function to handle Gemini response generation
def get_response_from_gemini(user_input, hotel_name):
    """Generate response from Gemini model considering the selected hotel and session context."""

    user_input_clean = user_input.lower().strip()

    greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening"]

    if any(greet in user_input_clean for greet in greetings):
        hotel_display = hotel_name if hotel_name else "the hotel"
        return f"👋 Namaste! I'm HOSPI, your AI assistant at {hotel_display}. How can I help you today? 😊"


    hotel_data = get_hotel_data(hotel_name)
    if not hotel_data:
        return "🤖 Sorry, I couldn't find the details for that hotel."

    description = hotel_data.get('description', '')
    location = hotel_data.get('location', '')
    rooms = "\n".join([f"{room_name}: {room_info['description']}" for room_name, room_info in hotel_data.get('rooms', {}).items()])
    facilities = "\n".join([f"{k}: {v}" for k, v in hotel_data.get('facilities', {}).items()])
    menu = "\n".join([f"{meal.capitalize()}: {', '.join(items)}" for meal, items in hotel_data.get('menu', {}).items()])
    services = "\n".join(hotel_data.get('services', []))


    # prompt for Gemini
    prompt = (
        f"You are HOSPI, a hotel assistant AI for {hotel_name}.\n"
        f"Hotel Description: {description}\n"
        f"Location: {location}\n"
        f"Rooms: {rooms}\n"
        f"Facilities: {facilities}\n"
        f"Menu: {menu}\n"
        f"Services: {services}\n"
        f"Last Query: {st.session_state.get('last_query', '')}\n"
        f"Last Response: {st.session_state.get('last_response', '')}\n"
        f"User Input: {user_input}\n"
        "Instructions:\n"
        "- Respond in a friendly, warm, and concise tone.\n"
        "- Use emojis generously.\n"
        "- If the input is a greeting or start of conversation, start with a warm greeting including 'Namaste' and introduce yourself as the hotel assistant.\n"
        "- Only answer questions relevant to the hotel and its services.\n"
        "- If the current input is vague or incomplete, use the conversation context to infer what the user means.\n"
        "- If you can't infer, politely ask the user for clarification with examples.\n"
        "- Always keep responses concise, relevant to the hotel’s services, and human-like.\n"
    )

    try:
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        response = gemini_model.generate_content(prompt)

        if hasattr(response, "parts") and response.parts:
            reply = response.parts[0].text.strip()
            if not reply:
                return "🤖 I'm sorry, I couldn't generate a response for that query."

            st.session_state["last_query"] = user_input
            st.session_state["last_response"] = reply

            return reply

    except Exception as e:
        return f"⚠️ Gemini model error: {str(e)}"

    return "🤖 Gemini couldn't process your request right now."

# Handle room-related queries from the user
def handle_room_query(hotel_data):
    """Handle room-related queries from the user."""
    rooms = hotel_data.get("rooms", {})
    room_details = "\n".join([f"**{room_name}**: {room_info['description']}" for room_name, room_info in rooms.items()])
    return f"🏨 Room options:\n{room_details}"

# Handle facilities-related queries from the user
def handle_facilities_query(hotel_data):
    """Handle facilities-related queries from the user."""
    facilities = hotel_data.get("facilities", {})
    facility_details = "\n".join([f"**{facility_name}**: {facility_desc}" for facility_name, facility_desc in facilities.items()])
    return f"🛎️ Available facilities:\n{facility_details}"

# Handle menu-related queries from the user
def handle_menu_query(hotel_data):
    """Handle menu-related queries from the user."""
    menu = hotel_data.get("menu", {})
    menu_details = ""
    for meal, items in menu.items():
        menu_details += f"\n**{meal.capitalize()}**: {', '.join(items)}"
    return f"🍽️ Menu:\n{menu_details}"

# Main function to handle user input and decide the flow
def get_response(user_input, hotel_name):

    user_input_clean = user_input.lower().strip()

    hotel_data = get_hotel_data(hotel_name)  # Now uses fuzzy matching if needed
    if not hotel_data:
        return "🤖 Sorry, I couldn't find the details for that hotel."

    st.session_state["last_intent"] = "hotel"
    st.session_state["last_subintent"] = hotel_name

    # First try getting a response from Gemini
    gemini_response = get_response_from_gemini(user_input, hotel_name)
    
    # If Gemini doesn't provide a valid response, fallback to rule-based logic
    if "🤖 I'm sorry" in gemini_response:  # Check if Gemini failed to respond
        return rule_based_response(user_input)
    
    return gemini_response

# Get the basic information about the selected hotel
def get_hotel_data(hotel_name):
    # Try exact match first
    if hotel_name in hotel_data:
        return hotel_data[hotel_name]
    
    # Fuzzy match (allows for small typos or variations)
    match = get_close_matches(hotel_name, hotel_data.keys(), n=1, cutoff=0.6)  # Adjust cutoff as needed
    if match:
        return hotel_data[match[0]]
    
    return None
