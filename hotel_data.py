from difflib import get_close_matches


hotel_data = {
    "Taj Palace": {
        "assistant_name": "HOSPI",
        "description": "Taj Palace, located in the heart of Delhi, is a luxurious 5-star hotel known for its impeccable service and world-class amenities. It offers a blend of traditional grandeur and modern comfort, making it the perfect destination for both business and leisure travelers.",
        "location": "Delhi",
        "rooms": {
            "Presidential Suite": {
                "description": "Luxurious suite with a king-sized bed, separate living room, and panoramic city views.",
                "amenities": ["Private balcony", "24/7 room service", "Premium linens", "Private concierge", "Jacuzzi", "High-speed internet"]
            },
            "Deluxe Room": {
                "description": "Spacious rooms with king/queen-sized beds and luxury bathroom amenities.",
                "amenities": ["Mini-bar", "Flat-screen TV", "In-room dining", "Tea/Coffee Maker"]
            },
            "Standard Room": {
                "description": "Affordable yet comfortable with all necessary amenities.",
                "amenities": ["Comfortable bedding", "Air conditioning", "Desk", "Room service"]
            }
        },
        "facilities": {
            "Wi-Fi": "Free high-speed internet access throughout the hotel.",
            "Pool": "Temperature-controlled pool surrounded by lush gardens, open from 7 AM to 9 PM.",
            "Fitness Center": "Fully equipped gym with cardio and weight machines.",
            "Spa": "Spa and wellness center offering Swedish, Deep Tissue, and Ayurvedic massages.",
            "Restaurant": "Multi-cuisine restaurant serving North Indian, South Indian, and Continental dishes."
        },
        "menu": {
            "Breakfast": ["Continental", "Indian", "Juices", "Smoothies"],
            "Lunch": ["Butter Chicken", "Tandoori", "Dal Makhani", "Naan"],
            "Dinner": ["Rogan Josh", "Lamb Shank", "Biriyani"]
        },
        "services": [
            "24/7 Room Service",
            "Concierge",
            "Airport Shuttle",
            "Laundry Service",
            "Currency Exchange",
            "Valet Parking",
            "Business Center",
            "Event Facilities"
        ],
        "bookings": {
            "room": [],
            "spa": [],
            "restaurant": [],
            "facilities": []
        }
    },

    "Radisson Blu": {
        "assistant_name": "HOSPI",
        "description": "Located in the bustling city of Mumbai, Radisson Blu offers a luxurious stay with modern amenities, breathtaking views, and unparalleled service. It is the perfect destination for business travelers and tourists alike.",
        "location": "Mumbai",
        "rooms": {
            "Royal Suite": {
                "description": "Ultra-modern suite with panoramic views of the city and sea, private butler service.",
                "amenities": ["King-sized bed", "Private balcony", "Marble bathroom", "Smart TV", "24/7 room service", "Minibar"]
            },
            "Executive Room": {
                "description": "Luxurious rooms with sea views, high-end amenities, and spacious workstations.",
                "amenities": ["Flat-screen TV", "Coffee maker", "Air-conditioning", "Premium bedding", "Mini-bar"]
            },
            "Superior Room": {
                "description": "Spacious rooms with all modern amenities, perfect for both business and leisure stays.",
                "amenities": ["Complimentary Wi-Fi", "Smart TV", "In-room safe", "Tea/Coffee maker", "Laundry services"]
            }
        },
        "facilities": {
            "Wi-Fi": "Free Wi-Fi throughout the hotel with high-speed internet.",
            "Pool": "Infinity pool with a scenic view of the city skyline.",
            "Spa": "A tranquil spa offering a range of massages, facials, and skin treatments.",
            "Restaurant": "Fine dining with international cuisine, featuring fresh seafood and classic Indian delicacies."
        },
        "menu": {
            "Breakfast": ["Pancakes", "Full English Breakfast", "Fresh Fruits", "Cereals"],
            "Lunch": ["Grilled Salmon", "Crispy Duck", "Vegetarian Tacos", "Mushroom Risotto"],
            "Dinner": ["Filet Mignon", "Lobster Thermidor", "Pasta Primavera"]
        },
        "services": [
            "24/7 Room Service",
            "Concierge",
            "Shuttle Service",
            "Laundry Service",
            "Business Center",
            "Event Planning",
            "Valet Parking",
            "Free Airport Pickup"
        ],
        "bookings": {
            "room": [],
            "spa": [],
            "restaurant": [],
            "facilities": []
        }
    },

    "The Leela Palace": {
        "assistant_name": "HOSPI",
        "description": "The Leela Palace in Bengaluru is a stunning blend of grandeur and elegance, offering a regal experience with a variety of luxurious rooms, fine dining options, and world-class facilities. The hotel promises unparalleled service and exquisite comfort.",
        "location": "Bengaluru",
        "rooms": {
            "Imperial Suite": {
                "description": "Elegantly designed suite with antique decor, private dining area, and marble bathrooms.",
                "amenities": ["King-size bed", "In-room jacuzzi", "Personal assistant", "Private gym", "Panoramic views"]
            },
            "Premier Room": {
                "description": "Spacious and modern room with floor-to-ceiling windows and luxury amenities.",
                "amenities": ["Smart TV", "In-room coffee machine", "24/7 room service", "High-speed internet", "Air-conditioning"]
            },
            "Classic Room": {
                "description": "Comfortable and affordable room with modern comforts for a pleasant stay.",
                "amenities": ["Comfortable bedding", "Desk", "Mini-bar", "Laundry service", "Tea/Coffee maker"]
            }
        },
        "facilities": {
            "Wi-Fi": "Unlimited high-speed Wi-Fi access throughout the property.",
            "Pool": "An outdoor infinity pool with stunning views of the city skyline.",
            "Fitness Center": "State-of-the-art fitness center with a variety of equipment and personal trainers.",
            "Restaurant": "Award-winning restaurant serving Indian and international cuisine.",
            "Spa": "Luxury spa with signature Ayurvedic and Aromatherapy treatments."
        },
        "menu": {
            "Breakfast": ["South Indian (Dosa, Idli, Sambar)", "Continental", "Pancakes", "Eggs Benedict"],
            "Lunch": ["Paneer Butter Masala", "Mutton Shank", "Kebabs", "Biryani"],
            "Dinner": ["Tandoori Lobster", "Mushroom Risotto", "Steak", "Chocolate Lava Cake"]
        },
        "services": [
            "24/7 Room Service",
            "Concierge",
            "Business Center",
            "Laundry Service",
            "Spa Services",
            "Private Tours",
            "Shuttle Services",
            "Valet Parking",
            "Wedding Services"
        ],
        "bookings": {
            "room": [],
            "spa": [],
            "restaurant": [],
            "facilities": []
        }
    }
}


