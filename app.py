from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)

# Sample data for demonstration purposes
data = {
    "courses": {
        "course_1": {
            "name": "Computer Science",
            "fees": "1,12,500",
            "facilities": "Lab access, Online resources"
        },
        "course_2": {
            "name": "Mechanical Engineering",
            "fees": "50000",
            "facilities": "Workshops, Lab access"
        },
        "course_3": {
            "name": "Business Administration",
            "fees": "85000",
            "facilities": "Library access, Case studies"
        }
    },
    "hostel": {
        "single_room": {
            "fees": "85000",
            "facilities": "Single bed, Study table, Wi-Fi,Common Bathroom"
        },
        "double_room": {
            "fees": "125000",
            "facilities": "Two beds, Study tables,A/c, Wi-Fi,Attached Bathroom"
        }
    },
    "infrastructure": "Our college has state-of-the-art labs, libraries, sports facilities, and more.",
    "location": "NH-45, Trichy Chennai Trunk Road Samayapuram, near Samayapuram Toll Plaza, Tiruchirappalli, Tamil Nadu 621112.",
    "application_link": "https://admissions.dsuniversity.ac.in/",
    "contact": {
        "admissions_office": "1800 532 2222",
        "support": "enquiry@dsuniversity.ac.in",
        "phone": "70944 58021,70944 58022"
    }
}

# Twilio credentials (replace with your own)
account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')  # Twilio Sandbox number

# Initialize Twilio client
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query').lower()
    response = get_response(query)
    return jsonify(response)

# Route to handle incoming messages from WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '').lower()
    response_message = get_response(incoming_message)
    response = MessagingResponse()
    response.message(response_message)
    return str(response)

def get_response(query):
    if "course fees" in query:
        return get_course_fees(query)
    elif "course facilities" in query:
        return get_course_facilities(query)
    elif "hostel fees" in query:
        return get_hostel_fees(query)
    elif "hostel facilities" in query:
        return get_hostel_facilities(query)
    elif "infrastructure" in query:
        return data['infrastructure']
    elif "location" in query:
        return data['location']
    elif "apply" in query or "admission" in query:
        return data['application_link']
    elif "contact" in query:
        return data['contact']
    else:
        return "Sorry, I don't understand that question."

def get_course_fees(query):
    for course_key, course_info in data['courses'].items():
        if course_info['name'].lower() in query:
            return f"{course_info['name']} course fees: {course_info['fees']}"
    return "Course not found."

def get_course_facilities(query):
    for course_key, course_info in data['courses'].items():
        if course_info['name'].lower() in query:
            return f"{course_info['name']} course facilities: {course_info['facilities']}"
    return "Course not found."

def get_hostel_fees(query):
    return "Hostel fees: " + ", ".join([f"{room_type}: {info['fees']}" for room_type, info in data['hostel'].items()])

def get_hostel_facilities(query):
    return "Hostel facilities: " + ", ".join([f"{room_type}: {info['facilities']}" for room_type, info in data['hostel'].items()])

if __name__ == '__main__':
    app.run(debug=True)
