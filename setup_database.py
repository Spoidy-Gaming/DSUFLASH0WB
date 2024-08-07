import sqlite3

def create_and_populate_db():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('dsuniversity.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            fees TEXT,
            facilities TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hostels (
            id INTEGER PRIMARY KEY,
            room_type TEXT,
            fees TEXT,
            facilities TEXT
        )
    ''')

  cursor.execute('''
    CREATE TABLE info (
        id INTEGER PRIMARY KEY,
        infrastructure TEXT,
        location TEXT,
        application_link TEXT,
        admissions_office TEXT,
        support TEXT,
        phone TEXT,
        image_path TEXT
    )
''')

    # Insert data into courses (modify and add more data as needed)
    courses_data = [
        ('Computer Science', '130,000 - 200,000', 'Lab access, Online resources'),
        ('Engineering', '150,000 - 220,000', 'Lab access, Online resources, Workshops'),
        # Add other courses here
    ]
    cursor.executemany('INSERT INTO courses (name, fees, facilities) VALUES (?, ?, ?)', courses_data)

    # Insert data into hostels (modify and add more data as needed)
    hostels_data = [
        ('Single Room', '85,000', 'Single bed, Study table, Wi-Fi, Common Bathroom'),
        ('Shared Room', '60,000', 'Shared bed, Study table, Wi-Fi, Common Bathroom'),
        # Add other hostel types here
    ]
    cursor.executemany('INSERT INTO hostels (room_type, fees, facilities) VALUES (?, ?, ?)', hostels_data)

    # Insert general information (modify and add more data as needed)
  general_info = [
    ('Our college has state-of-the-art labs, libraries, sports facilities, and more.',
     'NH-45, Trichy Chennai Trunk Road Samayapuram, near Samayapuram Toll Plaza, Tiruchirappalli, Tamil Nadu 621112.',
     'https://admissions.dsuniversity.ac.in/', '1800 532 2222', 'enquiry@dsuniversity.ac.in', '70944 58021, 70944 58022',
     'static/images/academic_block.jpg')  # Add image path here
    ]
    cursor.executemany('INSERT INTO info (infrastructure, location, application_link, admissions_office, support, phone) VALUES (?, ?, ?, ?, ?, ?)', general_info)

    conn.commit()
    conn.close()

# Call the function to create and populate the database
create_and_populate_db()
