from flask import Flask, request, jsonify, render_template
import re
from twilio.rest import Client

app = Flask(__name__)

# Updated data with courses, hostel details, and fees structure
data = {
    "courses": {
        "computer_science": {
            "name": "Computer Science",
            "fees": "130,000 - 200,000",
            "facilities": "Lab access, Online resources"
        },
        "artificial_intelligence_data_science": {
            "name": "Artificial Intelligence and Data Science",
            "fees": "130,000 - 200,000",
            "facilities": "AI labs, Research projects"
        },
        "information_technology": {
            "name": "Information Technology",
            "fees": "130,000 - 200,000",
            "facilities": "IT labs, Software development resources"
        },
        "cyber_security": {
            "name": "Computer Science and Engineering with Cyber Security",
            "fees": "130,000 - 200,000",
            "facilities": "Cybersecurity labs, Research projects"
        },
        "ai_ml": {
            "name": "Artificial Intelligence and Machine Learning",
            "fees": "130,000 - 200,000",
            "facilities": "AI labs, Research projects"
        },
        "iot": {
            "name": "Computer Science Engineering with IoT",
            "fees": "100,000",
            "facilities": "IoT labs, Research projects"
        },
        "electronics_communication": {
            "name": "Electronics and Communication Engineering",
            "fees": "100,000",
            "facilities": "ECE labs, Research projects"
        },
        "agricultural_engineering": {
            "name": "Agricultural Engineering",
            "fees": "100,000",
            "facilities": "Agricultural labs, Field research"
        },
        "biomedical_engineering": {
            "name": "Biomedical Engineering",
            "fees": "100,000",
            "facilities": "Biomedical labs, Research projects"
        },
        "biotechnology": {
            "name": "Biotechnology",
            "fees": "100,000",
            "facilities": "Biotech labs, Research projects"
        },
        "electrical_electronics_engineering": {
            "name": "Electrical and Electronics Engineering",
            "fees": "100,000",
            "facilities": "EEE labs, Research projects"
        },
        "mechanical_engineering": {
            "name": "Mechanical Engineering",
            "fees": "100,000",
            "facilities": "Mechanical labs, Research projects"
        },
        "dialysis_technology": {
            "name": "Dialysis Technology",
            "fees": "125,000",
            "facilities": "Dialysis labs, Internship"
        },
        "optometry": {
            "name": "Optometry",
            "fees": "125,000",
            "facilities": "Optometry labs, Internship"
        },
        "physician_assistant": {
            "name": "Physician Assistant",
            "fees": "150,000",
            "facilities": "PA labs, Internship"
        },
        "radiography_imaging_technology": {
            "name": "Radiography and Imaging Technology",
            "fees": "150,000",
            "facilities": "Radiography labs, Internship"
        },
        "cardio_pulmonary_perfusion_technology": {
            "name": "Cardio Pulmonary and Perfusion Technology",
            "fees": "175,000",
            "facilities": "CPPT labs, Internship"
        },
        "operation_theatre_anesthesia_technology": {
            "name": "Operation Theatre and Anesthesia Technology",
            "fees": "200,000",
            "facilities": "OTAT labs, Internship"
        },
        "cardio_vascular_technology": {
            "name": "Cardio Vascular Technology",
            "fees": "200,000",
            "facilities": "CVT labs, Internship"
        },
        "medical_laboratory_technology": {
            "name": "Medical Laboratory Technology",
            "fees": "125,000",
            "facilities": "MLT labs, Internship"
        },
        "critical_care_technology": {
            "name": "Critical Care Technology",
            "fees": "100,000",
            "facilities": "CCT labs, Internship"
        },
        "accident_emergency_care_technology": {
            "name": "Accident and Emergency Care Technology",
            "fees": "100,000",
            "facilities": "AECT labs, Internship"
        },
        "agriculture_honors": {
            "name": "Agriculture (Honors)",
            "fees": "175,000",
            "facilities": "Agriculture labs, Field research"
        },
        "physiotherapy": {
            "name": "Bachelor of Physiotherapy",
            "fees": "125,000",
            "facilities": "Physiotherapy labs, Internship"
        },
        "pharmacy": {
            "name": "Bachelor of Pharmacy",
            "fees": "175,000",
            "facilities": "Pharmacy labs, Internship"
        }
    },
    "hostel": {
        "single_room": {
            "fees": "85,000",
            "facilities": "Single bed, Study table, Wi-Fi, Common Bathroom"
        },
        "double_room": {
            "fees": "125,000",
            "facilities": "Two beds, Study tables, A/C, Wi-Fi, Attached Bathroom"
        },
        "triple_room": {
            "fees": "75,000",
            "facilities": "Three beds, Study tables, Common Bathroom"
        }
    },
    "infrastructure": "Our college has state-of-the-art labs, libraries, sports facilities, and more.",
    "location": "NH-45, Trichy Chennai Trunk Road Samayapuram, near Samayapuram Toll Plaza, Tiruchirappalli, Tamil Nadu 621112.",
    "application_link": "https://admissions.dsuniversity.ac.in/",
    "contact": {
        "admissions_office": "1800 532 2222",
        "support": "enquiry@dsuniversity.ac.in",
        "phone": "70944 58021, 70944 58022"
    }
}

