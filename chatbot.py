from difflib import get_close_matches
from dotenv import load_dotenv
load_dotenv()
import os
import time
import re
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- INTENT MATCHING ---
def matches_intent(user_input, keywords, cutoff=0.8):
    words = user_input.lower().split()
    return any(get_close_matches(word, keywords, cutoff=cutoff) for word in words)

def is_hindi(text):
    return bool(re.search("[\u0900-\u097F]", text))

# --- RULE-BASED FALLBACK LOGIC ---
def rule_based_response(user_input):
    user_input = user_input.lower().strip()
    followups = ["yes", "okay", "please do", "book", "show me", "sure", "yep", "go ahead", "confirm", "do it", "sounds good"]

    if st.session_state.get("last_intent") == "menu":
        if "north" in user_input:
            st.session_state["last_subintent"] = "north"
            return rule_based_response("yes")  # simulate confirmation
        elif "south" in user_input:
            st.session_state["last_subintent"] = "south"
            return rule_based_response("yes")
        elif "continental" in user_input:
            st.session_state["last_subintent"] = "continental"
            return rule_based_response("yes")
        
        # 💆 Spa subintent follow-up handling
    if st.session_state.get("last_intent") == "spa":
        if "swedish" in user_input:
            st.session_state["last_subintent"] = "swedish"
            return "💆 Swedish massage selected. Shall I confirm your spa slot?"
        elif "deep" in user_input or "tissue" in user_input:
            st.session_state["last_subintent"] = "deep_tissue"
            return "💆 Deep Tissue massage chosen. Shall I go ahead and book your spa appointment?"
        elif "ayurvedic" in user_input:
            st.session_state["last_subintent"] = "ayurvedic"
            return "💆 Ayurvedic therapy selected. Would you like me to confirm your booking?"
    
    if st.session_state.get("last_intent") == "support":
        if "laundry" in user_input:
            st.session_state["last_subintent"] = "laundry"
            return rule_based_response("yes")
        elif "taxi" in user_input or "cab" in user_input:
            st.session_state["last_subintent"] = "taxi"
            return rule_based_response("yes")
        elif "wake" in user_input or "alarm" in user_input:
            st.session_state["last_subintent"] = "alarm"
            return "⏰ What time shall I set the wake-up call for?"
    
    if st.session_state.get("last_intent") == "children":
        if "babysitter" in user_input:
            st.session_state["last_subintent"] = "babysitter"
            return rule_based_response("yes")
    
    # 🛏️ Booking Sub-intent Captures
    if st.session_state.get("last_intent") == "booking":
        text = user_input.lower()
        if re.search(r"\b(deluxe|budget|suite)\b", text):
            st.session_state["last_subintent"] = "room_type"
            st.session_state["latest_query"] = text
            return "🛌 Room type noted. Could you also share the check-in/check-out dates and city?"

        elif re.search(r"\b\d+\s*(guests|people|persons)\b", text):
            st.session_state["last_subintent"] = "guests"
            st.session_state["latest_query"] = text
            return "👥 Number of guests updated. What’s the city and travel dates?"

        elif re.search(r"\b(delhi|bangalore|mumbai|goa|pune|chennai|kolkata|hyderabad|jaipur)\b", text):
            st.session_state["last_subintent"] = "city"
            st.session_state["latest_query"] = text
            return "📍 Got the city. Could you now provide check-in and check-out dates?"

        elif re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)?\s*(july|august|september)\b", text):
            st.session_state["last_subintent"] = "dates"
            st.session_state["latest_query"] = text
            return "📅 Dates captured. I’ll just need the remaining details to confirm your booking."

    
    
    if any(fu in user_input for fu in followups):
        last_intent = st.session_state.get("last_intent")
        last_subintent = st.session_state.get("last_subintent")

        def clear_state():
            st.session_state["last_intent"] = None
            st.session_state["last_subintent"] = None
            st.session_state["latest_query"] = None

        if last_intent == "spa":
            therapy = st.session_state.get("last_subintent", "massage")
            clear_state()
            return f"✅ {therapy.replace('_', ' ').title()} spa slot booked! A confirmation message will be shared with you shortly."

        elif last_intent == "menu":
            if last_subintent == "north":
                clear_state()
                return "🍛 North Indian Menu: Paneer, Dal Makhani, Naan, Jeera Rice."
            elif last_subintent == "continental":
                clear_state()
                return "🍝 Continental Menu: Pasta Alfredo, Grilled Veggies, Cheesecake."
            elif last_subintent == "south":
                clear_state()
                return "🍲 South Indian Menu: Dosa, Vada, Sambar, Chutney."
            clear_state()
            return (
                "🍽️ Here's today's complete menu:\n\n"
                "**Breakfast (7–10 AM)**: Idli-Sambar, Toast, Juice, Coffee\n"
                "**Lunch (12–3 PM)**: Paneer Butter Masala, Dal Fry, Rice, Salad\n"
                "**Dinner (7–10 PM)**: Butter Chicken, Jeera Rice, Naan, Gulab Jamun\n\n"
                "✅ Meals can be delivered to your room at no extra cost."
            )

        elif last_intent == "booking":
            text = st.session_state.get("latest_query", user_input)
            city_match = re.search(r"\b(delhi|bangalore|mumbai|goa|pune|chennai|kolkata|hyderabad|jaipur)\b", text)
            guests_match = re.search(r"\b(\d+)\s*(guests|people|persons)\b", text)
            room_type_match = re.search(r"\b(deluxe|budget|suite)\b", text)
            date_match = re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)?\s*(july|august|september)\b", text)

            city = city_match.group() if city_match else None
            guests = guests_match.group(1) if guests_match else None
            room_type = room_type_match.group() if room_type_match else None
            checkin = f"{date_match[0][0]} {date_match[0][1].capitalize()}" if len(date_match) >= 1 else None
            checkout = f"{date_match[1][0]} {date_match[1][1].capitalize()}" if len(date_match) >= 2 else None

            missing = []
            if not city: missing.append("📍 city")
            if not checkin or not checkout: missing.append("📅 check-in/out dates")
            if not guests: missing.append("👥 number of guests")
            if not room_type: missing.append("🛌 room type")

            if missing:
                return (
                    f"📋 I still need a few details to complete your booking:\n- " +
                    "\n- ".join(missing) +
                    "\n\nPlease share them so I can proceed."
                )
            else:
                clear_state()
                return (
                    f"✅ Room booked successfully!\n\n"
                    f"🛏️ *{room_type.capitalize()} Room*\n"
                    f"📍 *{city.title()}*\n"
                    f"📅 *{checkin} to {checkout}*\n"
                    f"👥 *{guests} guests*\n\n"
                    "📩 Confirmation sent to your registered number."
                )

        elif last_intent == "support":
            if last_subintent == "laundry":
                clear_state()
                return "🧺 Laundry will be picked up from your room between 9 AM – 7 PM."
            elif last_subintent == "taxi":
                clear_state()
                return "🚕 Taxi service booked. Would you like airport drop or local sightseeing?"
            elif last_subintent == "alarm":
                clear_state()
                return "⏰ Wake-up call scheduled. What time should I set it for?"
            clear_state()
            return (
                "✅ 24×7 support activated! You can now request:\n"
                "- 🧹 Housekeeping\n"
                "- 🚕 Cab booking\n"
                "- 🍲 Food orders\n"
                "- 🧺 Laundry\n\n"
                "What do you need right now?"
            )

        elif last_intent == "children":
            if last_subintent == "babysitter" or "babysitter" in user_input:
                clear_state()
                return "👶 Babysitter arranged for the evening. Confirmation on the way!"
            else:
                st.session_state["last_subintent"] = "babysitter"
                return "👶 Crib and toddler meals will be arranged. Would you like a babysitter too?"

        elif last_intent == "sightseeing":
            clear_state()
            return "🚗 Sightseeing tour booked! We’ll share the itinerary details shortly."

        elif last_intent == "honeymoon":
            clear_state()
            return "💖 Honeymoon package confirmed! Special arrangements await your arrival."

    if any(kw in user_input for kw in ["spa", "massage"]):
        st.session_state["last_intent"] = "spa"
        st.session_state["last_subintent"] = "offered"
        return (
            "💆 Our spa is open 10 AM – 6 PM.\n"
            "Swedish, Deep Tissue & Ayurvedic therapies available.\n"
            "Would you like to book a slot?"
        )

    if any(kw in user_input for kw in ["room", "book", "stay"]):
        st.session_state["last_intent"] = "booking"
        st.session_state["last_subintent"] = "start"
        return (
            "🛏️ Let's book your room.\n\n"
            "**Please share:**\n"
            "• 📍 City\n"
            "• 📅 Dates (Check-in/Check-out)\n"
            "• 👥 Guests\n"
            "• 🛌 Room type (Deluxe/Budget/Suite)"
        )

    if any(kw in user_input for kw in ["menu", "breakfast", "lunch", "dinner", "food"]):
        st.session_state["last_intent"] = "menu"
        if "north" in user_input:
            st.session_state["last_subintent"] = "north"
        elif "continental" in user_input:
            st.session_state["last_subintent"] = "continental"
        elif "south" in user_input:
            st.session_state["last_subintent"] = "south"
        else:
            st.session_state["last_subintent"] = "general"
        return (
            "📜 We serve:\n"
            "- 🍛 North Indian\n"
            "- 🍝 Continental\n"
            "- 🍲 South Indian\n\n"
            "Would you like to see today's full menu?"
        )

    if any(kw in user_input for kw in ["child", "baby", "toddler", "babysitter"]):
        st.session_state["last_intent"] = "children"
        st.session_state["last_subintent"] = "general"
        return (
            "🧸 We offer kids’ meals, cribs, high chairs, and babysitting.\n"
            "Would you like help planning a toddler-friendly stay?"
        )

    if any(kw in user_input for kw in ["sightseeing", "tour", "visit", "places"]):
        st.session_state["last_intent"] = "sightseeing"
        st.session_state["last_subintent"] = "heritage"
        return (
            "🗺️ We offer:\n"
            "- Delhi Darshan\n"
            "- Full-day heritage tour\n"
            "- Self-drive options\n\n"
            "Would you like me to book one?"
        )

    if any(kw in user_input for kw in ["honeymoon", "couple", "romantic"]):
        st.session_state["last_intent"] = "honeymoon"
        st.session_state["last_subintent"] = "package"
        return (
            "💖 We offer romantic suites, candlelight dinners & spa packages.\n"
            "Would you like to book the honeymoon package?"
        )

    if any(kw in user_input for kw in ["laundry", "wash", "clothes"]):
        st.session_state["last_intent"] = "support"
        st.session_state["last_subintent"] = "laundry"
        return "🧺 Laundry service runs 9 AM–7 PM. Should we send someone now?"

    if any(kw in user_input for kw in ["taxi", "cab"]):
        st.session_state["last_intent"] = "support"
        st.session_state["last_subintent"] = "taxi"
        return "🚕 Where do you need the taxi? (Airport/local)"

    if any(kw in user_input for kw in ["wake", "alarm"]):
        st.session_state["last_intent"] = "support"
        st.session_state["last_subintent"] = "alarm"
        return "⏰ What time shall I set the wake-up call for?"

    if any(kw in user_input for kw in ["help", "support", "assistance"]):
        st.session_state["last_intent"] = "support"
        return (
            "🧑‍💼 I’m here 24×7 to help with housekeeping, food, cabs, and more.\n"
            "What do you need assistance with?"
        )

    return "🤖 I'm sorry, I couldn't understand that clearly. Could you please rephrase or let me know which hotel service you need help with?"
