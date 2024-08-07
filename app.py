from flask import Flask, request, jsonify, render_template
import re
import sqlite3
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials (replace with your own)
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_client = Client(account_sid, auth_token)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('dsuniversity.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query').lower()
    response = get_response(query)
    return jsonify(response)

def get_response(query):
    if re.search(r'\bcourse\b|\bprogram\b|\bsubject\b|\bmajor\b|\bdiscipline\b', query):
        if re.search(r'\bfee\b|\bcost\b|\bprice\b|\btuition\b|\bcharges\b|\bexpenses\b', query):
            return get_course_fees(query)
        elif re.search(r'\bfacilit(y|ies)\b|\bresource\b|\bamenit(y|ies)\b|\bprovision\b|\boffering\b', query):
            return get_course_facilities(query)
        else:
            return get_course_list()
    elif re.search(r'\bhostel\b|\baccommodation\b|\bboarding\b|\broom\b|\blodging\b', query):
        if re.search(r'\bfee\b|\bcost\b|\bprice\b|\bcharges\b', query):
            return get_hostel_fees(query)
        elif re.search(r'\bfacilit(y|ies)\b|\bamenit(y|ies)\b|\bprovision\b', query):
            return get_hostel_facilities(query)
    elif re.search(r'\binfrastructure\b|\bcampus\b|\bfacilit(y|ies)\b|\bamenit(y|ies)\b|\bresource\b|\benvironment\b|\bbuilding\b|\bsetup\b', query):
        return get_infrastructure()
    elif re.search(r'\blocation\b|\baddress\b|\bplace\b|\bsituated\b|\blocated\b|\bwhere\b', query):
        return get_location()
    elif re.search(r'\bapplication\b|\bapply\b|\badmission\b|\bform\b|\benroll\b|\bregistration\b|\bprocess\b|\blink\b', query):
        return get_application_link()
    elif re.search(r'\bcontact\b|\bphone\b|\bnumber\b|\bemail\b|\baddress\b|\breach\b|\bget in touch\b|\bcommunicate\b', query):
        return get_contact()
    else:
        return {"message": "Sorry, I don't understand that question. Please ask about course fees, facilities, hostel details, infrastructure, location, application process, or contact information."}

def get_course_fees(query):
    courses = query_db("SELECT name, fees FROM courses")
    for course in courses:
        if re.search(course[0].lower(), query):
            return {"course": course[0], "fees": course[1], "message": f"The fees for the {course[0]} course are {course[1]}."}
    return {"message": "Course not found. Please specify a valid course name."}

def get_course_facilities(query):
    courses = query_db("SELECT name, facilities FROM courses")
    for course in courses:
        if re.search(course[0].lower(), query):
            return {"course": course[0], "facilities": course[1], "message": f"The facilities for the {course[0]} course include: {course[1]}."}
    return {"message": "Course not found. Please specify a valid course name."}

def get_course_list():
    courses = query_db("SELECT name FROM courses")
    course_list = [course[0] for course in courses]
    return {"courses": course_list, "message": "The available courses are: " + ", ".join(course_list) + "."}

def get_hostel_fees(query):
    hostels = query_db("SELECT room_type, fees FROM hostels")
    hostel_fees = {hostel[0]: hostel[1] for hostel in hostels}
    return {"hostel_fees": hostel_fees, "message": "The hostel fees are as follows: " + ", ".join([f"{k}: {v}" for k, v in hostel_fees.items()]) + "."}

def get_hostel_facilities(query):
    hostels = query_db("SELECT room_type, facilities FROM hostels")
    hostel_facilities = {hostel[0]: hostel[1] for hostel in hostels}
    return {"hostel_facilities": hostel_facilities, "message": "The hostel facilities are as follows: " + ", ".join([f"{k}: {v}" for k, v in hostel_facilities.items()]) + "."}

def get_infrastructure():
    infrastructure = query_db("SELECT infrastructure FROM info", one=True)
    return {"infrastructure": infrastructure[0]}

def get_location():
    location = query_db("SELECT location FROM info", one=True)
    return {"location": location[0]}

def get_application_link():
    application_link = query_db("SELECT application_link FROM info", one=True)
    return {"application_link": application_link[0]}

def get_contact():
    contact = query_db("SELECT admissions_office, support, phone FROM info", one=True)
    return {"contact": {"admissions_office": contact[0], "support": contact[1], "phone": contact[2]}}

if __name__ == '__main__':
    app.run(debug=True)