# Twilio credentials (replace with your own)
account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'your_auth_token'
twilio_client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query').lower()
    response = get_response(query)
    return jsonify(response)

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    phone_number = request.form.get('phone_number')
    message_body = request.form.get('message')
    try:
        message_sid = send_whatsapp_message(phone_number, message_body)
        return jsonify({"status": "Message sent", "sid": message_sid})
    except Exception as e:
        return jsonify({"status": "Failed to send message", "error": str(e)})

def get_response(query):
    if re.search(r'\bcourse\b|\bprogram\b|\bsubject\b|\bmajor\b|\bdiscipline\b', query) and re.search(r'\bfee\b|\bcost\b|\bprice\b|\btuition\b|\bcharges\b|\bexpenses\b', query):
        return get_course_fees(query)
    elif re.search(r'\bcourse\b|\bprogram\b|\bsubject\b|\bmajor\b|\bdiscipline\b', query) and re.search(r'\bfacilit(y|ies)\b|\bresource\b|\bamenit(y|ies)\b|\bprovision\b|\boffering\b', query):
        return get_course_facilities(query)
    elif re.search(r'\bcourse\b|\bprogram\b|\bsubject\b|\bmajor\b|\bdiscipline\b|\bfield of study\b', query) and re.search(r'\bavailable\b|\boffered\b', query):
        return get_course_list()
    elif re.search(r'\bhostel\b|\baccommodation\b|\bboarding\b|\broom\b|\blodging\b', query) and re.search(r'\bfee\b|\bcost\b|\bprice\b|\bcharges\b', query):
        return get_hostel_fees(query)
    elif re.search(r'\bhostel\b|\baccommodation\b|\bboarding\b|\broom\b|\blodging\b', query) and re.search(r'\bfacilit(y|ies)\b|\bamenit(y|ies)\b|\bprovision\b', query):
        return get_hostel_facilities(query)
    elif re.search(r'\binfrastructure\b|\bcampus\b|\bfacilit(y|ies)\b|\bamenit(y|ies)\b|\bresource\b|\benvironment\b|\bbuilding\b|\bsetup\b', query):
        return data['infrastructure']
    elif re.search(r'\blocation\b|\baddress\b|\bplace\b|\bsituated\b|\blocated\b|\bwhere\b', query):
        return data['location']
    elif re.search(r'\bapplication\b|\bapply\b|\badmission\b|\bform\b|\benroll\b|\bregistration\b|\bprocess\b|\blink\b', query):
        return data['application_link']
    elif re.search(r'\bcontact\b|\bphone\b|\bnumber\b|\bemail\b|\baddress\b|\breach\b|\bget in touch\b|\bcommunicate\b', query):
        return data['contact']
    else:
        return {"message": "Sorry, I don't understand that question. Please ask about course fees, facilities, hostel details, infrastructure, location, application process, or contact information."}

def get_course_fees(query):
    for course_key, course_info in data['courses'].items():
        if re.search(course_info['name'].lower(), query):
            return {
                "course": course_info['name'],
                "fees": course_info['fees'],
                "message": f"The fees for the {course_info['name']} course are {course_info['fees']}."
            }
    return {"message": "Course not found. Please specify a valid course name."}

def get_course_facilities(query):
    for course_key, course_info in data['courses'].items():
        if re.search(course_info['name'].lower(), query):
            return {
                "course": course_info['name'],
                "facilities": course_info['facilities'],
                "message": f"The facilities for the {course_info['name']} course include: {course_info['facilities']}."
            }
    return {"message": "Course not found. Please specify a valid course name."}

def get_course_list():
    course_list = [course_info['name'] for course_info in data['courses'].values()]
    return {
        "courses": course_list,
        "message": "The available courses are: " + ", ".join(course_list) + "."
    }

def get_hostel_fees(query):
    hostel_fees = {room_type: info['fees'] for room_type, info in data['hostel'].items()}
    return {
        "hostel_fees": hostel_fees,
        "message": "The hostel fees are as follows: " + ", ".join([f"{room_type.replace('_', ' ').title()}: {fee}" for room_type, fee in hostel_fees.items()]) + "."
    }

def get_hostel_facilities(query):
    hostel_facilities = {room_type: info['facilities'] for room_type, info in data['hostel'].items()}
    return {
        "hostel_facilities": hostel_facilities,
        "message": "The hostel facilities are as follows: " + ", ".join([f"{room_type.replace('_', ' ').title()}: {facilities}" for room_type, facilities in hostel_facilities.items()]) + "."
    }

def send_whatsapp_message(phone_number, message_body):
    message = twilio_client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',  # Twilio Sandbox WhatsApp number
        to=f'whatsapp:{phone_number}'
    )
    return message.sid

if __name__ == '__main__':
    app.run(debug=True)