def get_response(user_input):
    try:
        # Track the time taken to call the API
        start_time = time.time()
        st.session_state["latest_query"] = user_input
        is_hindi_query = is_hindi(user_input)
        language_note = "Please respond in Hindi or Hinglish politely." if is_hindi_query else "Respond in English politely."

        # Construct the prompt for Gemini
        prompt = (
            "You are AI Chieftain, a professional hotel concierge in India.\n"
            "Handle one query at a time. Services include:\n"
            "- 🛏️ Room bookings\n"
            "- 🍽️ Food menus\n"
            "- 💆 Spa\n"
            "- 🕐 Check-in/Check-out\n"
            "- 🗺️ Sightseeing\n"
            "- 👶 Kids/family\n"
            "- 💖 Honeymoon\n"
            "- 🚖 Taxi/laundry/wake-up calls\n"
            "- 🧑‍💼 24×7 concierge support\n\n"
            f"Guest Query: {user_input}\n"
            f"Previous Intent: {st.session_state.get('last_intent')}\n"
            f"Previous Subintent: {st.session_state.get('last_subintent')}\n"
            f"{language_note}\n\n"
            "Respond only to hotel-related topics. If unclear, ask clarifying questions. No small talk."
        )

        with st.spinner("HOSPI is preparing your response..."):
            # Call Gemini model to generate content
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            response = gemini_model.generate_content(prompt) 

        # Process response
        if hasattr(response, "parts") and response.parts:
            reply = response.parts[0].text.strip()
        else:
            raise ValueError("Gemini response parts missing or empty.")
        
        # Check if the response is empty or failed
        if not reply:
            raise ValueError("Gemini returned an empty string.")

        elapsed_time = time.time() - start_time

        # Return the reply from Gemini
        st.session_state["last_fallback"] = False
        return reply

    except Exception as e:
        # Handle failure and provide fallback logic
        st.write(f"Error encountered: {str(e)}")
        return rule_based_response(user_input)  # Fallback logic if Gemini fails
