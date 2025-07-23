# HOSPI - Your Virtual Hotel Assistant✨

## Project Overview
HOSPI is an intelligent AI-powered chatbot designed to function as a 24/7 virtual concierge for hotels. Using Streamlit and powered by Google Gemini, HOSPI aims to enhance the guest experience by providing instant assistance across numerous hotel services, including room bookings, food orders, spa appointments, and local sightseeing information. 

The user can now **select a particular hotel**, and the chatbot will provide assistance and information tailored to that hotel only, ensuring a more personalized and context-aware experience.

## Key Features:
HOSPI offers a diverse array of services tailored to guest needs:
- 🛏️ **Room Bookings**: Facilitates booking various room types (Deluxe, Budget, Suite) based on city, dates, and number of guests.
- 🍽️ **Food Menus**: Provides detailed menus for North Indian, Continental, and South Indian cuisines, with full-day options.
- 💆 **Spa Services**: Informs about spa timings and available therapies (Swedish, Deep Tissue, Ayurvedic), and assists with booking.
- 🧺 **Laundry Services**: Arranges laundry pickup.
- 🚕 **Taxi & Cab Bookings**: Helps in booking taxis for airport transfers or local sightseeing.
- ⏰ **Wake-up Calls**: Schedules wake-up calls.
- 👶 **Kids & Family Services**: Offers information for cribs, toddler meals, and babysitting.
- 🗺️ **Sightseeing & Tours**: Provides details on local tours and assists with bookings.
- 💖 **Honeymoon Packages**: Informs about special romantic arrangements including suites and spa options.
- 🧑‍💼 **24x7 Concierge Support**: Provides assistance for hotel queries.
- 🗣️ **Multilingual Support (Hinglish/Hindi)**: Capable of understanding and responding in English and Hinglish/Hindi.
- 🎙️ **Speech-to-Text Input**: Allows interaction via voice commands (local environment).
- 🔊 **Text-to-Speech Output**: Reads out responses (local environment).
- 👍👎 **Feedback Mechanism**: Guests can give feedback to improve service quality.

## Technologies Used:
- **Python**: Core programming language.
- **Streamlit**: For the interactive web interface.
- **Google Gemini API**: The AI model driving HOSPI's conversation.
- **speech_recognition**: Converts spoken input to text.
- **pyttsx3**: Converts text responses to speech.
- **python-dotenv**: For securely loading environment variables.
- **qrcode**: For generating QR codes.
- **pyaudio**: Required for microphone access in speech_recognition.

## App Structure:
### Files Overview:
- **app.py**: Main Streamlit application that handles user interface and service interactions. **New Update**: Users are now able to **select a particular hotel** from a dropdown menu, and HOSPI will provide assistance specific to that hotel.
- **chatbot.py**: Contains the main logic for handling conversational AI, integrates with the Google Gemini API, and manages user queries.
- **requirements.txt**: Lists all required Python libraries for the project.
- **Hotel_Logo.png**: Logo used within the application interface.
- **.env**: Contains sensitive configuration information like the API key (not to be shared).
- **.gitignore**: Specifies files/directories to ignore in git, such as the .env file.
- **admin_dashboard.py**: Allows hotel administrators to manage and update room bookings, dining bookings, spa services, and user feedback. Requires admin authentication via a password to access.

## Admin Dashboard Access:
### Overview:
The Admin Dashboard in HOSPI is designed for hotel administrators to monitor bookings, manage guest feedback, and view analytics. It enables administrators to:
- View Active Room, Spa, and Dining Bookings: Display real-time information on bookings, including the ability to update booking statuses.
- Monitor User Feedback: View guest feedback (thumbs up/down) and delete specific feedback.
- View Analytics: Provides insights on total bookings and feedback counts.

### Accessing the Admin Dashboard:
- **Login**: The admin dashboard is password-protected. After entering the correct password, the admin will have access to the dashboard.
- **Password**: The admin password is securely loaded from the .env file.
  
### Navigation:
- From the main screen, once the admin enters the password, they can click the **Go to Admin Dashboard** button in the sidebar.
- This will redirect them to the **Admin Dashboard** page, where they can view the data and perform administrative tasks.

### Admin Dashboard Features:
- **Active Room Bookings**: View and update the status of room bookings (Pending, Confirmed, Cancelled).
- **Active Spa Bookings**: View and update spa booking statuses.
- **Active Dining Bookings**: View and update dining booking statuses.
- **Feedback Management**: Admin can delete specific guest feedback.
- **Analytics**: Shows counts for room bookings, spa bookings, dining bookings, and feedback.

### Admin Dashboard Logging:
- **Real-time Booking Logs**: Every booking made by a guest (room, food, spa) is logged into the system and displayed on the Admin Dashboard. Admins can view details of these bookings in real-time and track analytics for room, spa, and dining services.

## Demo Video
[Watch HOSPI in Action!]

## Future Enhancements:
If we had more time, we would pursue the following enhancements:
- **Real-time Availability**: Integrate with hotel backend for live availability of rooms and services.
- **Payment Gateway Integration**: Enable direct bookings and payment processing within the chat.
- **Personalized Recommendations**: Use user history to suggest tailored services or attractions.
- **Multi-language Support**: Expand support to more international languages.
- **Advanced Context Management**: Enhance the bot's ability to handle complex conversations.

## License
This project is licensed under the MIT License - see the LICENSE file for details.