def get_hotel_data(hotel_name):
    if hotel_name in hotel_data:
        return hotel_data.get(hotel_name)
    
       # Use fuzzy matching
    match = get_close_matches(hotel_name, hotel_data.keys(), n=1, cutoff=0.6)
    if match:
        return hotel_data[match[0]]
    
    return None

def book_room(hotel_name, room_type, guest_name, check_in, check_out):
    try:
        hotel = hotel_data.get(hotel_name)
        if not hotel:
            return f"❌ Hotel '{hotel_name}' not found."

        room = hotel["rooms"].get(room_type)
        if not room:
            return f"❌ Room type '{room_type}' not available in {hotel_name}."

        if room.get("available", 0) < 1:
            return f"🚫 No {room_type} rooms currently available at {hotel_name}."

        booking = {
            "guest_name": guest_name,
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out,
            "status": "Confirmed"
        }
        hotel["bookings"]["room"].append(booking)
        room["available"] -= 1

        return f"✅ {room_type} booked at {hotel_name} from {check_in} to {check_out}."

    except Exception as e:
        return f"⚠️ An error occurred while booking: {str(e)}"

def book_spa(hotel_name, spa_service, guest_name, appointment_time):
    try:
        hotel = hotel_data.get(hotel_name)
        if not hotel:
            return f"❌ Hotel '{hotel_name}' not found."

        if "Spa" not in hotel.get("facilities", {}):
            return f"❌ Spa not available at {hotel_name}."

        existing = hotel["bookings"]["spa"]
        if any(bk['appointment_time'] == appointment_time for bk in existing):
            return f"🚫 Time slot {appointment_time} already booked for Spa."

        booking = {
            "spa_service": spa_service,
            "guest_name": guest_name,
            "appointment_time": appointment_time,
            "status": "Confirmed"
        }
        hotel["bookings"]["spa"].append(booking)

        return f"✅ Spa appointment for {spa_service} booked at {appointment_time}."

    except Exception as e:
        return f"⚠️ Failed to book spa: {str(e)}"

def book_restaurant(hotel_name, meal_time, guest_name, reservation_time):
    try:
        hotel = hotel_data.get(hotel_name)
        if not hotel:
            return f"❌ Hotel '{hotel_name}' not found."

        if meal_time not in hotel.get("menu", {}):
            return f"❌ {meal_time} not available in restaurant."

        existing = hotel["bookings"]["restaurant"]
        if any(bk['reservation_time'] == reservation_time for bk in existing):
            return f"🚫 Restaurant is full at {reservation_time}. Try another time."

        booking = {
            "meal_time": meal_time,
            "guest_name": guest_name,
            "reservation_time": reservation_time,
            "status": "Confirmed"
        }
        hotel["bookings"]["restaurant"].append(booking)

        return f"✅ {meal_time} reservation confirmed at {reservation_time}."

    except Exception as e:
        return f"⚠️ Error in restaurant booking: {str(e)}"
